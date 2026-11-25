# Force Landscape - All Apps v2.23.5-test1

[ZIP indir / Download ZIP](https://github.com/forcelandscape/ForceLandscape-AllApps/releases/download/v2.23.5-test1/ForceLandscape-AllApps-v2.23.5-test1.zip)

## Türkçe

**Bu bir deneme sürümüdür; son değişiklikler Xiaomi Pad 6 / MIUI 14 üzerinde henüz doğrulanmadı.** Kurulumdan önce modül ve sistem ayarlarınızın yedeğini saklayın. Mevcut rapor v2.23.3 içindir, bu sürümün cihaz testi değildir. Bazı MIUI mailbox, uygulama bazlı geri alma ve önceki sistem değerlerini koruma senaryoları halen açıktır.

- Toplu seçimler tekli işlem yoluyla bağımsız süreçlerde uygulanır ve başarısız paketler bildirilir.
- Yedek girdisi hazırlık öncesinde okunur; boş/geçersiz yedek reddedilir ve kısmi hatalar bildirilir.
- İzleyici kapatma isteğini döngüde yeniden okur; PID dosyası başka izleyiciye aitse silinmez.
- Compat MEDIUM ID, paket listesindeki birebir eşleşme, XML özniteliklerinin korunması ve hata bildirimi iyileştirildi.
- SukiSU / KernelSU uyumlu `updateJson` adresi eklendi. Önceki kurulu modülünüzde bu adres yoksa otomatik güncelleme görünmez; bu ZIP bir kez yerel yüklenmelidir. Kurulumdan sonra yeniden başlatın.

13 host regresyon testi, shell ve JavaScript sözdizimi kontrolleri geçti. Gerçek cihazda kurulum, WebUI ve yeniden başlatma testi hâlâ gereklidir. Güncelleme eski ayarları korumayı hedefler; tam ve güvenli geri alma henüz garanti edilemez.

## English

**This is a test release; the latest changes have not yet been verified on the Xiaomi Pad 6 / MIUI 14.** Keep backups of module data and system settings before installation. The existing device report covers v2.23.3, not this build. Some MIUI mailbox, per-app rollback, and preservation-of-prior-state scenarios remain unresolved.

- Bulk selection uses isolated single-package operations and reports failures.
- Backup input is read before initialization; invalid or empty backups are rejected and partial failures are reported.
- The watcher checks the stop setting in its loop and does not delete another watcher's PID file.
- Corrected the Android 13 MEDIUM compat ID, literal package matching, preservation of unrelated XML attributes, and error reporting.
- Added an `updateJson` URL for SukiSU / KernelSU. If the installed version lacks this URL, install this ZIP locally once. Reboot after installation.

13 host regression tests and shell/JavaScript syntax checks passed. Real-device installation, WebUI and reboot testing are still required. Preservation of previous settings and complete rollback are not guaranteed yet.
