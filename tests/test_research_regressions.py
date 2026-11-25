#!/usr/bin/env python3
"""Host-only regression checks; no Android commands or device files are touched.

These cover previously identified regressions with mocked system commands.
Run: python3 -m unittest discover -s tests -v
"""
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def shell(body):
    with tempfile.TemporaryDirectory() as tmp:
        script = f'''
. "$1/landscape.sh"
trap - EXIT INT TERM HUP
FL_DIR="$2"
FL_ORIENT_LIST="$2/yon.txt"
FL_ORIENT_BAK="$2/yon.bak"
fl_log() {{ :; }}
fl_evt() {{ :; }}
fl_miui_fixperm() {{ :; }}
{body}
'''
        return subprocess.run(['/bin/sh', '-c', script, 'test', str(ROOT), tmp],
                              text=True, capture_output=True, timeout=10)


class SafetyRegressions(unittest.TestCase):
    def test_package_lookup_is_literal(self):
        p = shell('printf "%s\\n" comXexampleYapp > "$FL_DIR/list"\n'
                  'if fl_list_has "$FL_DIR/list" com.example.app; then echo MATCH; else echo NO_MATCH; fi')
        self.assertEqual(p.stdout.strip(), 'NO_MATCH', p.stderr)

    def test_delete_does_not_remove_similarly_named_package(self):
        p = shell('printf "%s\\n" com.example.app comXexampleYapp > "$FL_DIR/list"\n'
                  'fl_list_del "$FL_DIR/list" com.example.app\ncat "$FL_DIR/list"')
        self.assertEqual(p.stdout.strip(), 'comXexampleYapp', p.stderr)

    def test_failed_compat_command_is_not_success(self):
        p = shell('am() { echo rejected; return 1; }\n'
                  'cmd() { echo rejected; return 1; }\n'
                  'if fl_am_cmd enable OVERRIDE_MIN_ASPECT_RATIO com.example.app; then echo ACCEPT; else echo REJECT; fi')
        self.assertTrue(p.stdout.strip().endswith('REJECT'), p.stdout + p.stderr)

    def test_successful_silent_compat_command_is_not_rejected(self):
        p = shell('am() { return 0; }\ncmd() { return 1; }\n'
                  'if fl_am_cmd enable OVERRIDE_MIN_ASPECT_RATIO com.example.app; then echo ACCEPT; else echo REJECT; fi')
        self.assertTrue(p.stdout.strip().endswith('ACCEPT'), p.stdout + p.stderr)

    def test_empty_existing_orientation_list_not_restored_from_stale_backup(self):
        p = shell(': > "$FL_ORIENT_LIST"\nprintf "com.example.app\\tdikey\\n" > "$FL_ORIENT_BAK"\n'
                  'fl_yon_restore\nwc -c < "$FL_ORIENT_LIST"')
        self.assertEqual(p.stdout.strip(), '0', p.stderr)

    def test_xml_update_preserves_existing_unrelated_attributes(self):
        p = shell('printf \'%s\\n\' \'<package_config>\' \'<package name="com.example.app" ratio="1.5" isScale="true" />\' \'</package_config>\' > "$FL_DIR/rules.xml"\n'
                  'fl_xml_upsert "$FL_DIR/rules.xml" com.example.app \'<package name="com.example.app" disable="true" />\' >/dev/null\n'
                  'cat "$FL_DIR/rules.xml"')
        self.assertIn('ratio="1.5"', p.stdout, p.stderr)
        self.assertIn('isScale="true"', p.stdout, p.stderr)

    def test_clean_removes_all_invalid_entries(self):
        p = shell('FL_FORCE="$FL_DIR/force"; FL_NEVER="$FL_DIR/never"; FL_APPMODE="$FL_DIR/appmode"\n'
                  'FL_MB_LIST="$FL_DIR/mailbox"; FL_ORIENT_LIST="$FL_DIR/yon"\n'
                  'printf "0\\n" > "$FL_FORCE"\nfl_lists_clean\ncat "$FL_FORCE"')
        self.assertEqual(p.stdout.strip(), '', p.stderr)

    def test_xml_update_rejects_duplicate_package_without_modification(self):
        p = shell('printf \'%s\\n\' \'<root>\' \'<package name="com.example.app" a="1" />\' \'<package name="com.example.app" a="2" />\' \'</root>\' > "$FL_DIR/rules.xml"\n'
                  'fl_xml_upsert "$FL_DIR/rules.xml" com.example.app \'<package name="com.example.app" disable="true" />\'\ncat "$FL_DIR/rules.xml"')
        self.assertIn('fail|xml-formati', p.stdout)
        self.assertIn('a="1"', p.stdout)
        self.assertIn('a="2"', p.stdout)
        self.assertNotIn('disable="true"', p.stdout)

    def test_appmode_clear_reports_partial_failure(self):
        p = shell('FL_AM_LIST="OVERRIDE_MIN_ASPECT_RATIO"\n'
                  'fl_am_cmd() { return 1; }\n'
                  'if fl_appmode_clear com.example.app; then echo ACCEPT; else echo REJECT; fi')
        self.assertIn('kismi|', p.stdout)
        self.assertTrue(p.stdout.strip().endswith('REJECT'), p.stdout + p.stderr)

    def test_medium_compat_id_matches_aosp13(self):
        p = shell('fl_id_num OVERRIDE_MIN_ASPECT_RATIO_MEDIUM')
        self.assertEqual(p.stdout.strip(), '180326845', p.stderr)


if __name__ == '__main__':
    unittest.main()
