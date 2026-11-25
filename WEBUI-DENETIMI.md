# WebUI incelemesi — çalışma notları

Bu bir ilk düzeltme turudur, bütün işlevlerin MIUI 14'te çalıştığına dair
cihaz testi veya garanti değildir. Bu değişiklikler henüz yayınlanan ZIP'te yoktur.

## Düzeltilen bulgular

- Toplu seçim tekli seçimden farklı geri alma davranışına sahipti ve kabuk
  fonksiyonlarının global değişkenleri döngü sayaçlarını bozabiliyordu. Artık
  her paket için tekli seçim yolunu ayrı süreçte çalıştırır; kısmi hata bildirilir.
- Hata koduyla biten WebUI komutları çıktı içeriyorsa hata yutulabiliyordu;
  rapor niteliğindeki `SONUC` çıktıları korunarak hata kodu iletilir. Bazı
  butonlardaki koşulsuz başarı mesajları düzeltildi.
- Compat komutu hata koduyla dönse bile olumlu metin içeriyorsa başarılı
  sayılıyordu. Çıkış kodu da kontrol edilir.
- Ekrana yayma kapatılırken PORTRAIT_ONLY zorla açılıyordu; artık Android
  `reset` ile varsayılan davranışa dönülür. Kısmi sıfırlama hata olarak
  gösterilir. Bu, daha önce başka araçla atanmış override'ları geri getirmez.
- Android 13 MEDIUM change ID'si LARGE ile aynı yazılmıştı; 180326845 olarak
  düzeltildi. Uygulama başlatma/durdurma komutunun hata kodu ve duraklatmada
  PID sahipliği de kontrol edilir.

## Kaynaklar

- Android 13 compat değişiklikleri ve ID'leri: https://developer.android.com/about/versions/13/reference/compat-framework-changes
- Android `am compat reset` semantiği: https://developer.android.com/guide/app-compatibility/test-debug
- KernelSU WebUI bridge API: https://github.com/tiann/KernelSU/blob/main/js/README.md

## Doğrulanması gerekenler

- Gerçek MIUI 14 / Android 13 cihazında `cmd miui_embedding_window` komutlarının,
  XML'lerin ve yeniden başlatma sonrası etkilerinin ROM'a özel testi gerekir.
- Tüm geri alma yolları önceden var olan başka araçlara ait compat/MIUI
  override'larını eksiksiz koruyacak şekilde kanıtlanmış değildir. Özellikle
  toplu geri alma ve `fl_restore` kapsamı ayrıca gözden geçirilmelidir.
- Global ignore-orientation ayarı uygulama başına dikey seçimlerle çatışabilir;
  farklı uygulamalar ve yön değişimleriyle gerçek cihazda test edilmelidir.
- Testler: `tests/webui-regression.sh`, `tests/compat-regression.sh`,
  `node tests/webui-bridge.test.js`. Bunlar Android/MIUI cihaz testi değildir.
