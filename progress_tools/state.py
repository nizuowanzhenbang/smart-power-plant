"""固定版本恢复与单活动认领，状态写入须保留真实代码证据。"""
from datetime import datetime, timezone
import json
import re

from .github import ProgressError

CORE = ['AGENTS.md', 'SUMMARY.md', 'CURRENT.md', 'TASKS.md']
STATUSES = {'待核查', '待做', '进行中', '已验证候选', '已合并', '阻塞', '已有覆盖', '取消'}
PHASES = {'claimed', 'decision', 'reproduced', 'implemented', 'reviewed', 'pr_open', 'merged'}
SHA = re.compile(r'^[0-9a-f]{40}$')
REPO = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')


def now():
    return datetime.now(timezone.utc).isoformat()


def text_value(value, label):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise ProgressError(label + ' 必须为非空单行文本')
    return value


def strict_json(value):
    def pairs(items):
        result = {}
        for key, item in items:
            if key in result:
                raise ProgressError('JSON 重复字段：' + key)
            result[key] = item
        return result
    def invalid(_):
        raise ProgressError('JSON 不接受非有限数')
    try:
        return json.loads(value, object_pairs_hook=pairs, parse_constant=invalid)
    except ValueError as exc:
        raise ProgressError('JSON 格式错误') from exc


def tasks(markdown):
    result = {}
    headers = []
    for line in markdown.splitlines():
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if '编号' in cells and '状态' in cells:
            headers = cells
            continue
        if not headers or not re.fullmatch(r'(PP-\d{3}|DONE-[A-Z]+-\d+)', cells[0]):
            continue
        key = cells[0]
        if key in result:
            raise ProgressError('任务编号重复：' + key)
        index = headers.index('状态')
        if len(cells) <= index or cells[index] not in STATUSES:
            raise ProgressError('任务状态错误：' + key)
        result[key] = cells[index]
    if not result:
        raise ProgressError('未找到任务台账')
    return result


def validate_session(state, registry):
    if not isinstance(state, dict) or state.get('schema_version') != 1 or not {'active', 'last'} <= state.keys():
        raise ProgressError('SESSION 结构错误')
    for name in ['active', 'last']:
        item = state[name]
        if item is None:
            continue
        if not isinstance(item, dict) or item.get('task_id') not in registry:
            raise ProgressError('SESSION 包含未知任务')
        if name == 'active' and registry[item['task_id']] in {'已合并', '已有覆盖', '取消'}:
            raise ProgressError('不可认领已完成任务')
        for field in ['owner', 'branch', 'started_at', 'updated_at']:
            text_value(item.get(field), field)
        if not REPO.fullmatch(item.get('code_repository', '')):
            raise ProgressError('目标仓库格式错误')
        for field in ['started_at', 'updated_at']:
            try:
                stamp = datetime.fromisoformat(item[field])
                if stamp.utcoffset() is None or stamp.utcoffset().total_seconds() != 0:
                    raise ValueError()
            except ValueError as exc:
                raise ProgressError('时间必须使用 UTC ISO 格式') from exc
        checkpoint = item.get('checkpoint')
        if not isinstance(checkpoint, dict) or checkpoint.get('phase') not in PHASES:
            raise ProgressError('检查点阶段错误')
        text_value(checkpoint.get('note'), 'note')
        text_value(checkpoint.get('next_action'), 'next_action')
        if checkpoint.get('commit') is not None and not SHA.fullmatch(checkpoint['commit']):
            raise ProgressError('检查点必须记录完整代码 SHA')


def snapshot(api, repo, expected_sha=None):
    if not REPO.fullmatch(repo):
        raise ProgressError('中央仓库格式错误')
    sha = expected_sha or api.request(f'repos/{repo}/commits/main')['sha']
    if not SHA.fullmatch(sha):
        raise ProgressError('中央版本必须为完整 SHA')
    files = {name: api.file(repo, 'progress/' + name, sha) for name in CORE + ['SESSION.json']}
    registry = tasks(files['TASKS.md'])
    state = strict_json(files['SESSION.json'])
    validate_session(state, registry)
    return sha, files, registry, state


def mutate(api, repo, command, task, owner, metadata, expected_sha=None):
    text_value(owner, 'owner')
    sha, _, registry, state = snapshot(api, repo, expected_sha)
    if task not in registry:
        raise ProgressError('未知任务：' + task)
    active = state['active']
    if command == 'claim':
        if registry[task] in {'已合并', '已有覆盖', '取消'}:
            raise ProgressError('不可认领已完成任务')
        code_repo = metadata.get('code_repo', '')
        branch = text_value(metadata.get('branch'), 'branch')
        if not REPO.fullmatch(code_repo):
            raise ProgressError('目标仓库格式错误')
        if active:
            if (active['task_id'], active['owner'], active['code_repository'], active['branch']) == (task, owner, code_repo, branch):
                return sha
            if (metadata.get('takeover_from') != active['owner'] or active['task_id'] != task
                    or active['code_repository'] != code_repo or active['branch'] != branch):
                raise ProgressError('任务已认领；复读原分支/PR，不能覆盖其他执行者')
            reason = text_value(metadata.get('reason'), '接管理由')
            active.setdefault('takeovers', []).append({'previous_owner': active['owner'], 'reason': reason, 'at': now()})
            active['owner'] = owner
            active['updated_at'] = now()
        else:
            state['active'] = {'task_id': task, 'owner': owner, 'code_repository': code_repo,
                               'branch': branch, 'started_at': now(), 'updated_at': now(),
                               'checkpoint': {'phase': 'claimed', 'commit': None,
                                              'note': '已认领；尚未完成实现', 'next_action': '读取实际代码与计划'}}
    else:
        if not active or active['task_id'] != task or active['owner'] != owner:
            raise ProgressError('当前认领或执行者不匹配')
        if command == 'checkpoint':
            phase = metadata.get('phase')
            if phase not in PHASES - {'claimed'}:
                raise ProgressError('检查点阶段错误')
            commit = metadata.get('commit', '')
            if not SHA.fullmatch(commit):
                raise ProgressError('需要完整远端代码 SHA')
            code_repo = active['code_repository']
            remote = api.request(f'repos/{code_repo}/commits/{commit}')
            if remote.get('sha') != commit:
                raise ProgressError('远端代码 SHA 不一致')
            number = metadata.get('pr')
            if phase in {'pr_open', 'merged'}:
                if not isinstance(number, int) or number <= 0:
                    raise ProgressError('该阶段需要实际 PR 编号')
                pr = api.request(f'repos/{code_repo}/pulls/{number}')
                if phase == 'merged' and (pr.get('merged') is not True or pr.get('merge_commit_sha') != commit):
                    raise ProgressError('PR 未合并或合并 SHA 不一致')
                if phase == 'pr_open' and (pr.get('state') != 'open' or pr.get('head', {}).get('sha') != commit):
                    raise ProgressError('PR 候选状态或 SHA 不一致')
            active['checkpoint'] = {'phase': phase, 'commit': commit, 'pr': number,
                                    'note': text_value(metadata.get('note'), 'note'),
                                    'next_action': text_value(metadata.get('next_action'), 'next_action')}
            active['updated_at'] = now()
        elif command == 'release':
            active['release_reason'] = text_value(metadata.get('reason'), '释放理由')
            active['released_at'] = now()
            state['last'] = active
            state['active'] = None
        else:
            raise ProgressError('未知状态操作')
    validate_session(state, registry)
    return api.publish(repo, sha, state)
