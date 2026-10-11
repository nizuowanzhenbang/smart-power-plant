"""只读快照与 GitHub Git ref 条件发布。"""
import base64
import json
import os
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ProgressError(Exception):
    pass


class GitHub:
    def __init__(self, api_url='https://api.github.com', token=None):
        self.api_url = api_url.rstrip('/')
        if token is None:
            token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
            if not token:
                result = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True)
                if result.returncode:
                    raise ProgressError('GitHub 认证不可用；未读取或同步进度')
                token = result.stdout.strip()
        self.token = token

    def request(self, path, method='GET', body=None):
        headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode()
            headers['Content-Type'] = 'application/json'
        try:
            with urlopen(Request(self.api_url + '/' + path.lstrip('/'), data=data,
                                 headers=headers, method=method), timeout=20) as response:
                return json.load(response)
        except HTTPError as exc:
            raise ProgressError(f'GitHub HTTP {exc.code}：{path}；未同步/未验证，复读状态后再处理') from exc
        except (URLError, TimeoutError, ValueError) as exc:
            raise ProgressError('GitHub 访问或响应失败；不能声称已读取、同步或验证') from exc

    def file(self, repo, path, sha):
        value = self.request(f'repos/{repo}/contents/{path}?ref={sha}')
        if value.get('encoding') != 'base64':
            raise ProgressError('GitHub 文件编码不受支持')
        try:
            return base64.b64decode(value['content']).decode('utf-8')
        except (KeyError, ValueError, UnicodeError) as exc:
            raise ProgressError('GitHub 文件不可解码') from exc

    def publish(self, repo, parent, state):
        """不重试、不强推；同一父版本的竞争提交只能有一个进入 main。"""
        prefix = f'repos/{repo}/git'
        content = json.dumps(state, ensure_ascii=False, indent=2) + '\n'
        blob = self.request(prefix + '/blobs', 'POST', {
            'encoding': 'base64', 'content': base64.b64encode(content.encode()).decode(),
        })['sha']
        base_tree = self.request(prefix + '/commits/' + parent)['tree']['sha']
        tree = self.request(prefix + '/trees', 'POST', {'base_tree': base_tree, 'tree': [{
            'path': 'progress/SESSION.json', 'mode': '100644', 'type': 'blob', 'sha': blob,
        }]})['sha']
        commit = self.request(prefix + '/commits', 'POST', {
            'message': 'progress: 保存会话认领或阶段交接', 'tree': tree, 'parents': [parent],
        })['sha']
        self.request(prefix + '/refs/heads/main', 'PATCH', {'sha': commit, 'force': False})
        return commit
