#!/system/bin/sh
# Modul kaldirilirken tum degisiklikleri geri alir.

MODDIR=${0%/*}
[ -f "$MODDIR/landscape.sh" ] || MODDIR=/data/adb/modules/force_landscape_all
. "$MODDIR/landscape.sh"

fl_log "uninstall.sh calisti: tum degisiklikler geri aliniyor"
fl_restore

# Eski yedegi tum dosyaya geri yuklemek, kurulum sonrasi diger
# kaynaklarin yazdigi override'lari siler. Mevcut dosyayi koru.
XML=/data/misc/appcompat/compat_framework_overrides.xml
echo " compat XML toplu yedekten geri yuklenmedi; mevcut dosya korundu: $XML"
# v2.8: MIUI orta-pencere prop'unu fabrika degerine dondur
# (modul kaldirildiktan sonra "ortada kalan uygulama" davranisi geri gelmesin
#  diye DEGIL; kullanici modulu kaldirinca sistem eski haline donsun diye)
RP=""
for b in /data/adb/ksu/bin/resetprop /data/adb/magisk/resetprop /data/adb/ap/bin/resetprop; do
    [ -x "$b" ] && { RP=$b; break; }
done
[ -n "$RP" ] && "$RP" -n ro.config.miui_activity_embedding_enable true >/dev/null 2>&1
echo " MIUI orta-pencere anahtari geri alindi (true)"

# v2.11: MIUI mailbox / yatay kural satirlarini temizle (ROM kurallari kalir)
if [ -f "$FL_MB_LIST" ]; then
    _un=$(grep -c . "$FL_MB_LIST" 2>/dev/null)
    for _up in $(cat "$FL_MB_LIST" 2>/dev/null); do
        [ -n "$_up" ] || continue
        fl_miui_clear "$_up"
    done
    echo " MIUI mailbox/yatay kural satirlari silindi (${_un:-0})"
fi
rm -f /sdcard/force_landscape_rapor.txt 2>/dev/null
rm -rf "$FL_DIR" 2>/dev/null
exit 0
