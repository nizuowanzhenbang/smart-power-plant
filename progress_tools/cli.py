"""供 Codex 与人工共同使用的显式恢复/保存命令。"""
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

from .audit import audit
from .github import GitHub, ProgressError
from .state import CORE, PHASES, mutate, snapshot


def main(argv=None):
    parser = argparse.ArgumentParser(description='电厂进度恢复、条件保存与发布核验')
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--repo', default='nizuowanzhenbang/smart-power-plant')
    parser.add_argument('--api-url', default='https://api.github.com')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('resume')
    check = sub.add_parser('check')
    mode = check.add_mutually_exclusive_group(required=True)
    mode.add_argument('--offline', action='store_true')
    mode.add_argument('--remote', action='store_true')
    for command in ['claim', 'checkpoint', 'release']:
        item = sub.add_parser(command)
        item.add_argument('task')
        item.add_argument('--owner', required=True)
        item.add_argument('--expected-sha')
        if command == 'claim':
            item.add_argument('--code-repo', required=True)
            item.add_argument('--branch', required=True)
            item.add_argument('--takeover-from')
            item.add_argument('--reason')
        elif command == 'checkpoint':
            item.add_argument('--phase', choices=sorted(PHASES - {'claimed'}), required=True)
            item.add_argument('--commit', required=True)
            item.add_argument('--note', required=True)
            item.add_argument('--next-action', required=True)
            item.add_argument('--pr', type=int)
        else:
            item.add_argument('--reason', required=True)
    args = parser.parse_args(argv)
    try:
        host = urlparse(args.api_url)
        if not ((host.scheme == 'https' and host.hostname == 'api.github.com')
                or (host.scheme == 'http' and host.hostname in {'127.0.0.1', 'localhost', '::1'})):
            raise ProgressError('API 地址只允许 GitHub HTTPS 或本地测试服务')
        api = None if args.command == 'check' and args.offline else GitHub(args.api_url)
        if args.command == 'check':
            errors = audit(args.root, api)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print('进度核验通过（' + ('离线结构/链接' if args.offline else '结构/链接及索引范围的真实发布') + '）')
        elif args.command == 'resume':
            sha, files, _, state = snapshot(api, args.repo)
            print('中央固定 SHA：' + sha)
            for name in CORE:
                print('\n# progress/' + name + '\n' + files[name])
            print('\n# 实时会话与最后交接\n' + json.dumps(state, ensure_ascii=False, indent=2))
        else:
            sha = mutate(api, args.repo, args.command, args.task, args.owner, vars(args), args.expected_sha)
            print(json.dumps({'central_sha': sha, 'task_id': args.task, 'operation': args.command,
                              'synced': True}, ensure_ascii=False))
        return 0
    except (ProgressError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
