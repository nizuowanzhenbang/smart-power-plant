"""明确范围的文档、状态和固定发布核验。"""
from pathlib import Path
import re
from urllib.parse import unquote

from .github import ProgressError
from .state import CORE, REPO, SHA, strict_json, tasks, validate_session


def audit(root, api=None):
    root = Path(root)
    directory = root / 'progress'
    errors = []
    try:
        for name in CORE:
            if not (directory/name).is_file() or not (directory/name).read_text().strip():
                raise ProgressError('核心文件缺失或为空：' + name)
        registry = tasks((directory/'TASKS.md').read_text())
        validate_session(strict_json((directory/'SESSION.json').read_text()), registry)
        manifest = strict_json((directory/'RELEASES.json').read_text())
        if not isinstance(manifest, dict) or manifest.get('schema_version') != 1 or not isinstance(manifest.get('releases'), list):
            raise ProgressError('RELEASES 结构错误')
        seen = set()
        for item in manifest['releases']:
            task = item.get('task_id')
            if task in seen or registry.get(task) != '已合并':
                raise ProgressError('交付索引任务重复或状态不一致：' + str(task))
            seen.add(task)
            if (not REPO.fullmatch(item.get('repository', '')) or not SHA.fullmatch(item.get('commit', ''))
                    or not isinstance(item.get('pr'), int) or isinstance(item['pr'], bool) or item['pr'] <= 0
                    or not isinstance(item.get('checks'), list) or not item['checks']
                    or any(not isinstance(name, str) or not name.strip() for name in item['checks'])):
                raise ProgressError('交付索引字段错误：' + str(task))
            if api:
                verify_release(api, item)
        for path in directory.rglob('*.md'):
            for link in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', path.read_text()):
                target = link.strip().strip('<>').split('#', 1)[0]
                if not target or '://' in target or target.startswith(('mailto:', 'app:')):
                    continue
                if not (path.parent/unquote(target)).exists():
                    errors.append(f'{path.relative_to(root)}：失效链接 {target}')
    except (ProgressError, OSError, TypeError, KeyError, AttributeError) as exc:
        errors.append(str(exc))
    return errors


def verify_release(api, item):
    repo, commit, number = item['repository'], item['commit'], item['pr']
    if api.request(f'repos/{repo}/commits/{commit}').get('sha') != commit:
        raise ProgressError('固定代码 SHA 不一致')
    pr = api.request(f'repos/{repo}/pulls/{number}')
    if pr.get('merged') is not True or pr.get('merge_commit_sha') != commit:
        raise ProgressError('PR 未合并或固定合并 SHA 不一致')
    runs = []
    for page in range(1, 11):
        response = api.request(f'repos/{repo}/commits/{commit}/check-runs?per_page=100&page={page}')
        batch = response.get('check_runs', [])
        runs.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise ProgressError('检查分页超限；未完成核验')
    for name in item['checks']:
        matches = [run for run in runs if run.get('name') == name]
        latest = max(matches, key=lambda run: run.get('id', 0), default=None)
        if not latest or latest.get('status') != 'completed' or latest.get('conclusion') != 'success':
            raise ProgressError(f'{repo}@{commit} 检查 {name} 缺失、未完成或未成功')
