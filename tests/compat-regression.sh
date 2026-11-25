#!/bin/sh
# Mock Android commands; exercises real functions without touching /data.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
export ROOT TMP
sh <<'TEST'
. "$ROOT/landscape.sh"
trap - EXIT INT TERM HUP
fl_log() { :; }
fl_evt() { :; }
# A nonzero process must never be accepted even if its output looks positive.
am() { echo 'success'; return 1; }
cmd() { echo 'success'; return 1; }
if fl_am_cmd enable OVERRIDE_MIN_ASPECT_RATIO com.test.app >/dev/null; then
    echo 'nonzero compat command accepted' >&2; exit 1
fi
[ "$(fl_id_num OVERRIDE_MIN_ASPECT_RATIO_MEDIUM)" = 180326845 ]
getprop() { echo 33; }
fl_am_cmd() { echo "$1 $2 $3" >> "$TMP/commands"; case "$2" in OVERRIDE_MIN_ASPECT_RATIO_LARGE) return 1;; esac; }
if fl_appmode_clear com.test.app > "$TMP/result"; then echo 'partial reset accepted' >&2; exit 1; fi
grep -q '^kismi|' "$TMP/result"
grep -q '^reset OVERRIDE_MIN_ASPECT_RATIO_PORTRAIT_ONLY com.test.app$' "$TMP/commands"
if grep -q 'OVERRIDE_ANY_ORIENTATION_TO_USER' "$TMP/commands"; then echo 'Android 14 flag used on Android 13' >&2; exit 1; fi
if grep -q '^enable ' "$TMP/commands"; then echo 'clear enabled an override' >&2; exit 1; fi
TEST
echo 'compat regression tests passed'
