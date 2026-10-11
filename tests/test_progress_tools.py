"""真实 CLI/临时 HTTP 验证恢复、Git 条件写入与核验失败路径。"""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '1' * 40
CODE = 'c' * 40
MERGED = 'b' * 40


def digest(value):
    return hashlib.sha1(json.dumps(value, sort_keys=True).encode()).hexdigest()


class Store:
    def __init__(self):
        self.head = INITIAL
        self.blobs = {}
        self.trees = {}
        self.commits = {}
        self.lock = threading.Lock()
        self.checks = [{'name': name, 'id': i, 'status': 'completed', 'conclusion': 'success'}
                       for i, name in enumerate(['backend', 'frontend'])]
        self.pr = {'merged': True, 'merge_commit_sha': MERGED}
        self.fail_code = None
        files = {p: (ROOT / 'progress' / p).read_text() for p in ['AGENTS.md', 'SUMMARY.md', 'CURRENT.md']}
        files['TASKS.md'] = '| 编号 | 状态 |\n|---|---|\n| PP-003 | 待做 |\n| PP-004 | 待做 |\n| PP-010 | 已合并 |\n'
        files['SESSION.json'] = json.dumps({'schema_version': 1, 'active': None, 'last': None})
        tree = digest(files)
        self.trees[tree] = {'progress/' + p: content for p, content in files.items()}
        self.commits[INITIAL] = {'tree': {'sha': tree}, 'parents': []}

    def files(self):
        return self.trees[self.commits[self.head]['tree']['sha']]

    def session(self):
        return json.loads(self.files()['progress/SESSION.json'])


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def answer(self, code, value):
        data = json.dumps(value).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        s = self.server.store
        if s.fail_code:
            return self.answer(s.fail_code, {'message': 'simulated access failure'})
        url = urlparse(self.path)
        path = unquote(url.path)
        if path == '/repos/demo/progress/commits/main':
            return self.answer(200, {'sha': s.head})
        if '/contents/' in path:
            filename = path.split('/contents/')[1]
            ref = parse_qs(url.query).get('ref', [s.head])[0]
            if ref not in s.commits:
                return self.answer(404, {})
            files = s.trees[s.commits[ref]['tree']['sha']]
            if filename not in files:
                return self.answer(404, {})
            content = files[filename]
            return self.answer(200, {'sha': digest(content), 'encoding': 'base64',
                                     'content': base64.b64encode(content.encode()).decode()})
        if '/git/commits/' in path:
            value = s.commits.get(path.split('/')[-1])
            return self.answer(200 if value else 404, value or {})
        if path.startswith('/repos/demo/code/commits/') and path.endswith('/check-runs'):
            return self.answer(200, {'check_runs': s.checks})
        if path.startswith('/repos/demo/code/commits/'):
            ref = path.split('/')[-1]
            return self.answer(200 if ref in [CODE, MERGED] else 404, {'sha': ref})
        if path == '/repos/demo/code/pulls/3':
            return self.answer(200, s.pr)
        return self.answer(404, {})

    def do_POST(self):
        s = self.server.store
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        if self.path.endswith('/git/blobs'):
            key = digest(body)
            s.blobs[key] = base64.b64decode(body['content']).decode()
        elif self.path.endswith('/git/trees'):
            files = dict(s.trees[body['base_tree']])
            for entry in body['tree']:
                files[entry['path']] = s.blobs[entry['sha']]
            key = digest(files)
            s.trees[key] = files
        elif self.path.endswith('/git/commits'):
            key = digest(body)
            s.commits[key] = {'tree': {'sha': body['tree']}, 'parents': body['parents']}
        else:
            return self.answer(404, {})
        return self.answer(201, {'sha': key})

    def do_PATCH(self):
        s = self.server.store
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        with s.lock:
            # GitHub 非强制 ref 更新的 fast-forward 契约：竞争提交的父版本必须仍为当前版本。
            if body.get('force') is not False or s.commits[body['sha']]['parents'] != [s.head]:
                return self.answer(422, {'message': 'not a fast forward'})
            s.head = body['sha']
        return self.answer(200, {'object': {'sha': s.head}})


class ProgressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.api_url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.store = Store()
        self.server.store = self.store
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / 'progress', self.root / 'progress')
        (self.root / 'progress/SESSION.json').write_text(json.dumps({'schema_version': 1, 'active': None, 'last': None}))
        (self.root / 'progress/RELEASES.json').write_text(json.dumps({'schema_version': 1, 'releases': [
            {'task_id': 'PP-010', 'repository': 'demo/code', 'commit': MERGED, 'pr': 3,
             'checks': ['backend', 'frontend']}]}))

    def invoke(self, *args):
        env = dict(os.environ, GH_TOKEN='fixture-token')
        return subprocess.run([sys.executable, '-m', 'progress_tools', '--root', str(self.root),
                               '--api-url', self.api_url, '--repo', 'demo/progress', *args],
                              cwd=ROOT, env=env, capture_output=True, text=True)

    def ok(self, *args):
        result = self.invoke(*args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def reject(self, *args):
        before = self.store.session()
        result = self.invoke(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.store.session(), before)
        return result

    def claim(self, owner='alice', *extra):
        return self.ok('claim', 'PP-003', '--owner', owner, '--code-repo', 'demo/code', '--branch', 'work', *extra)

    def test_resume_reads_one_immutable_snapshot(self):
        result = self.ok('resume')
        self.assertIn(INITIAL, result.stdout)
        for filename in ['AGENTS.md', 'SUMMARY.md', 'CURRENT.md', 'TASKS.md']:
            self.assertIn(filename, result.stdout)
        self.assertEqual(self.store.head, INITIAL)

    def test_claim_persists_owner_and_task(self):
        self.claim()
        active = self.store.session()['active']
        self.assertEqual((active['task_id'], active['owner']), ('PP-003', 'alice'))
        self.assertNotEqual(self.store.head, INITIAL)

    def test_claim_competition_has_one_winner(self):
        results = []
        def attempt(owner):
            results.append(self.invoke('claim', 'PP-003', '--owner', owner, '--code-repo', 'demo/code',
                                       '--branch', 'work', '--expected-sha', INITIAL))
        threads = [threading.Thread(target=attempt, args=(owner,)) for owner in ['alice', 'bob']]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(r.returncode for r in results), [0, 1])
        self.assertIn(self.store.session()['active']['owner'], ['alice', 'bob'])

    def test_stale_write_cannot_replace_claim(self):
        self.claim()
        self.reject('claim', 'PP-004', '--owner', 'bob', '--code-repo', 'demo/code', '--branch', 'work',
                    '--expected-sha', INITIAL)

    def test_stale_identical_claim_cannot_report_success_after_takeover(self):
        self.claim()
        old = self.store.head
        self.claim('bob', '--takeover-from', 'alice', '--reason', 'previous session stopped')
        self.reject('claim', 'PP-003', '--owner', 'alice', '--code-repo', 'demo/code',
                    '--branch', 'work', '--expected-sha', old)
        self.assertEqual(self.store.session()['active']['owner'], 'bob')

    def test_same_current_claim_remains_idempotent(self):
        self.claim()
        current = self.store.head
        self.claim('alice', '--expected-sha', current)
        self.assertEqual(self.store.head, current)

    def test_malformed_checkpoints_and_handoffs_are_rejected(self):
        self.claim()
        valid = self.store.session()
        for phase in ['decision', 'reproduced', 'implemented', 'reviewed', 'pr_open', 'merged']:
            with self.subTest(phase=phase):
                state = json.loads(json.dumps(valid))
                state['active']['checkpoint'].update(phase=phase, commit=None, pr=None)
                self.store.files()['progress/SESSION.json'] = json.dumps(state)
                self.reject('release', 'PP-003', '--owner', 'alice', '--reason', 'handoff')
                (self.root/'progress/SESSION.json').write_text(json.dumps(state))
                self.assertNotEqual(self.invoke('check', '--offline').returncode, 0)
        for changes in [{'phase': 'merged', 'commit': CODE, 'pr': None},
                        {'phase': 'pr_open', 'commit': CODE, 'pr': True},
                        {'phase': 'implemented', 'commit': 17}]:
            with self.subTest(changes=changes):
                state = json.loads(json.dumps(valid))
                state['active']['checkpoint'].update(changes)
                (self.root/'progress/SESSION.json').write_text(json.dumps(state))
                self.assertNotEqual(self.invoke('check', '--offline').returncode, 0)
        for changes in [{'release_reason': '', 'released_at': 'invalid'},
                        {'takeovers': [{'previous_owner': '', 'reason': 'handoff', 'at': 'bad'}]}]:
            state = json.loads(json.dumps(valid))
            state['last'] = state.pop('active')
            state['active'] = None
            state['last'].update(changes)
            (self.root/'progress/SESSION.json').write_text(json.dumps(state))
            self.assertNotEqual(self.invoke('check', '--offline').returncode, 0)

    def test_publication_preserves_existing_active_batch_owner(self):
        state = json.loads((ROOT/'progress/evidence/2026-10-11-session-migration.json').read_text())
        active = state['active']
        self.assertIsNotNone(active, 'publication must migrate the active PP-003 claim')
        self.assertEqual((active['task_id'], active['owner']),
                         ('PP-003', 'codex-batch-20261011-01'))
        self.store.files()['progress/SESSION.json'] = json.dumps(state)
        self.reject('claim', 'PP-003', '--owner', 'bob', '--code-repo',
                    active['code_repository'], '--branch', active['branch'])

    def test_other_owner_cannot_claim_checkpoint_or_release(self):
        self.claim()
        self.reject('claim', 'PP-004', '--owner', 'bob', '--code-repo', 'demo/code', '--branch', 'work')
        self.reject('checkpoint', 'PP-003', '--owner', 'bob', '--phase', 'implemented', '--commit', CODE,
                    '--note', 'done', '--next-action', 'review')
        self.reject('release', 'PP-003', '--owner', 'bob', '--reason', 'resume')

    def test_completed_and_unknown_tasks_cannot_be_claimed(self):
        for task in ['PP-010', 'PP-999']:
            self.reject('claim', task, '--owner', 'alice', '--code-repo', 'demo/code', '--branch', 'work')

    def test_empty_owner_is_rejected(self):
        self.reject('claim', 'PP-003', '--owner', '', '--code-repo', 'demo/code', '--branch', 'work')

    def test_explicit_takeover_preserves_reason(self):
        self.claim()
        self.reject('claim', 'PP-003', '--owner', 'bob', '--code-repo', 'demo/code', '--branch', 'work',
                    '--takeover-from', 'alice')
        self.claim('bob', '--takeover-from', 'alice', '--reason', 'old session ended; inspected branch')
        active = self.store.session()['active']
        self.assertEqual(active['owner'], 'bob')
        self.assertEqual(active['takeovers'][-1]['previous_owner'], 'alice')

    def test_checkpoint_records_pushed_revision_and_next_action(self):
        self.claim()
        self.ok('checkpoint', 'PP-003', '--owner', 'alice', '--phase', 'implemented', '--commit', CODE,
                '--note', 'tests passed', '--next-action', 'independent review')
        stage = self.store.session()['active']['checkpoint']
        self.assertEqual((stage['commit'], stage['next_action']), (CODE, 'independent review'))

    def test_checkpoint_rejects_missing_remote_revision(self):
        self.claim()
        self.reject('checkpoint', 'PP-003', '--owner', 'alice', '--phase', 'implemented', '--commit', 'd' * 40,
                    '--note', 'not pushed', '--next-action', 'review')

    def test_merged_checkpoint_requires_real_merge_sha(self):
        self.claim()
        self.reject('checkpoint', 'PP-003', '--owner', 'alice', '--phase', 'merged', '--commit', CODE,
                    '--pr', '3', '--note', 'done', '--next-action', 'release')
        self.ok('checkpoint', 'PP-003', '--owner', 'alice', '--phase', 'merged', '--commit', MERGED,
                '--pr', '3', '--note', 'actual merged version', '--next-action', 'release')

    def test_release_preserves_last_handoff(self):
        self.claim()
        self.ok('checkpoint', 'PP-003', '--owner', 'alice', '--phase', 'implemented', '--commit', CODE,
                '--note', 'tests passed', '--next-action', 'review')
        self.ok('release', 'PP-003', '--owner', 'alice', '--reason', 'paused; branch saved')
        saved = self.store.session()
        self.assertIsNone(saved['active'])
        self.assertEqual(saved['last']['checkpoint']['next_action'], 'review')

    def test_api_access_failure_does_not_report_success(self):
        self.store.fail_code = 403
        result = self.invoke('resume')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('fixture-token', result.stdout + result.stderr)

    def test_offline_check_accepts_valid_repository(self):
        self.ok('check', '--offline')

    def test_offline_check_rejects_broken_link(self):
        (self.root/'progress/SUMMARY.md').write_text('[broken](absent.md)')
        result = self.invoke('check', '--offline')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('absent.md', result.stdout + result.stderr)

    def test_offline_check_rejects_duplicate_task_id(self):
        with (self.root/'progress/TASKS.md').open('a') as file:
            file.write('\n| PP-003 | 待做 | duplicate |\n')
        self.assertNotEqual(self.invoke('check', '--offline').returncode, 0)

    def test_offline_check_rejects_invalid_json(self):
        (self.root/'progress/SESSION.json').write_text('{"active": NaN}')
        self.assertNotEqual(self.invoke('check', '--offline').returncode, 0)

    def test_offline_check_rejects_unknown_state_task(self):
        (self.root/'progress/SESSION.json').write_text(json.dumps({'schema_version': 1, 'active':
            {'task_id': 'PP-999', 'owner': 'alice'}, 'last': None}))
        self.assertNotEqual(self.invoke('check', '--offline').returncode, 0)

    def test_remote_check_accepts_actual_release_contract(self):
        self.ok('check', '--remote')

    def test_remote_check_rejects_unmerged_or_wrong_revision(self):
        self.store.pr['merged'] = False
        self.assertNotEqual(self.invoke('check', '--remote').returncode, 0)
        self.store.pr.update(merged=True, merge_commit_sha=CODE)
        self.assertNotEqual(self.invoke('check', '--remote').returncode, 0)

    def test_remote_check_rejects_missing_pending_failed_checks(self):
        for checks in [[], [{'name': 'backend', 'status': 'in_progress', 'conclusion': None}],
                       [{'name': name, 'status': 'completed', 'conclusion': 'failure'} for name in ['backend','frontend']]]:
            self.store.checks = checks
            self.assertNotEqual(self.invoke('check', '--remote').returncode, 0)


if __name__ == '__main__':
    unittest.main()
