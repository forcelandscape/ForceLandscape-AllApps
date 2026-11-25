#!/bin/sh
# Host-side mock tests, not a replacement for Android/MIUI device testing.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/webui.sh" "$TMP/webui.sh"
cat > "$TMP/landscape.sh" <<'STUB'
FL_FORCE=$TEST_DIR/force; FL_NEVER=$TEST_DIR/never
fl_prepare() { touch "$FL_FORCE" "$FL_NEVER"; }
fl_log() { :; }
fl_pkg_sane() { case "$1" in ''|*[!a-zA-Z0-9_.]*|[0-9]*) return 1;; esac; }
fl_pkg_installed() { return 0; }
fl_list_add() { grep -Fxq "$2" "$1" || echo "$2" >> "$1"; }
fl_list_del() { grep -Fxv "$2" "$1" > "$1.tmp" || :; mv "$1.tmp" "$1"; }
fl_force_apply() { case "$1" in *fail*) echo 'HATA|simulated'; return 1;; esac; echo 'OK|pkg|force|test'; }
fl_revert_pkg() { [ "${2:-}" = never ] && fl_list_add "$FL_NEVER" "$1"; fl_list_del "$FL_FORCE" "$1"; echo 'OK|temiz'; }
fl_cache_update_one() { _p=clobbered; _v=clobbered; _c=999; }
STUB
export TEST_DIR="$TMP"
sh "$TMP/webui.sh" setmany force com.test.one com.test.two | grep -Fx 'OK|force|2'
grep -Fxq com.test.one "$TMP/force" && grep -Fxq com.test.two "$TMP/force"
sh "$TMP/webui.sh" setmany never com.test.one com.test.two | grep -Fx 'OK|never|2'
grep -Fxq com.test.one "$TMP/never" && grep -Fxq com.test.two "$TMP/never"
sh "$TMP/webui.sh" setmany auto com.test.one com.test.two | grep -Fx 'OK|auto|2'
[ ! -s "$TMP/never" ] && [ ! -s "$TMP/force" ]
if sh "$TMP/webui.sh" setmany force com.test.one com.test.fail > "$TMP/out"; then echo 'expected failure' >&2; exit 1; fi
grep -Fq 'HATA|force|1/2|kalan: com.test.fail' "$TMP/out"
echo 'webui bulk regression tests passed'
