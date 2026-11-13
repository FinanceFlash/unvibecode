"""Regression tests for FinanceFlash/unvibecode#781.

The hosted job id must be printed at submit time and persisted client-side
('.unvibecode-job' in the output folder) so a run stays recoverable when the
CLI exits ungracefully (SIGKILL, power loss, SSH drop).

Fully offline: a fake API server on 127.0.0.1 stands in for the hosted
service (the CLI honors UNVIBECODE_API_URL and allows http://127.0.0.1).
The REAL unvibecode CLI from the installed package runs as a subprocess.

Usage:  python test_issue_781_job_recovery.py [path-to-site-packages]

Tests:
  1 kill_then_resume      SIGKILL mid-run, then `resume <saved id>` must succeed
  2 graceful_completion   normal completion still works
  3 readonly_output       unwritable output dir must not kill a submitted run
  4 repeated_reviews      second review into same output: marker = latest job

Exit 0 = all tests pass (fixed CLI). Exit 1 = bug present (unpatched 0.4.0
fails test 1: the id is neither printed nor persisted, so nothing can resume).
"""
import io, json, os, re, signal, stat, subprocess, sys, tempfile, threading, time, zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer

REPORT_NAME = 'repo-unvibecode-full.html'

class State:
    def __init__(self, mode):
        self.mode = mode            # 'hang' (never completes) or 'complete'
        self.job_seq = 0
        self.submit_event = threading.Event()
        self.poll_event = threading.Event()
        self.lock = threading.Lock()

def make_handler(state):
    class FakeAPI(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _json(self, obj, code=200):
            b = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(b)))
            self.end_headers(); self.wfile.write(b)
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0); self.rfile.read(n)
            if self.path == '/analysis/jobs':
                with state.lock:
                    state.job_seq += 1
                    job = format(state.job_seq, '032x')
                state.submit_event.set()
                self._json({'job_id': job}); return
            self._json({'error': 'not found'}, 404)
        def do_GET(self):
            if re.fullmatch(r'/analysis/jobs/[0-9a-f]{32}', self.path.split('?')[0]):
                state.poll_event.set()
                if state.mode == 'complete':
                    self._json({'status': 'completed', 'exit_code': 0, 'has_more': False,
                                'presentation': [{'id': 1, 'kind': 'print',
                                                  'text': 'Review summary complete.', 'final': True}]})
                else:
                    self._json({'status': 'running', 'has_more': True,
                                'presentation': [{'id': 1, 'kind': 'print',
                                                  'text': 'Business analysis running: 0 of 1 code areas reviewed'}]})
                return
            if self.path.split('?')[0].endswith('/download'):
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, 'w') as z:
                    z.writestr(f'repo-unvibecode-analysis-20261114_000000/{REPORT_NAME}', '<html>full report</html>')
                b = buf.getvalue()
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Length', str(len(b)))
                self.end_headers(); self.wfile.write(b); return
            self._json({'error': 'not found'}, 404)
    return FakeAPI

class Harness:
    def __init__(self, site, mode):
        self.state = State(mode)
        self.server = HTTPServer(('127.0.0.1', 0), make_handler(self.state))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = os.path.join(self.tmp.name, 'repo'); os.makedirs(self.repo)
        open(os.path.join(self.repo, 'a.py'), 'w').write('def a():\n    return 1\n')
        self.env = dict(os.environ,
                        UNVIBECODE_API_URL=f'http://127.0.0.1:{self.server.server_address[1]}/analysis')
        if site: self.env['PYTHONPATH'] = site
    def run_cli(self, argv):
        return subprocess.Popen([sys.executable, '-m', 'unvibecode'] + argv,
                                env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    def review(self, out):
        return self.run_cli(['review', '--repository', self.repo, '--output', out, '--no-open-browser'])
    def resume(self, job, out):
        return self.run_cli(['resume', job, '--output', out, '--no-open-browser'])
    def close(self):
        self.server.shutdown(); self.server.server_close(); self.tmp.cleanup()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()

def wait_kill(proc):
    """Bounded communicate; on timeout kill and re-collect. Returns (rc, output)."""
    try:
        out, _ = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill(); out, _ = proc.communicate(timeout=10)
    return proc.returncode, out

def marker_value(out_dir):
    p = os.path.join(out_dir, '.unvibecode-job')
    return open(p).read().strip() if os.path.exists(p) else None

def report_downloaded(out_dir):
    for root, _, files in os.walk(out_dir):
        if REPORT_NAME in files: return True
    return False

results = []
def check(name, ok, detail):
    results.append((name, ok))
    print(f'{name}: {"PASS" if ok else "FAIL"} ({detail})')

def test_kill_then_resume(site):
    with Harness(site, 'hang') as h:
        out_dir = os.path.join(h.tmp.name, 'out')
        proc = h.review(out_dir)
        try:
            if not h.state.submit_event.wait(15):
                check('kill_then_resume', False, 'CLI never submitted'); return
            if not h.state.poll_event.wait(15):
                check('kill_then_resume', False, 'CLI never started polling'); return
            if proc.poll() is not None:
                check('kill_then_resume', False, f'CLI exited early rc={proc.returncode}'); return
            proc.send_signal(signal.SIGKILL)   # ungraceful termination
            rc, out = wait_kill(proc)
        finally:
            if proc.poll() is None: proc.kill()
        job1 = format(1, '032x')
        exact_line = f'Job started: {job1} - resume with: unvibecode resume {job1}'
        printed = exact_line in out
        saved = marker_value(out_dir)
        if not (printed and saved == job1):
            check('kill_then_resume', False,
                  f'after SIGKILL: exact resume line printed={printed}, marker={saved!r}; nothing left to resume with')
            return
        # Recover using the saved id against the (now completing) service.
        h.state.mode = 'complete'
        rproc = h.resume(saved, out_dir)
        rrc, rout = wait_kill(rproc)
        ok = rrc == 0 and report_downloaded(out_dir)
        check('kill_then_resume', ok,
              f'SIGKILL rc={rc}; id printed+persisted; resume <saved id> rc={rrc}, report downloaded={report_downloaded(out_dir)}')

def test_graceful_completion(site):
    with Harness(site, 'complete') as h:
        out_dir = os.path.join(h.tmp.name, 'out')
        proc = h.review(out_dir)
        rc, out = wait_kill(proc)
        job1 = format(1, '032x')
        ok = rc == 0 and report_downloaded(out_dir)
        check('graceful_completion', ok,
              f'rc={rc}, report downloaded={report_downloaded(out_dir)}, '
              f'resume line printed={f"unvibecode resume {job1}" in out}, marker={marker_value(out_dir)!r}')

def test_readonly_output(site):
    with Harness(site, 'hang') as h:
        parent = os.path.join(h.tmp.name, 'locked'); os.makedirs(parent)
        os.chmod(parent, stat.S_IRUSR | stat.S_IXUSR)  # read+execute only
        out_dir = os.path.join(parent, 'out')
        proc = h.review(out_dir)
        try:
            if not h.state.submit_event.wait(15):
                check('readonly_output', False, 'CLI never submitted'); return
            if not h.state.poll_event.wait(15):
                # polling starts AFTER the patched print/persist block; no poll = it died there
                rc, out = wait_kill(proc)
                check('readonly_output', False,
                      f'CLI died after successful remote submit when output was unwritable (rc={rc})')
                return
            alive = proc.poll() is None
            proc.send_signal(signal.SIGKILL)
            rc, out = wait_kill(proc)
        finally:
            if proc.poll() is None: proc.kill()
            os.chmod(parent, stat.S_IRWXU)
        job1 = format(1, '032x')
        printed = f'Job started: {job1} - resume with: unvibecode resume {job1}' in out
        warned = 'Warning: could not save the job id' in out
        ok = alive and printed and warned and marker_value(out_dir) is None
        check('readonly_output', ok,
              f'still polling after failed persist={alive}, exact resume line printed={printed}, '
              f'warning shown={warned}, marker absent={marker_value(out_dir) is None}')

def test_repeated_reviews(site):
    with Harness(site, 'complete') as h:
        out_dir = os.path.join(h.tmp.name, 'out')
        rc1, _ = wait_kill(h.review(out_dir))
        proc2 = h.review(out_dir)
        rc2, out2 = wait_kill(proc2)
        job2 = format(2, '032x')
        saved = marker_value(out_dir)
        # Second review submits fine (marker = newest job) but stops at download:
        # the report folder from run 1 already exists (pre-existing 0.4.0 collision rule).
        stopped_on_collision = 'This report folder already exists' in out2
        ok = rc1 == 0 and saved == job2 and stopped_on_collision
        check('repeated_reviews', ok,
              f'run1 rc={rc1}; run2 marker={saved!r} (latest job), run2 stopped on pre-existing '
              f'report folder={stopped_on_collision} (unchanged 0.4.0 collision rule)')

def main():
    site = sys.argv[1] if len(sys.argv) > 1 else None
    test_kill_then_resume(site)
    test_graceful_completion(site)
    test_readonly_output(site)
    test_repeated_reviews(site)
    failed = [n for n, ok in results if not ok]
    print('SUMMARY:', 'ALL PASS' if not failed else f'FAILED: {", ".join(failed)}')
    return 0 if not failed else 1

if __name__ == '__main__':
    sys.exit(main())
