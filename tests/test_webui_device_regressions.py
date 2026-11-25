#!/usr/bin/env python3
"""Host-side WebUI regression tests with a stubbed Android backend."""
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

STUB = r'''
FL_DIR="$MODDIR/data"
mkdir -p "$FL_DIR"
FL_FORCE="$FL_DIR/force"; FL_NEVER="$FL_DIR/never"; FL_APPMODE="$FL_DIR/appmode"
FL_ORIENT_LIST="$FL_DIR/orient"; FL_MB_LIST="$FL_DIR/mailbox"; FL_CFG="$FL_DIR/config"
FL_TAB="$(printf '\t')"
fl_prepare() { cat >/dev/null; }
fl_log() { :; }
fl_pkg_installed() { return 0; }
fl_list_add() { printf '%s\n' "$2" >> "$1"; _v=corrupt; _p=corrupt; _c=999; }
fl_list_del() { :; }
fl_force_apply() { echo "$1" >> "$FL_DIR/applied"; echo 'OK|pkg|force|done'; }
fl_cache_update_one() { _p=corrupt; _v=corrupt; }
fl_revert_pkg() { echo "OK|clean|done"; }
fl_count() { grep -c . "$1" 2>/dev/null || :; }
fl_appmode_count() { fl_count "$FL_APPMODE"; }
fl_apps_cache_build() { :; }
'''

class WebuiDeviceRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        (self.root / 'webui.sh').write_text((ROOT / 'webui.sh').read_text())
        (self.root / 'landscape.sh').write_text(STUB)
        (self.root / 'data').mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def run_webui(self, *args, input=''):
        return subprocess.run(['/bin/sh', str(self.root / 'webui.sh'), *args], input=input,
                              capture_output=True, text=True, timeout=10)

    def test_setmany_calls_isolated_single_selection_for_each_package(self):
        p = self.run_webui('setmany', 'force', 'com.first.app', 'com.second.app')
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn('OK|force|2', p.stdout)
        self.assertEqual((self.root / 'data/applied').read_text().splitlines(),
                         ['com.first.app', 'com.second.app'])

    def test_backup_pipe_captured_before_prepare_consumes_stdin(self):
        p = self.run_webui('restore-backup', input='#FORCE_LANDSCAPE_BACKUP|v2\nforce|com.first.app\n')
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual((self.root / 'data/applied').read_text().strip(), 'com.first.app')

    def test_invalid_backup_does_not_clear_existing_lists(self):
        f = self.root / 'data/force'
        f.write_text('com.existing.app\n')
        for text in ('', '#FORCE_LANDSCAPE_BACKUP|v2\n#mod|$(bad)\n', 'not a backup\n'):
            p = self.run_webui('restore-backup', input=text)
            self.assertNotEqual(p.returncode, 0, p.stdout)
            self.assertEqual(f.read_text(), 'com.existing.app\n')

if __name__ == '__main__':
    unittest.main()
