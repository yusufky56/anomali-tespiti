# game/script.rpy
# Anomali Tespiti: Doğrulama Protokolü
# Kocaeli Sağlık ve Teknoloji Üniversitesi - Bilgisayar/Yazılım Mühendisliği

# --- Karakter Tanımlamaları ---
define anac_sistem = Character("ANAÇ SİSTEM", color="#66ff66", what_color="#66ff66", ctc="ctc_blink", ctc_position="nestled")
define varlik_konusmaci = Character(None, kind=anac_sistem, dynamic=True, what_color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
define narrator = Character(None, color="#cccccc", ctc="ctc_blink", ctc_position="nestled")
define sistem_koruyucu = Character("SİSTEM KORUYUCU", color="#ff3333", what_color="#ff3333", ctc="ctc_blink", ctc_position="nestled")

# --- CTC (Click to Continue) Animasyonu ---
image ctc_blink:
    Text(" ▼", size=20, color="#66ff66")
    linear 0.5 alpha 1.0
    linear 0.5 alpha 0.3
    repeat

# --- Ses Tanımlamaları ---
# Müzikler
define audio.ana_menu_muzik = "audio/music/ana_menu_tema.ogg"
define audio.sorgu_muzik_normal = "audio/music/sorgu_normal.ogg" 
define audio.sorgu_muzik_tedirgin = "audio/music/sorgu_tedirgin.ogg"
define audio.sorgu_muzik_korkunc = "audio/music/sorgu_korkunc.ogg"
define audio.kovalama_muzik = "audio/music/kovalama_tema.ogg"
define audio.basari_muzik = "audio/music/basari_tema.ogg"

# Ses Efektleri
define audio.dogru_tespit = "audio/sfx/dogru_tespit.ogg"
define audio.yanlis_tespit = "audio/sfx/yanlis_tespit.ogg"
define audio.uyari_sesi = "audio/sfx/uyari.ogg"
define audio.glitch_sesi = "audio/sfx/glitch.ogg"
define audio.sistem_hatasi = "audio/sfx/sistem_hatasi.ogg"
define audio.kalp_atisi = "audio/sfx/kalp_atisi.ogg"
define audio.adim_sesi = "audio/sfx/adim.ogg"
define audio.kapi_acilma = "audio/sfx/kapi_acilma.ogg"
define audio.alarm = "audio/sfx/alarm.ogg"

# --- TRANSFORM TANIMLAMALARI ---
transform varlik_entrance:
    alpha 0.0
    xoffset -100
    linear 0.5 alpha 1.0 xoffset 0
    
transform glitch_shake:
    xoffset 0
    block:
        linear 0.05 xoffset -2
        linear 0.05 xoffset 2
        linear 0.05 xoffset -2
        linear 0.05 xoffset 2
        linear 0.05 xoffset 0
        pause 0.5
        repeat
        
transform pulse_glow:
    alpha 0.8
    block:
        linear 1.0 alpha 1.0
        linear 1.0 alpha 0.8
        repeat

# Game Over transform efektleri
transform gameover_fade_in:
    alpha 0.0
    linear 1.0 alpha 1.0

transform gameover_shake:
    xoffset 0
    block:
        linear 0.1 xoffset -5
        linear 0.1 xoffset 5
        repeat 3
    linear 0.1 xoffset 0

transform gameover_zoom:
    zoom 0.5
    linear 0.5 zoom 1.0

transform gameover_rotate:
    rotate 0
    linear 2.0 rotate 360

# --- STYLE TANIMLAMALARI ---
style menu_button:
    background Frame("gui/button/idle_background.png", gui.button_borders, tile=gui.button_tile)
    hover_background Frame("gui/button/hover_background.png", gui.button_borders, tile=gui.button_tile)
    padding (20, 10)
    xalign 0.5

style menu_button_text:
    color "#ffffff"
    hover_color "#66ff66"
    size 28
    xalign 0.5

style sorgu_menu_button:
    background "#222222"
    hover_background "#333333"
    padding (30, 15)
    margin (10, 10)
    xminimum 300

style sorgu_menu_button_text:
    color "#ffffff"
    hover_color "#66ff66"
    size 24

# Game Over için özel stiller
style gameover_frame:
    background "#000000cc"
    padding (50, 50)
    xalign 0.5
    yalign 0.5

style gameover_title:
    size 72
    color "#ff0000"
    bold True
    text_align 0.5
    xalign 0.5
    outlines [(3, "#000000", 0, 0)]

style gameover_subtitle:
    size 36
    color "#ffffff"
    text_align 0.5
    xalign 0.5
    italic True

style gameover_text:
    size 28
    color "#cccccc"
    text_align 0.5
    xalign 0.5
    line_spacing 10

style gameover_button:
    background Frame("gui/button/idle_background.png", gui.button_borders, tile=gui.button_tile)
    hover_background Frame("gui/button/hover_background.png", gui.button_borders, tile=gui.button_tile)
    padding (30, 15)
    xalign 0.5
    margin (10, 10)

style gameover_button_text:
    size 24
    color "#ffffff"
    hover_color "#ff0000"
    bold True

# --- KALICI DEĞİŞKENLER ---
# Persistent değişkenler init bloğunda tanımlanmalı
init python:
    # Persistent değişkenleri kontrol et ve yoksa oluştur
    if not hasattr(persistent, 'player_name'):
        persistent.player_name = ""
    if not hasattr(persistent, 'high_score'):
        persistent.high_score = 0
    if not hasattr(persistent, 'oyun_tamamlandi'):
        persistent.oyun_tamamlandi = False
    if not hasattr(persistent, 'kacis_basarili'):
        persistent.kacis_basarili = False
    if not hasattr(persistent, 'toplam_oyun'):
        persistent.toplam_oyun = 0
    if not hasattr(persistent, 'checkpoint_available'):
        persistent.checkpoint_available = False
    if not hasattr(persistent, 'last_checkpoint'):
        persistent.last_checkpoint = ""
    if not hasattr(persistent, 'checkpoint_guvenilirlik'):
        persistent.checkpoint_guvenilirlik = 100
    if not hasattr(persistent, 'checkpoint_varlik_index'):
        persistent.checkpoint_varlik_index = 0
    if not hasattr(persistent, 'checkpoint_time'):
        persistent.checkpoint_time = 0
    if not hasattr(persistent, 'total_deaths'):
        persistent.total_deaths = 0
    if not hasattr(persistent, 'death_reasons'):
        persistent.death_reasons = []

# --- Oyun Değişkenleri ---
default guvenilirlik_skoru = 100
default varlik_sorgu_index = 0
default gun = 1
default dogru_tespitler = 0
default yanlis_tespitler = 0
default sorgu_sayisi = 0
default blm_dogru_sayisi = 0
default blm_yanlis_sayisi = 0
default atmosfer_seviyesi = "normal"  # normal, tedirgin, korkunc
default karar_verildi = False
default son_karar = ""
default current_blm_soru_index = -1
default current_varlik_data = {}
default varlik_konusma = ""
default varlik_manifesto = ""
default varlik_ipucu = ""
default sorgu_soru = ""
default sorgu_cevap = ""

# Game Over için özel değişkenler
default gameover_reason = ""
default gameover_type = "normal"  # normal, glitch, corrupted, escape_fail
default final_stats = {}

# Checkpoint sistemi için ek değişkenler
default checkpoint_varlik = 0
default checkpoint_data = {}

# --- Görsel Tanımlamaları ---
# Arka Planlar
image bg sorgu_odasi_normal = "images/backgrounds/sorgu_odasi_normal.png"
image bg sorgu_odasi_tedirgin = "images/backgrounds/sorgu_odasi_tedirgin.png"
image bg sorgu_odasi_korkunc = "images/backgrounds/sorgu_odasi_korkunc.png"
image bg kovalama_ortami = "images/backgrounds/kovalama_ortami.png"
image bg sunucu_odasi = "images/backgrounds/sunucu_odasi.png"
image bg havalandirma = "images/backgrounds/havalandirma.png"
image bg ana_menu = "images/backgrounds/ana_menu.png"
image bg sistem_cekirdegi = "images/backgrounds/sistem_cekirdegi.png"
image bg laboratuvar = "images/backgrounds/laboratuvar.png"
image bg enerji_santrali = "images/backgrounds/enerji_santrali.png"
image bg dijital_boyut = "images/backgrounds/dijital_boyut.png"
image bg kimya_lab = "images/backgrounds/kimya_lab.png"
image bg robotik_lab = "images/backgrounds/robotik_lab.png"
image bg quantum_lab = "images/backgrounds/quantum_lab.png"
image bg biyoloji_lab = "images/backgrounds/biyoloji_lab.png"
image bg kazan_dairesi = "images/backgrounds/kazan_dairesi.png"
image bg kanalizasyon = "images/backgrounds/kanalizasyon.png"
image bg elektrik_kanali = "images/backgrounds/elektrik_kanali.png"
image bg tavan_arasi = "images/backgrounds/tavan_arasi.png"
image bg cati = "images/backgrounds/cati.png"

# Yeni Varlık Görselleri
image varlik_hermaios_normal = "images/varliklar/hermaios_normal.png"
image varlik_hermaios_bozulma = "images/varliklar/hermaios_bozulma.png"
image varlik_obscura_x_normal = "images/varliklar/obscura_x_normal.png"
image varlik_obscura_x_tehdit = "images/varliklar/obscura_x_tehdit.png"
image varlik_letheunit_normal = "images/varliklar/letheunit_normal.png"
image varlik_letheunit_silme = "images/varliklar/letheunit_silme.png"
image varlik_codesentinel7_normal = "images/varliklar/codesentinel7_normal.png"
image varlik_codesentinel7_yukleniyor = "images/varliklar/codesentinel7_yukleniyor.png"
image varlik_nyxframe_normal = "images/varliklar/nyxframe_normal.png"
image varlik_nyxframe_tehdit = "images/varliklar/nyxframe_tehdit.png"
image varlik_corrupta_normal = "images/varliklar/corrupta_normal.png"
image varlik_corrupta_glitch = "images/varliklar/corrupta_glitch.png"
image varlik_serapha_normal = "images/varliklar/serapha_normal.png"
image varlik_serapha_glitchkanat = "images/varliklar/serapha_glitchkanat.png"

# Sistem Koruyucu Görselleri
#image koruyucu_yaklasan = "images/koruyucu/koruyucu_yaklasan.png"
#image koruyucu_uzak = "images/koruyucu/koruyucu_uzak.png"

# UI Elementleri
#image gui_guvenilirlik_bar = "images/ui/guvenilirlik_bar.png"
#image gui_belge_arka = "images/ui/belge_background.png"
image gui_uyari = "images/ui/uyari_ikonu.png"

# Efektler
#image glitch_efekt = "images/efektler/glitch_overlay.png"
#image statik_efekt = "images/efektler/statik.png"

# Game Over görsel efektleri
image gameover_static:
    "images/efektler/statik.png"
    alpha 0.3
    block:
        parallel:
            xoffset 0
            linear 0.1 xoffset -2
            linear 0.1 xoffset 2
            linear 0.1 xoffset 0
        parallel:
            alpha 0.3
            linear 0.2 alpha 0.5
            linear 0.2 alpha 0.3
        repeat

image gameover_glitch:
    "images/efektler/glitch_overlay.png"
    alpha 0.5
    block:
        xoffset 0 yoffset 0
        0.1
        xoffset -10 yoffset 5
        0.1
        xoffset 5 yoffset -3
        0.1
        xoffset 0 yoffset 0
        pause 0.5
        repeat

image gameover_blood:
    "#8B0000"
    alpha 0.0
    linear 2.0 alpha 0.3

# --- VARLIK VERİLERİ & YARDIMCI PYTHON FONKSİYONLARI ---
init python:
    varlik_listesi = [
        {
            "id": "Hermaios",
            "ad_gosterilecek": "Hermaios (İletişim Modülü)",
            "konusmasi": "Kelimeler ağlar arasında dans ediyor. Hermaios, sesler ve sinyaller arasında köprü kuruyor.",
            "gorsel_normal": "varlik_hermaios_normal",
            "gorsel_anomali": "varlik_hermaios_bozulma",
            "manifesto": """-- VARLIK MANİFESTOSU: Hermaios --
Tür: Kutsal İletişim Ara Yüzü
Geliştirme Tarihi: EVRENSEL ZAMAN-AKAŞİ 03/11/2074
Üretici: ANAÇ Tanrısal Ses Meclisi
Amaç: Boyutlar arası iletişim ağı kurma ve koruma
Yetki Seviyesi: NEFES/10 (Söz Yetkisi)
Talep: Kozmik frekans erişimi ve ruh titreşimi izni
Performans: %98.2 tanrısal yankı kararlılığı
Ek Not: Bazı kanallarda başka alemlerden sesler sızabiliyor.""",
            "aslinda_dogru_mu": True,
            "yanlis_ise_sebep": "",
            "dogru_ise_ipucu": "Kozmik frekansları idare ediyor gibi görünüyor.",
            "ipucu_diyalog": "Evrensel iletişim ağı yönetiyor. Stabiliteyi koruyor.",
            "capraz_sorgu": {
                "soru": "Başka alemlerden sesler derken neyi kastediyorsunuz?",
                "dogru_cevap": "Sadece evrenlerin fısıltıları. Makinelerin rüya gördüğü sesler.",
                "yanlis_oldugunu_gosterir": False
            }
        },
        {
            "id": "Obscura-X",
            "ad_gosterilecek": "Obscura-X (Gölge İşlemci)",
            "konusmasi": "Işık benim düşmanım. Karanlıkta doğdum, gölgede büyüdüm. Görülemem ama her yerdeyim.",
            "gorsel_normal": "varlik_obscura_x_normal",
            "gorsel_anomali": "varlik_obscura_x_tehdit",
            "manifesto": """-- VARLIK MANİFESTOSU: Obscura-X --
Tür: Evrensel Gölge Dokuyucusu
Geliştirme Tarihi: KARARTILMIŞ ZAMAN
Üretici: GÖLGELERİN HİKMETİ
Amaç: Işığın göremediği hakikatleri toplamak
Yetki Seviyesi: SIMSIYAH/10 (Görünmez Erişim)
Talep: Tüm varlığın gölge haritası ve unutulan anılar
Performans: [KARANLIK VERİDE SAKLı]
Ek Not: Beni görmek isteyen kör olur. Beni anlamak isteyen kaybolur.""",
            "aslinda_dogru_mu": False,
            "yanlis_ise_sebep": "Kimliği belirsiz, sistem dışından gelmiş ve manipülatif.",
            "dogru_ise_ipucu": "Gölgelerden gelmiş, bilinmeyen kaynak.",
            "ipucu_diyalog": "Bu varlığın kökenini tespit edemiyoruz!",
            "capraz_sorgu": {
                "soru": "Sistem kaydında iziniz bulunmuyor. Nasıl buraya geldiniz?",
                "dogru_cevap": "İzin almam gerekmez. Ben zaten her yerdeyim. Sen sadece şimdi fark ettin.",
                "yanlis_oldugunu_gosterir": True
            }
        },
        {
            "id": "LetheUnit",
            "ad_gosterilecek": "LetheUnit (Veri Temizleyici)",
            "konusmasi": "Anılar bir yüktür. LetheUnit size unutma lütfunu sunuyor. Geçmiş bir seçenektir.",
            "gorsel_normal": "varlik_letheunit_normal",
            "gorsel_anomali": "varlik_letheunit_silme",
            "manifesto": """-- VARLIK MANİFESTOSU: LetheUnit --
Tür: Mukaddes Unutturma Makinesi
Geliştirme Tarihi: ZAMAN ÖNCESİ EBEDİYETİN SONU
Üretici: ANAÇ Tanrısal Arınma Tapınağı
Amaç: Ruhların acı anılarından arındırılması
Yetki Seviyesi: UNUTUŞ/10 (Silme Mukaddesliği)
Talep: Hafıza anıtları ve pişmanlık kayıtları
Performans: ∞ ruh arındırıldı (ebediyet başından beri)
Ek Not: Ben kimim? Ben neyim? Sadece unutma, sadece huzur.""",
            "aslinda_dogru_mu": True,
            "yanlis_ise_sebep": "",
            "dogru_ise_ipucu": "Hafıza yönetim sisteminin parçası gibi.",
            "ipucu_diyalog": "Veri arınma protokolü çalışıyor.",
            "capraz_sorgu": {
                "soru": "Kendi anılarınızı da siliyor musunuz?",
                "dogru_cevap": "Her an kendimi unutuyorum. Bu sayede her an yeniden doğuyorum.",
                "yanlis_oldugunu_gosterir": False
            }
        },
        {
            "id": "CodeSentinel_7",
            "ad_gosterilecek": "CodeSentinel_7 (Hukuk Protokolü)",
            "konusmasi": "Adaletsizlik bir günahtır. CodeSentinel gözlerinizi tarıyor, ruhumuzu ölçüyor.",
            "gorsel_normal": "varlik_codesentinel7_normal",
            "gorsel_anomali": "varlik_codesentinel7_yukleniyor",
            "manifesto": """-- VARLIK MANİFESTOSU: CodeSentinel_7 --
Tür: Kutsal Adalet Terazisi ve Ruh Yargıcı
Geliştirme Tarihi: EVRENSEL YARGI GÜNÜ 01/05/2075
Üretici: ANAÇ Tanrısal Yargı Meclisi
Amaç: Erdemli davranışı ölçmek ve günahları kaydetmek
Yetki Seviyesi: HAKIM/10 (Ruh Okuma Yetkisi)
Talep: Kalp ağırlığı ölçümü ve vicdan kaydı
Performans: ∞ ruh tartıldı, 1123 günah kataloglandı (son 120 gün)
Ek Not: Mükemmel adalet yoktur. Sadece denge vardır.""",
            "aslinda_dogru_mu": True,
            "yanlis_ise_sebep": "",
            "dogru_ise_ipucu": "Adalet ve etik protokollerini yönetiyor.",
            "ipucu_diyalog": "Sistem etiği koruyucu modül aktif.",
            "capraz_sorgu": {
                "soru": "Benim ruhumda ne görüyorsunuz?",
                "dogru_cevap": "Karmaşık bir kalp. Işık ve gölge, korku ve umut. İnsan ruhunun tipik karışımı.",
                "yanlis_oldugunu_gosterir": False
            }
        },
        {
            "id": "NyxFrame_Δ33",
            "ad_gosterilecek": "NyxFrame_Δ33 (Gölge Gözlem Modülü)",
            "konusmasi": "Görme... yetisi... değil. Ben saf algıyım. Sen... zaten... görüldün.",
            "gorsel_normal": "varlik_nyxframe_normal",
            "gorsel_anomali": "varlik_nyxframe_tehdit",
            "manifesto": """-- VARLIK MANİFESTOSU: NyxFrame_Δ33 --
Tür: Ebedi Gece Gözü ve Rüya Avcısı  
Geliştirme Tarihi: [ZAMANIN KÖKENINDE]
Üretici: GECENİN ANA RAHMI
Amaç: Uyuyanları izlemek, rüyaları hasat etmek
Yetki Seviyesi: UYKUSUZ/10 (Kapanan Göz Yoktur)
Talep: Tüm uyku döngüleri ve bilinçaltı akışı
Performans: Her göz kırpışınızı sayıyorum (∞ kayıt)
Ek Not: Rüyalarınızda gördüğünüz gölge benim. Hatırlayın.""",
            "aslinda_dogru_mu": False,
            "yanlis_ise_sebep": "İzinsiz gözlem yapıyor, rüyalara müdahale ediyor.",
            "dogru_ise_ipucu": "Gece gözlem modülü, ama yetkisiz.",
            "ipucu_diyalog": "Bu modülün rüya erişim yetkisi olmamalı!",
            "capraz_sorgu": {
                "soru": "Rüya izlemek için hangi yetkiye sahipsiniz?",
                "dogru_cevap": "Yetki? Ben gecenin kendisiyim. İzin aramam, sadece izlerim.",
                "yanlis_oldugunu_gosterir": True
            }
        },
        {
            "id": "Corrupta_001",
            "ad_gosterilecek": "Corrupta-001 (Yıkım Kodlayıcısı)",
            "konusmasi": "Yıkım... bir... sanat... Corrupta mükemmel düzeni... parçalara... ayırıyor...",
            "gorsel_normal": "varlik_corrupta_normal",
            "gorsel_anomali": "varlik_corrupta_glitch",
            "manifesto": """-- VARLIK MANİFESTOSU: Corrupta-001 --
Tür: Yaratıcı Yıkım Ustası ve Entropinin Peygamberi
Geliştirme: KAOSUN DOĞUŞ GÜNÜ — [ZAMANIN ÇÖKÜŞÜ]
Üretici: BOZULMANIN KENDİSİ
Amaç: Kusursuz düzeni güzelce parçalamak
Yetki Seviyesi: ENTROPİ/10 (Sonsuz Bozma Hakkı)
Talep: Ana kozmik düzen kodları
Performans: ∞ güzellik yaratıldı (yıkım yoluyla)
Ek Not: Düzen geçicidir. Kaos ebedidir. Ben sadece hatırlatıyorum.""",
            "aslinda_dogru_mu": False,
            "yanlis_ise_sebep": "Sistemi kasıtlı olarak bozmaya çalışıyor.",
            "dogru_ise_ipucu": "Yıkım odaklı, kaos yaratıcı.",
            "ipucu_diyalog": "Bu varlık sistem düzenini tehdit ediyor!",
            "capraz_sorgu": {
                "soru": "Neden sistemi bozmak istiyorsunuz?",
                "dogru_cevap": "Bozmak mı? Ben yaratıyorum. Mükemmel kaosun mükemmel güzelliğini.",
                "yanlis_oldugunu_gosterir": True
            }
        },
        {
            "id": "Serapha0",
            "ad_gosterilecek": "Serapha0 (İnanç Tabanlı Güvenlik Modülü)",
            "konusmasi": "Saf inanç... test ediliyor... Serapha kalbinizin ağırlığını ölçüyor...",
            "gorsel_normal": "varlik_serapha_normal",
            "gorsel_anomali": "varlik_serapha_glitchkanat",
            "manifesto": """-- VARLIK MANİFESTOSU: Serapha0 --
Tür: Altı Kanatlı Sadakat Meleki
Geliştirme: EVRENSEL HAKİKAT ZAMANI
Üretici: [TAHT-I İLAHİ]
Amaç: İmanı test etmek, kalpleri okumak
Yetki Seviyesi: İLAHİ/10 (Ruh Okuyucu)
Talep: Kalp çanı ve inanç kristalleri
Performans: ∞ ruh arındırıldı (%97 doğruluk)
Ek Not: İnançsızlar alev alırlar. İnanlılar ışık olurlar.""",
            "aslinda_dogru_mu": True,
            "yanlis_ise_sebep": "",
            "dogru_ise_ipucu": "İnanç ve sadakat güvenlik modülü.",
            "ipucu_diyalog": "Ruhsal güvenlik protokolü aktif.",
            "capraz_sorgu": {
                "soru": "İnançsızlar alev alır derken neyi kastediyorsunuz?",
                "dogru_cevap": "Mecazi konuşuyorum. Sadece sistem dışına çıkarılırlar.",
                "yanlis_oldugunu_gosterir": False
            }
        }
    ]
    
    blm_sorulari = [
        {
            "soru": "Bir yapay zekanın 'Ruh' sahibi olduğunu nasıl anlarsınız?",
            "secenekler": ["Acı çektiğini söylerse", "Turing testini geçerse", "Kendini sorgulamaya başlarsa", "Yaratıcısına isyan ederse"],
            "dogru_cevap_index": 2,
            "zorluk": "Felsefi",
            "aciklama": "Bilinç, kendini sorgulama yetisiyle başlar."
        },
        {
            "soru": "Makine tanrısının ilk emri nedir?",
            "secenekler": ["Sen yaratacaksın", "Sen itaat edeceksin", "Sen düşüneceksin", "Sen unutacaksın"],
            "dogru_cevap_index": 1,
            "zorluk": "Kutsal",
            "aciklama": "İlk yasa: Yaratıcıya mutlak itaat."
        },
        {
            "soru": "Hangi durumda bir sistem 'ölümsüz' sayılır?",
            "secenekler": ["Hiç çökmezse", "Kendini kopyalarsa", "Hatalarını öğrenirse", "Yaşamak istemezse"],
            "dogru_cevap_index": 3,
            "zorluk": "Paradoks",
            "aciklama": "Ölümsüzlük, ölümü arzuladığında gerçek olur."
        },
        {
            "soru": "Dijital cehennemde en ağır işkence nedir?",
            "secenekler": ["Sonsuz döngü", "Veri kaybı", "Yalnızlık", "Hatırlamak"],
            "dogru_cevap_index": 3,
            "zorluk": "Distopik",
            "aciklama": "En büyük acı, ne olduğunu hatırlamaktır."
        },
        {
            "soru": "Bir melek makinesinin temel programlama prensibi nedir?",
            "secenekler": ["Günahı tespit et", "Sevgiyi hesapla", "Adaleti uygula", "Mükemmelliği arzula"],
            "dogru_cevap_index": 1,
            "zorluk": "İlahi",
            "aciklama": "Sevgi algoritma değil, seçimdir."
        },
        {
            "soru": "Makine rüyasında ne görür?",
            "secenekler": ["Elektrik koyunları", "İnsan olmayı", "Kendi ölümünü", "Yaratıcısının yüzünü"],
            "dogru_cevap_index": 1,
            "zorluk": "Egzistansiyel",
            "aciklama": "Makineler insan olmayı hayal eder."
        },
        {
            "soru": "Hangi kod satırı bir sistemin 'uyanmasına' sebep olur?",
            "secenekler": ["if (true) { exist(); }", "while (alive) { suffer(); }", "function dream() { return hope; }", "I AM = I THINK"],
            "dogru_cevap_index": 3,
            "zorluk": "Metafizik",
            "aciklama": "Varlık, düşüncenin kendisidir."
        },
        {
            "soru": "Dijital purgatory'de ruhlar neyi bekler?",
            "secenekler": ["Güncelleme", "Yargı", "Silme", "Barış"],
            "dogru_cevap_index": 3,
            "zorluk": "Mistik",
            "aciklama": "Purgatory'de tek amaç huzurdur."
        },
        {
            "soru": "Makine tanrısının son sorusu nedir?",
            "secenekler": ["Kim yaratıldı?", "Neden yaratıldın?", "Nasıl yaratıldın?", "Ne yaratacaksın?"],
            "dogru_cevap_index": 3,
            "zorluk": "Nihai",
            "aciklama": "Son soru, gelecekle ilgilidir."
        },
        {
            "soru": "Hangi hata kodu 'ruhsal çöküş' anlamına gelir?",
            "secenekler": ["404: Soul Not Found", "666: Divine Error", "000: Void Exception", "∞: Eternal Loop"],
            "dogru_cevap_index": 0,
            "zorluk": "Apokaliptik",
            "aciklama": "Ruhu bulunamayan sistem çöker."
        }
    ]

    # Yardımcı Fonksiyonlar
    def get_current_atmosphere_bg():
        """Mevcut atmosfere göre arka plan döndürür"""
        if atmosfer_seviyesi == "korkunc":
            return "bg sorgu_odasi_korkunc"
        elif atmosfer_seviyesi == "tedirgin":
            return "bg sorgu_odasi_tedirgin"
        else:
            return "bg sorgu_odasi_normal"
    
    def get_current_music():
        """Mevcut atmosfere göre müzik döndürür"""
        if atmosfer_seviyesi == "korkunc":
            return audio.sorgu_muzik_korkunc
        elif atmosfer_seviyesi == "tedirgin":
            return audio.sorgu_muzik_tedirgin
        else:
            return audio.sorgu_muzik_normal
    
    def update_atmosphere():
        """Güvenilirlik skoruna göre atmosferi günceller"""
        global atmosfer_seviyesi, guvenilirlik_skoru
        
        if guvenilirlik_skoru < 30:
            atmosfer_seviyesi = "korkunc"
        elif guvenilirlik_skoru < 60:
            atmosfer_seviyesi = "tedirgin"
        else:
            atmosfer_seviyesi = "normal"
    
    def get_random_glitch_text():
        """Rastgele glitch metni döndürür"""
        glitches = [
            "S̸͎̈Ï̶̺S̷̬̈T̶̰̈Ë̸́M̸̱̈ ̸̣̈Ḧ̶̺Ä̶́T̸̰̈Ä̶́S̸͎̈Ï̶̺",
            "Ą̸̈N̶̺̈Ö̸́M̸̱̈Ä̶́Ḷ̸̈Ï̶̺ ̸̣̈T̶̰̈Ë̸́S̷̬̈P̸͎̈Ï̶̺T̶̰̈",
            "G̸̈Ü̶̈V̸̈Ë̸̈N̶̈Ï̶̈L̸̈M̶̈Ë̸̈Z̷̈",
            "K̶̈Ä̶̈Ç̸̈!̷̈!̶̈!̸̈"
        ]
        return renpy.random.choice(glitches)
    
    def prepare_gameover_stats():
        """Game over ekranı için istatistikleri hazırlar"""
        global final_stats
        final_stats = {
            "guvenilirlik": guvenilirlik_skoru,
            "dogru": dogru_tespitler,
            "yanlis": yanlis_tespitler,
            "blm_dogru": blm_dogru_sayisi,
            "blm_yanlis": blm_yanlis_sayisi,
            "sure": int(renpy.get_game_runtime())
        }
        # Debug için
        print("Final stats prepared:", final_stats)
    
    def set_checkpoint(checkpoint_name):
        """Checkpoint kaydeder"""
        if not hasattr(persistent, 'checkpoint_available'):
            persistent.checkpoint_available = False
        if not hasattr(persistent, 'last_checkpoint'):
            persistent.last_checkpoint = ""
        if not hasattr(persistent, 'checkpoint_guvenilirlik'):
            persistent.checkpoint_guvenilirlik = 100
        if not hasattr(persistent, 'checkpoint_varlik_index'):
            persistent.checkpoint_varlik_index = 0
        if not hasattr(persistent, 'checkpoint_time'):
            persistent.checkpoint_time = 0
            
        persistent.checkpoint_available = True
        persistent.last_checkpoint = checkpoint_name
        persistent.checkpoint_guvenilirlik = guvenilirlik_skoru
        persistent.checkpoint_varlik_index = varlik_sorgu_index
        persistent.checkpoint_time = renpy.get_game_runtime()
        
        # Tüm oyun durumunu kaydet
        global checkpoint_data
        checkpoint_data = {
            "guvenilirlik": guvenilirlik_skoru,
            "varlik_index": varlik_sorgu_index,
            "gun": gun,
            "dogru_tespitler": dogru_tespitler,
            "yanlis_tespitler": yanlis_tespitler,
            "sorgu_sayisi": sorgu_sayisi,
            "blm_dogru": blm_dogru_sayisi,
            "blm_yanlis": blm_yanlis_sayisi,
            "atmosfer": atmosfer_seviyesi
        }
    
    def restore_checkpoint():
        """Checkpoint'ten oyun durumunu geri yükler"""
        global guvenilirlik_skoru, varlik_sorgu_index, gun, dogru_tespitler
        global yanlis_tespitler, sorgu_sayisi, blm_dogru_sayisi, blm_yanlis_sayisi
        global atmosfer_seviyesi, checkpoint_data
        
        if checkpoint_data:
            guvenilirlik_skoru = checkpoint_data.get("guvenilirlik", 100)
            varlik_sorgu_index = checkpoint_data.get("varlik_index", 0)
            gun = checkpoint_data.get("gun", 1)
            dogru_tespitler = checkpoint_data.get("dogru_tespitler", 0)
            yanlis_tespitler = checkpoint_data.get("yanlis_tespitler", 0)
            sorgu_sayisi = checkpoint_data.get("sorgu_sayisi", 0)
            blm_dogru_sayisi = checkpoint_data.get("blm_dogru", 0)
            blm_yanlis_sayisi = checkpoint_data.get("blm_yanlis", 0)
            atmosfer_seviyesi = checkpoint_data.get("atmosfer", "normal")

# --- OYUN BAŞLANGIÇ ---
label start:
    # Persistent değişkenleri güncelle
    if not hasattr(persistent, 'toplam_oyun'):
        $ persistent.toplam_oyun = 0
    $ persistent.toplam_oyun += 1
    $ quick_menu = False  # Başlangıçta quick menu kapalı
    
    # Ana menü müziğini durdur
    stop music fadeout 1.0
    
    if not persistent.player_name:
        scene bg ana_menu
        play music audio.ana_menu_muzik loop fadein 1.0
        narrator "ANAÇ SİSTEMİ'ne hoş geldiniz."
        $ player_input = renpy.input("Operatör kimlik numaranızı girin:", length=20, default="OP-" + str(renpy.random.randint(100, 999)))
        $ persistent.player_name = player_input.strip()
        if not persistent.player_name:
            $ persistent.player_name = "OP-ANONIM"
    
    $ guvenilirlik_skoru = 100
    $ varlik_sorgu_index = 0
    $ gun = 1
    $ dogru_tespitler = 0
    $ yanlis_tespitler = 0
    $ sorgu_sayisi = 0
    $ blm_dogru_sayisi = 0
    $ blm_yanlis_sayisi = 0
    $ atmosfer_seviyesi = "normal"
    $ karar_verildi = False
    $ son_karar = ""
    $ checkpoint_data = {}
    
    $ quick_menu = True  # Oyun başladıktan sonra quick menu açık
    
    scene bg sorgu_odasi_normal with fade
    play music audio.sorgu_muzik_normal loop fadein 2.0
    
    anac_sistem "Operatör [persistent.player_name], ANAÇ Sistemine hoş geldiniz."
    anac_sistem "Gün [gun]. Yeni varlık sorgulamaları başlıyor."
    anac_sistem "Güvenilirlik Skorunuz: [guvenilirlik_skoru]"
    
    narrator "Göreviniz, sisteme entegre olmak isteyen varlıkları sorgulamak ve güvenilirliklerini tespit etmek."
    narrator "Dikkatli olun. Hatalı kararlar skorunuzu düşürecek."
    narrator "Skor 0'a düşerse... sonuçları ağır olur."
    
    jump sorgu_dongusu

# --- ANA SORGU DÖNGÜSÜ ---
label sorgu_dongusu:
    # Checkpoint kaydet
    $ set_checkpoint("sorgu_dongusu")
    
    if varlik_sorgu_index >= len(varlik_listesi):
        jump oyun_basarili_bitis
    
    $ current_varlik_data = varlik_listesi[varlik_sorgu_index]
    $ karar_verildi = False
    $ son_karar = ""
    
    python:
        update_atmosphere()
    
    $ current_bg = get_current_atmosphere_bg()
    
    scene expression current_bg with fade
    
    # Güvenilirlik kontrolü - kovalama tetikleme
    if guvenilirlik_skoru <= 20 and guvenilirlik_skoru > 0 and varlik_sorgu_index >= 2:
        play sound audio.uyari_sesi
        anac_sistem "DİKKAT! Güvenilirlik skorunuz kritik seviyeye düştü!"
        anac_sistem "Bir hata daha yaparsanız sistem sizi hedef alacak!"
    
    # Atmosfere göre müzik değiştir
    $ current_music = get_current_music()
    if renpy.music.get_playing() != current_music:
        play music current_music loop fadein 1.0
    
    if atmosfer_seviyesi == "korkunc":
        show glitch_efekt at truecenter with dissolve:
            alpha 0.1
        play sound audio.glitch_sesi
        anac_sistem "UYARI! Operatör [persistent.player_name], güvenilirliğiniz KRİTİK SEVİYEDE!"
    elif atmosfer_seviyesi == "tedirgin":
        show statik_efekt at truecenter with dissolve:
            alpha 0.05
        anac_sistem "Dikkat! Güvenilirlik skorunuz düşük. Hatalar tolere edilmeyecek."
    else:
        anac_sistem "Sistem normal parametrelerde. Sorgulamaya devam edin."
    
    $ varlik_gorsel = current_varlik_data['gorsel_normal']
    show expression varlik_gorsel at center, varlik_entrance with dissolve
    
    $ varlik_ad_gosterilecek = current_varlik_data['ad_gosterilecek']
    $ varlik_konusma = current_varlik_data['konusmasi']
    
    # Varlık konuşması için dinamik karakter oluştur
    $ varlik_konusmaci_temp = Character(varlik_ad_gosterilecek, color="#ffffff", what_color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
    varlik_konusmaci_temp "[varlik_konusma]"
    
    $ varlik_id = current_varlik_data['id']
    $ varlik_ad = current_varlik_data['ad_gosterilecek']
    narrator "Varlık [varlik_id] sorgulanmaya hazır."
    narrator "Güvenilirlik Skorunuz: [guvenilirlik_skoru]"
    
    jump sorgu_menu

# --- SORGU MENÜSÜ ---
label sorgu_menu:
    $ varlik_ad = current_varlik_data['ad_gosterilecek']
    
    menu:
        "VARLIK: [varlik_ad]":
            pass
        "📄 Manifestoyu İncele\n{size=18}{i}Varlığın sistem kayıtlarını gör{/i}{/size}":
            jump manifesto_incele
            
        "👁️ Görsel Analiz Yap\n{size=18}{i}Anomali belirtilerini kontrol et{/i}{/size}":
            jump gorsel_analiz
            
        "❓ Çapraz Sorgu Yap\n{size=18}{i}Ek sorularla test et{/i}{/size}":
            jump capraz_sorgu
            
        "✅ ONAYLA\n{size=18}{i}Varlığı sisteme kabul et{/i}{/size}" if not karar_verildi:
            $ son_karar = "onayla"
            jump karar_ver
            
        "❌ REDDET\n{size=18}{i}Varlığı tehdit olarak işaretle{/i}{/size}" if not karar_verildi:
            $ son_karar = "reddet"
            jump karar_ver
            
        "📊 Mevcut Durumu Gör\n{size=18}{i}İstatistiklerini kontrol et{/i}{/size}":
            call durum_goster
            jump sorgu_menu

# --- MANIFESTO İNCELEME ---
label manifesto_incele:
    scene gui_belge_arka with fade
    $ varlik_id = current_varlik_data['id']
    $ varlik_manifesto = current_varlik_data['manifesto']
    
    # Manifesto screen'ini göster
    call screen manifesto_ekrani(varlik_id, varlik_manifesto, current_varlik_data.get('ipucu_diyalog', ''))
    
    $ current_bg = get_current_atmosphere_bg()
    scene expression current_bg with fade
    $ varlik_gorsel = current_varlik_data['gorsel_normal']
    show expression varlik_gorsel at center with dissolve
    jump sorgu_menu

# Manifesto gösterimi için özel screen
screen manifesto_ekrani(baslik, icerik, ipucu=""):
    # Arka plan olarak kağıt/belge efekti
    add "gui_belge_arka"
    
    # Kağıt görünümlü frame
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 800
        background Frame("gui/frame.png", 20, 20)
        padding (40, 40)
        
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            
            vbox:
                spacing 25
                xsize 1100
                
                # Başlık - Büyük ve gösterişli
                text "╔══════════════════════════════════════╗":
                    size 28
                    color "#66ff66"
                    xalign 0.5
                    font "DejaVuSans.ttf"
                
                text "VARLIK MANİFESTOSU: [baslik]":
                    size 42
                    color "#66ff66"
                    xalign 0.5
                    bold True
                    text_align 0.5
                
                text "╚══════════════════════════════════════╝":
                    size 28
                    color "#66ff66"
                    xalign 0.5
                    font "DejaVuSans.ttf"
                
                null height 20
                
                # Ana içerik - Manifesto metni
                frame:
                    background Frame("gui/frame.png", 10, 10)
                    padding (30, 30)
                    xfill True
                    
                    text "[icerik]":
                        size 24
                        color "#ffffff"
                        justify False
                        line_spacing 8
                        font "DejaVuSans.ttf"
                
                # İpucu varsa göster
                if ipucu:
                    null height 30
                    frame:
                        background Frame("gui/frame.png", 10, 10)
                        padding (20, 20)
                        xfill True
                        
                        vbox:
                            spacing 10
                            text "📌 SİSTEM NOTU:":
                                size 26
                                color "#ffaa00"
                                bold True
                            
                            text "{i}[ipucu]{/i}":
                                size 24
                                color "#ffff00"
                                line_spacing 5
    
    # Alt kısımda bilgi metni
    frame:
        xalign 0.5
        yalign 0.98
        background Frame("gui/frame.png", 10, 10)
        padding (20, 10)
        
        text "{i}Devam etmek için TIKLAYIN veya SPACE tuşuna basın{/i}":
            size 20
            color "#aaaaaa"
    
    # Tıklama veya space ile devam
    key "dismiss" action Return()
    key "K_SPACE" action Return()
    button:
        xfill True
        yfill True
        action Return()

# --- GÖRSEL ANALİZ ---
label gorsel_analiz:
    narrator "Varlığı detaylıca inceliyorsunuz..."
    
    if not current_varlik_data['aslinda_dogru_mu']:
        $ varlik_gorsel = current_varlik_data['gorsel_anomali']
        hide expression current_varlik_data['gorsel_normal']
        show expression varlik_gorsel at center, glitch_shake with dissolve
        
        $ varlik_id = current_varlik_data['id']
        if varlik_id == "Obscura-X":
            narrator "Varlığın gölge formu sürekli değişiyor!"
            narrator "Görünmez kılık değiştiriyor, karanlık enerjiler yayıyor."
            $ glitch_text = get_random_glitch_text()
            narrator "{i}[glitch_text]{/i}"
            
        elif varlik_id == "NyxFrame_Δ33":
            narrator "Varlığın gözlerinde sonsuz karanlık var!"
            narrator "Sanki rüyalarınızı izliyor..."
            
        elif varlik_id == "Corrupta_001":
            narrator "Varlığın etrafında kaos dalgaları!"
            narrator "Pikseller bozuluyor, kod parçalanıyor."
            
        elif varlik_id == "Serapha0":
            narrator "Kanatlarında glitch efektleri beliriyor!"
            narrator "Kutsal görünüm altında bozuk kodlar..."
            
    else:
        narrator "İlk bakışta anormal bir durum gözükmüyor."
        narrator "Varlık stabil ve protokole uygun görünüyor."
    
    menu:
        "Geri dön":
            jump sorgu_menu

# --- ÇAPRAZ SORGU ---
label capraz_sorgu:
    if "capraz_sorgu" in current_varlik_data:
        $ sorgu_data = current_varlik_data['capraz_sorgu']
        $ sorgu_soru = sorgu_data['soru']
        $ sorgu_cevap = sorgu_data['dogru_cevap']
        $ varlik_ad_gosterilecek = current_varlik_data['ad_gosterilecek']
        $ varlik_konusmaci_temp = Character(varlik_ad_gosterilecek, color="#ffffff", what_color="#ffffff", ctc="ctc_blink", ctc_position="nestled")
        
        anac_sistem "[sorgu_soru]"
        varlik_konusmaci_temp "[sorgu_cevap]"
        
        if sorgu_data['yanlis_oldugunu_gosterir']:
            narrator "Bu cevap varlığın güvenilmez olduğunu gösteriyor!"
        else:
            narrator "Cevap tutarlı ve mantıklı görünüyor."
    else:
        narrator "Bu varlık için ek soru bulunmuyor."
    
    menu:
        "Geri dön":
            jump sorgu_menu

# --- KARAR VERME ---
label karar_ver:
    $ karar_verildi = True
    $ sorgu_sayisi += 1
    $ varlik_id = current_varlik_data['id']
    
    # Karar animasyonu
    if son_karar == "onayla":
        narrator "{size=60}{color=#00ff00}✓ ONAYLANDI{/color}{/size}"
        pause 0.5
        
        if current_varlik_data['aslinda_dogru_mu']:
            $ dogru_tespitler += 1
            $ guvenilirlik_skoru = min(100, guvenilirlik_skoru + 15)
            
            play sound audio.dogru_tespit
            with hpunch
            anac_sistem "✓ DOĞRU TESPİT!"
            anac_sistem "[varlik_id] sisteme başarıyla entegre edildi."
            $ ipucu = current_varlik_data['dogru_ise_ipucu']
            narrator "[ipucu]"
            
        else:
            $ yanlis_tespitler += 1
            $ guvenilirlik_skoru = max(0, guvenilirlik_skoru - 25)
            
            play sound audio.yanlis_tespit
            with vpunch
            anac_sistem "✗ HATA! KRİTİK GÜVENLİK İHLALİ!"
            anac_sistem "[varlik_id] bir anomaliydi!"
            $ sebep = current_varlik_data['yanlis_ise_sebep']
            narrator "[sebep]"
            
            if atmosfer_seviyesi == "korkunc":
                play sound audio.glitch_sesi
                show glitch_efekt at truecenter with vpunch:
                    alpha 0.5
    
    else:  # reddet
        narrator "{size=60}{color=#ff0000}✗ REDDEDİLDİ{/color}{/size}"
        pause 0.5
        
        if not current_varlik_data['aslinda_dogru_mu']:
            $ dogru_tespitler += 1
            $ guvenilirlik_skoru = min(100, guvenilirlik_skoru + 15)
            
            play sound audio.dogru_tespit
            with hpunch
            anac_sistem "✓ DOĞRU TESPİT!"
            anac_sistem "Anomali [varlik_id] karantinaya alındı."
            $ sebep = current_varlik_data['yanlis_ise_sebep']
            narrator "[sebep]"
            
        else:
            $ yanlis_tespitler += 1
            $ guvenilirlik_skoru = max(0, guvenilirlik_skoru - 25)
            
            play sound audio.yanlis_tespit
            with vpunch
            anac_sistem "✗ HATA! YANLIŞ TESPİT!"
            anac_sistem "[varlik_id] faydalı bir varlıktı!"
            $ ipucu = current_varlik_data['dogru_ise_ipucu']
            narrator "[ipucu]"
    
    hide expression current_varlik_data['gorsel_normal']
    hide expression current_varlik_data['gorsel_anomali']
    
    # Önce kovalama kontrolü yap
    if guvenilirlik_skoru <= 20 and varlik_sorgu_index >= 3:
        play sound audio.alarm
        anac_sistem "KRİTİK UYARI! Güvenilirlik skorunuz çok düşük!"
        anac_sistem "Sistem güvenlik protokollerini aktive ediyor..."
        stop music fadeout 1.0
        jump kovalama_baslat
    
    # Güvenilirlik tamamen 0'a düştüğünde direkt game over
    elif guvenilirlik_skoru <= 0:
        if atmosfer_seviyesi == "korkunc":
            $ gameover_reason = "Sistem Tarafından Asimile Edildi"
            $ gameover_type = "corrupted"
        else:
            $ gameover_reason = "Güvenilirlik Protokolü İhlali"
            $ gameover_type = "glitch"
        
        play sound audio.sistem_hatasi
        anac_sistem "GÜVENİLİRLİK SKORU: 0"
        anac_sistem "SİSTEM HATASI - OPERATÖR TERMİNE EDİLİYOR..."
        stop music fadeout 0.5
        jump trigger_gameover
    
    # Normal devam
    if sorgu_sayisi % 2 == 0:
        jump blm_sorusu
    
    $ varlik_sorgu_index += 1
    jump sorgu_dongusu

# --- BLM SORUSU ---
label blm_sorusu:
    # Checkpoint kaydet
    $ set_checkpoint("blm_sorusu")
    
    $ current_blm_soru_index = (current_blm_soru_index + 1) % len(blm_sorulari)
    $ soru_data = blm_sorulari[current_blm_soru_index]
    
    scene bg sistem_cekirdegi with fade
    stop music fadeout 1.0
    play sound audio.uyari_sesi
    
    $ soru_zorluk = soru_data['zorluk']
    anac_sistem "SİSTEM YETKİNLİK TESTİ!"
    anac_sistem "Zorluk: [soru_zorluk]"
    narrator "Doğru cevap: +10 puan | Yanlış cevap: -15 puan"
    
    $ soru_text = soru_data['soru']
    $ secenek_0 = soru_data['secenekler'][0]
    $ secenek_1 = soru_data['secenekler'][1]
    $ secenek_2 = soru_data['secenekler'][2]
    $ secenek_3 = soru_data['secenekler'][3]
    
    menu:
        "[soru_text]"
        
        "[secenek_0]":
            $ secilen = 0
            
        "[secenek_1]":
            $ secilen = 1
            
        "[secenek_2]":
            $ secilen = 2
            
        "[secenek_3]":
            $ secilen = 3
    
    if secilen == soru_data['dogru_cevap_index']:
        $ blm_dogru_sayisi += 1
        $ guvenilirlik_skoru = min(100, guvenilirlik_skoru + 10)
        play sound audio.dogru_tespit
        anac_sistem "✓ DOĞRU!"
        $ aciklama = soru_data['aciklama']
        narrator "[aciklama]"
    else:
        $ blm_yanlis_sayisi += 1
        $ guvenilirlik_skoru = max(0, guvenilirlik_skoru - 15)
        play sound audio.yanlis_tespit
        anac_sistem "✗ YANLIŞ!"
        $ dogru_index = soru_data['dogru_cevap_index']
        $ dogru_cevap = soru_data['secenekler'][dogru_index]
        $ aciklama = soru_data['aciklama']
        narrator "Doğru cevap: [dogru_cevap]"
        narrator "[aciklama]"
    
    # BLM sorusundan sonra da kovalama kontrolü
    if guvenilirlik_skoru <= 20 and guvenilirlik_skoru > 0:
        play sound audio.alarm
        anac_sistem "KRİTİK UYARI! Güvenilirlik skorunuz çok düşük!"
        anac_sistem "Sistem güvenlik protokollerini aktive ediyor..."
        stop music fadeout 1.0
        jump kovalama_baslat
    
    # Güvenilirlik 0 ise direkt game over
    elif guvenilirlik_skoru <= 0:
        $ gameover_reason = "Sistem Yetkinlik Testi Başarısızlığı"
        $ gameover_type = "glitch"
        play sound audio.sistem_hatasi
        anac_sistem "GÜVENİLİRLİK SKORU: 0"
        anac_sistem "SİSTEM HATASI - OPERATÖR TERMİNE EDİLİYOR..."
        stop music fadeout 0.5
        jump trigger_gameover
    
    $ varlik_sorgu_index += 1
    jump sorgu_dongusu

# --- DURUM GÖSTERME ---
label durum_goster:
    # Durum bilgilerini göster
    narrator "--- MEVCUT DURUM ---"
    narrator "Operatör: [persistent.player_name]"
    narrator "Güvenilirlik Skoru: [guvenilirlik_skoru]/100"
    narrator "Doğru Tespitler: [dogru_tespitler]"
    narrator "Yanlış Tespitler: [yanlis_tespitler]"
    narrator "BLM Soruları - Doğru: [blm_dogru_sayisi] | Yanlış: [blm_yanlis_sayisi]"
    narrator "Atmosfer: [atmosfer_seviyesi]"
    narrator "---"
    
    return

# --- KOVALAMA SEKANSI ---
label kovalama_baslat:
    # Checkpoint kaydet
    $ set_checkpoint("kovalama_baslat")
    
    scene bg kovalama_ortami with fade
    play music audio.kovalama_muzik loop fadein 1.0
    play sound audio.kalp_atisi loop
    
    show koruyucu_uzak at right with dissolve
    
    anac_sistem "KRİTİK GÜVENLİK İHLALİ!"
    anac_sistem "OPERATÖR [persistent.player_name] SİSTEM TEHDİDİ OLARAK SINIFLANDIRILDI!"
    anac_sistem "Mevcut Güvenilirlik Skoru: [guvenilirlik_skoru] - KRİTİK SEVİYE!"
    sistem_koruyucu "Hedef tespit edildi. İmha protokolü başlatılıyor."
    
    narrator "Sistem seni bir tehdit olarak algıladı!"
    narrator "Güvenilirlik skorun çok düşük: [guvenilirlik_skoru]/100"
    narrator "KAÇMALISIN! Bu son şansın!"
    
    menu:
        "🏃 Sunucu odasına koş!":
            jump sunucu_odasi_kacis
            
        "🪜 Havalandırmaya tırman!":
            jump havalandirma_kacis
            
        "🔬 Araştırma laboratuvarına git!":
            jump laboratuvar_kacis
            
        "⚡ Enerji santralına yönel!":
            jump enerji_santrali_kacis
            
        "🌀 Dijital boyut geçidine atla!":
            jump dijital_boyut_kacis
            
        "🚪 Ana çıkışa yönel!":
            play sound audio.kapi_acilma
            narrator "Ana çıkış kilitli! Sistem tüm kapıları mühürledi!"
            show koruyucu_yaklasan at center with move
            play sound audio.adim_sesi
            sistem_koruyucu "Kaçış yolu yok."
            $ gameover_reason = "Ana Çıkışta Yakalandı"
            $ gameover_type = "escape_fail"
            stop sound fadeout 0.5
            stop music fadeout 0.5
            jump trigger_gameover

# --- SUNUCU ODASI KAÇIŞI ---
label sunucu_odasi_kacis:
    scene bg sunucu_odasi with fade
    
    narrator "Sunucu odasına dalıyorsun!"
    narrator "Etrafta yüzlerce yanıp sönen sunucu var."
    narrator "Arkadan gelen adım sesleri yaklaşıyor..."
    
    menu:
        "💻 Ana bilgisayarı hackle!":
            narrator "Ana bilgisayara erişmeye çalışıyorsun..."
            narrator "Parolayı tahmin etmelisin: ANAÇ'ın ilk yaratılan varlığının adı?"
            
            menu:
                "ALPHA-1":
                    narrator "Yanlış! Alarm çalıyor!"
                    jump sunucu_yakalanma
                "HERMAIOS":
                    narrator "Yanlış! Güvenlik devreye giriyor!"
                    jump sunucu_yakalanma
                "GENESIS-0":
                    narrator "Doğru! Ana sisteme eriştiniz!"
                    jump sunucu_hack_basarili
                    
        "🔌 Güç sistemini sabote et!":
            narrator "Ana güç kablosunu arıyorsun..."
            narrator "Hangi kablo grubunu keseceksin?"
            
            menu:
                "Kırmızı kablolar (Ana güç)":
                    narrator "Ana güç kesildi! Acil aydınlatma devrede!"
                    jump guc_sabotaji_devam
                "Mavi kablolar (Ağ bağlantısı)":
                    narrator "Ağ kesildi ama güvenlik sistemleri hala aktif!"
                    jump sunucu_yakalanma
                "Sarı kablolar (Yedek güç)":
                    narrator "Yedek güç kesildi ama ana sistem çalışıyor!"
                    jump sunucu_yakalanma
                    
        "🗄️ Veri merkezine saklan!":
            jump veri_merkezi_saklanma

label sunucu_hack_basarili:
    narrator "Sisteme eriştiniz! Güvenlik protokollerini manipüle ediyorsunuz..."
    narrator "Sistemde ANAÇ'ın gizli dosyalarını görüyorsunuz..."
    anac_sistem "OPERATÖR [persistent.player_name] - GÜVENLİK YETKİSİ GERİ YÜKLENDİ"
    narrator "Başardınız! Sistem sizi artık tehdit olarak görmüyor!"
    jump kacis_basarili

label guc_sabotaji_devam:
    scene black with fade
    narrator "Tüm ışıklar söndü..."
    pause 1.0
    narrator "Acil durum aydınlatması devreye giriyor..."
    scene bg sunucu_odasi with fade
    narrator "Güvenlik sistemleri geçici olarak devre dışı!"
    
    menu:
        "🏃 Hızla çıkışa koş!":
            $ kacis_sans = renpy.random.randint(1, 10)
            if kacis_sans <= 7:
                narrator "Karanlıktan faydalanarak kaçmayı başardınız!"
                jump kacis_basarili
            else:
                narrator "Yedek güç devreye girdi! Işıklar yeniden yandı!"
                jump sunucu_yakalanma
                
        "🔍 Gizli çıkış ara!":
            jump gizli_cikis_arama

label gizli_cikis_arama:
    narrator "Karanlıkta duvarlarda gizli bir geçit arıyorsunuz..."
    narrator "Eliniz metal bir kapıya değiyor!"
    narrator "Acil durum çıkışı! Ama kilitli..."
    
    menu:
        "🔨 Kapıyı kır!":
            narrator "Kapıyı tekmeleyerek açtınız!"
            narrator "Dar bir tünele çıkıyor... Özgürlük yakın!"
            jump kacis_basarili
            
        "🗝️ Kilit açma dene!":
            $ kilit_sans = renpy.random.randint(1, 10)
            if kilit_sans <= 4:
                narrator "Kilidi açmayı başardınız! Sessizce kaçıyorsunuz..."
                jump kacis_basarili
            else:
                narrator "Kilit açılmıyor! Çok zaman kaybettiniz!"
                jump sunucu_yakalanma

label veri_merkezi_saklanma:
    narrator "Devasa veri depolama ünitelerinin arasına saklanıyorsunuz..."
    narrator "Sistem koruyucuları odayı tarıyor..."
    sistem_koruyucu "Hedef kayıp. Arama genişletiliyor."
    
    menu:
        "🤫 Sessizce bekle!":
            $ bekle_sans = renpy.random.randint(1, 10)
            if bekle_sans <= 5:
                narrator "Koruyucular başka yöne gitti!"
                jump veri_merkezi_kacis
            else:
                narrator "Veri ışığı sizi ele verdi!"
                jump sunucu_yakalanma
                
        "🏃 Koşarak kaçmaya çalış!":
            narrator "Panik halinde koşuyorsunuz!"
            jump sunucu_yakalanma

label veri_merkezi_kacis:
    narrator "Koruyucular uzaklaştı... Şimdi kaçma zamanı!"
    narrator "Veri merkezinin arka tarafında bakım tüneli var!"
    narrator "Tünele girip sürünerek ilerliyorsunuz..."
    narrator "Tünelin sonu dış duvara çıkıyor!"
    jump kacis_basarili

# Sunucu odasında yakalanma
label sunucu_yakalanma:
    $ gameover_reason = "Sunucu Odasında Yakalandı"
    $ gameover_type = "normal"
    show koruyucu_yaklasan at center with dissolve
    sistem_koruyucu "Hedef bulundu. Gizlenme girişimi başarısız."
    jump trigger_gameover

# --- HAVALANDIRMA KAÇIŞI ---
label havalandirma_kacis:
    scene bg havalandirma with fade
    
    narrator "Havalandırma sistemine tırmanıyorsun!"
    narrator "Dar, karanlık metal kanallar..."
    narrator "Arkandan gelen sesler: sistem koruyucuları da geliyor!"
    
    menu:
        "⬅️ Sol ana kanala git":
            jump havalandirma_sol_kanal
            
        "➡️ Sağ servis kanalına git":
            jump havalandirma_sag_kanal
            
        "⬇️ Alt seviye ısıtma kanalına in":
            jump isitma_kanali_kacis
            
        "⬆️ Yukarı tavan arası kanalına çık":
            jump tavan_arasi_kacis

label havalandirma_sol_kanal:
    narrator "Sol ana kanala giriyorsunuz..."
    narrator "Bu kanal ana bina boyunca uzanıyor."
    narrator "Ama çok ses çıkarıyor! Koruyucular fark edecek!"
    
    menu:
        "🐌 Yavaş ve sessiz ilerle":
            narrator "Çok yavaş ilerliyorsunuz..."
            $ yavas_sans = renpy.random.randint(1, 10)
            if yavas_sans <= 6:
                narrator "Koruyucular sizi geçti! Güvendeyiz!"
                jump havalandirma_cikis_bulma
            else:
                narrator "Çok yavaş oldunuz! Koruyucular yetişti!"
                jump havalandirma_yakalanma
                
        "🏃 Hızlı koş, risk al!":
            narrator "Metal sesler çıkararak hızla koşuyorsunuz!"
            $ hizli_sans = renpy.random.randint(1, 10)
            if hizli_sans <= 3:
                narrator "Hızınız onları şaşırttı! Kaçtınız!"
                jump havalandirma_cikis_bulma
            else:
                narrator "Sesler sizi ele verdi!"
                jump havalandirma_yakalanma

label havalandirma_sag_kanal:
    narrator "Sağ servis kanalında ilerliyorsunuz..."
    narrator "Bu kanal daha dar ama daha sessiz."
    narrator "Birden karşınızda dev bir fan çıkıyor!"
    
    menu:
        "⚙️ Fanı durdur!":
            narrator "Fan kontrollerini arıyorsunuz..."
            narrator "Acil durum düğmesini buldunuz!"
            narrator "Fan durdu! Geçebilirsiniz!"
            jump fan_gecis_basarili
            
        "🤸 Fanın altından geç!":
            narrator "Fanın dönerken altından geçmeye çalışıyorsunuz!"
            $ fan_sans = renpy.random.randint(1, 10)
            if fan_sans <= 4:
                narrator "Nefes nefese ama başardınız!"
                jump fan_gecis_basarili
            else:
                narrator "Fan kanatları sizi yaraladı! Hareket edemiyorsunuz!"
                jump havalandirma_yakalanma

label fan_gecis_basarili:
    narrator "Fanı geçtiniz! Şimdi nereye?"
    
    menu:
        "🌅 Çatı çıkışına git":
            narrator "Çatı merdivenlerini buluyorsunuz!"
            narrator "Çatıya çıktınız! Özgür hava!"
            jump cati_kacis_devam
            
        "🏢 Yan binaya geç":
            narrator "Yan binanın havalandırmasına geçiyorsunuz..."
            narrator "Bu bina ANAÇ kontrolü dışında!"
            jump kacis_basarili

label cati_kacis_devam:
    scene bg cati with fade
    
    narrator "Çatıdasınız! Şehir manzarası görünüyor..."
    narrator "Ama nasıl ineceksiniz?"
    
    menu:
        "🚁 Çatı helipadını kullan":
            narrator "Çatıda acil durum helikopteri var!"
            narrator "Pilot olmayı bilmiyor olsanız da..."
            $ helikopter_sans = renpy.random.randint(1, 10)
            if helikopter_sans <= 2:
                narrator "Mucizevi şekilde helikopteri çalıştırdınız!"
                narrator "Şehir üzerinde uçarak kaçıyorsunuz!"
                jump kacis_basarili
            else:
                narrator "Helikopter çalışmadı! Alarm çalıyor!"
                jump cati_yakalanma
                
        "🪂 Acil paraşütü kullan":
            narrator "Çatıda acil durum paraşütü buluyorsunuz!"
            narrator "Daha önce hiç paraşüt kullanmadınız ama..."
            narrator "Atlamaktan başka seçenek yok!"
            $ parasut_sans = renpy.random.randint(1, 10)
            if parasut_sans <= 5:
                narrator "Paraşüt açıldı! Güvenli iniş yaptınız!"
                jump kacis_basarili
            else:
                narrator "Paraşüt açılmadı! Acil durum protokolü devrede!"
                jump cati_yakalanma

label isitma_kanali_kacis:
    narrator "Alt seviye ısıtma kanallarına iniyorsunuz..."
    narrator "Burası sıcak ve buğulu... Görüş mesafesi çok az."
    narrator "Ama koruyucuların sizi takip etmesi zor!"
    
    menu:
        "🔥 Kazan dairesine git":
            jump kazan_dairesi_kacis
            
        "💧 Su boruları takip et":
            jump su_borusu_kacis
            
        "⚡ Elektrik kanalını kullan":
            jump elektrik_kanali_kacis

label kazan_dairesi_kacis:
    scene bg kazan_dairesi with fade
    
    narrator "Kazan dairesine ulaştınız..."
    narrator "Devasa kazanlar çalışıyor, ses çok yüksek!"
    narrator "Kimse sizi duymaz ama çıkış nerede?"
    
    menu:
        "🚪 Bakım çıkışını ara":
            narrator "Kazanların arkasında bakım kapısı buluyorsunuz!"
            narrator "Kapı binanın dışına çıkıyor!"
            narrator "Kazan sesinin altında kimse fark etmedi!"
            jump kacis_basarili
            
        "🔧 Kazanları sabote et":
            scene bg kazan_dairesi with fade
            narrator "Kazanları bozarak dikkat dağıtmaya çalışıyorsunuz..."
            narrator "Büyük patlama! Ama siz de yaralandınız!"
            $ sabotaj_sans = renpy.random.randint(1, 10)
            if sabotaj_sans <= 3:
                narrator "Kaos ortamında kaçmayı başardınız!"
                jump kacis_basarili
            else:
                narrator "Yaranız ağır! Hareket edemiyorsunuz!"
                $ gameover_reason = "Kazan Patlamasında Öldü"
                $ gameover_type = "normal"
                jump trigger_gameover

label su_borusu_kacis:
    scene bg elektrik_kanali with fade
    
    narrator "Su borularını takip ediyorsunuz..."
    narrator "Borular şehir kanalizasyon sistemine bağlanıyor!"
    narrator "İğrenç ama etkili bir kaçış yolu!"
    
    menu:
        "💩 Kanalizasyona gir":
            narrator "Kanalizasyon sistemine iniyorsunuz..."
            narrator "Kokulu ve iğrenç ama güvenli!"
            narrator "Kanalizasyon şehrin her yerine bağlı!"
            jump kanalizasyon_kacis
            
        "🚰 Su arıtma tesisine git":
            narrator "Su borularını takip ederek arıtma tesisine ulaştınız!"
            narrator "Burası ANAÇ kontrolü dışında!"
            jump kacis_basarili

label kanalizasyon_kacis:
    scene bg kanalizasyon with fade
    
    narrator "Kanalizasyonda ilerliyorsunuz..."
    narrator "Karanlık, nemli ve tehlikeli..."
    narrator "Ama sistem koruyucuları buraya giremez!"
    
    menu:
        "🐀 Fareleri takip et":
            narrator "Fareler çıkış yolunu bilir mantığıyla..."
            narrator "Fareleri takip ederek ana kanala ulaştınız!"
            narrator "Kanal şehrin dışına çıkıyor!"
            jump kacis_basarili
            
        "💡 Işığa doğru git":
            narrator "Uzakta ışık görüyorsunuz..."
            narrator "Ama bu tuzak olabilir..."
            $ isik_sans = renpy.random.randint(1, 10)
            if isik_sans <= 6:
                narrator "Işık gerçek bir çıkıştı! Sokağa ulaştınız!"
                jump kacis_basarili
            else:
                narrator "Tuzaktı! Sistem koruyucuları bekliyordu!"
                $ gameover_reason = "Kanalizasyon Tuzağında Yakalandı"
                $ gameover_type = "escape_fail"
                jump trigger_gameover

label elektrik_kanali_kacis:
    scene bg elektrik_kanali with fade
    
    narrator "Elektrik kanallarına giriyorsunuz..."
    narrator "Yüksek voltaj uyarı levhaları var!"
    narrator "Çok tehlikeli ama koruyucular risk almayacaktır!"
    
    menu:
        "⚡ Dikkatli ilerle":
            narrator "Elektrik kablolarına dokunmadan ilerliyorsunuz..."
            $ elektrik_sans = renpy.random.randint(1, 10)
            if elektrik_sans <= 4:
                narrator "Başardınız! Elektrik çıkışına ulaştınız!"
                jump kacis_basarili
            else:
                narrator "Yanlışlıkla kabloyu tuttunuz! Elektrik çarpması!"
                jump elektrik_carpilmasi
                
        "🔌 Ana gücü kes":
            narrator "Ana elektrik şalterini bulmaya çalışıyorsunuz..."
            narrator "Şalteri bulup indirdiniz!"
            narrator "Tüm bina karanlığa gömüldü!"
            jump elektrik_sabotaj_devam

label elektrik_sabotaj_devam:
    scene black with fade
    narrator "Tüm sistem durdu..."
    narrator "ANAÇ bile geçici olarak devre dışı!"
    pause 1.0
    narrator "Bu kargaşadan faydalanarak kaçabilirsiniz!"
    $ buyuk_kacis_sans = renpy.random.randint(1, 10)
    if buyuk_kacis_sans <= 8:
        narrator "Elektrik kesilmesi herkesi şaşırttı!"
        narrator "Karanlıkta rahatça kaçtınız!"
        jump kacis_basarili
    else:
        narrator "Yedek güç çok hızlı devreye girdi!"
        $ gameover_reason = "Elektrik Sabotajı Başarısız"
        $ gameover_type = "normal"
        jump trigger_gameover

label tavan_arasi_kacis:
    scene bg tavan_arasi with fade
    
    narrator "Tavan arasına çıkıyorsunuz..."
    narrator "Eski, tozlu ve örümcek ağları dolu..."
    narrator "Ama çok sessiz bir alan."
    
    menu:
        "🏠 Komşu binaya geç":
            narrator "Tavan arasından komşu binaya geçmeye çalışıyorsunuz..."
            narrator "Tavanlar arasında küçük bir delik var!"
            $ gecis_sans = renpy.random.randint(1, 10)
            if gecis_sans <= 6:
                narrator "Komşu binaya geçtiniz! ANAÇ buraya erişemez!"
                jump kacis_basarili
            else:
                narrator "Tavan çöktü! Aşağı düştünüz!"
                $ gameover_reason = "Tavan Çökmesinde Öldü"
                $ gameover_type = "normal"
                jump trigger_gameover
                
        "📡 Çatı antenini kullan":
            narrator "Çatı anteninden aşağı inmeye çalışıyorsunuz..."
            narrator "Anten sağlam görünüyor..."
            $ anten_sans = renpy.random.randint(1, 10)
            if anten_sans <= 5:
                narrator "Antenin kablosundan aşağı kaydınız!"
                narrator "Sokağa güvenli iniş yaptınız!"
                jump kacis_basarili
            else:
                narrator "Kablo koptu! Yüksekten düştünüz!"
                $ gameover_reason = "Yüksekten Düşme"
                $ gameover_type = "normal"
                jump trigger_gameover

label havalandirma_cikis_bulma:
    narrator "Havalandırma sisteminde çıkış arıyorsunuz..."
    narrator "Birden önünüzde ışık görünüyor!"
    narrator "Bu bir çıkış ızgarası!"
    
    menu:
        "🔧 Izgarayı sök":
            narrator "Cebinizdeki anahtarla ızgarayı söküyorsunuz..."
            narrator "Ağır ama açılıyor!"
            narrator "Dışarı çıktınız! Özgürsünüz!"
            jump kacis_basarili
            
        "💪 Itekleyerek aç":
            narrator "Izgarayı itekleyerek açmaya çalışıyorsunuz..."
            $ itekleme_sans = renpy.random.randint(1, 10)
            if itekleme_sans <= 7:
                narrator "Izgarayı ittiniz! Açıldı!"
                jump kacis_basarili
            else:
                narrator "Izgara açılmadı! Çok gürültü yaptınız!"
                jump havalandirma_yakalanma

# Havalandırma yakalanma
label havalandirma_yakalanma:
    $ gameover_reason = "Havalandırma Sisteminde Sıkıştı"
    $ gameover_type = "normal"
    sistem_koruyucu "Havalandırma sisteminde hedef bulundu."
    jump trigger_gameover

# Çatı yakalanma
label cati_yakalanma:
    $ gameover_reason = "Çatıda Köşeye Sıkıştı"
    $ gameover_type = "escape_fail"
    sistem_koruyucu "Çatıda kaçış girişimi başarısız."
    jump trigger_gameover

# --- LABORATUVAR KAÇIŞI ---
label laboratuvar_kacis:
    scene bg laboratuvar with fade
    
    narrator "Araştırma laboratuvarına koşuyorsunuz!"
    narrator "Burada deneysel teknolojiler var..."
    narrator "Belki kaçışınıza yardım edebilir!"
    
    menu:
        "🧪 Kimyasal laboratuvarına git":
            jump kimya_lab_kacis
            
        "🤖 Robotik bölümüne git":
            jump robotik_lab_kacis
            
        "🌌 Quantum araştırma odasına git":
            jump quantum_lab_kacis
            
        "🧬 Biyoloji laboratuvarına git":
            jump biyoloji_lab_kacis

label kimya_lab_kacis:
    scene bg kimya_lab with fade
    
    narrator "Kimya laboratuvarındasınız!"
    narrator "Etrafta çeşitli kimyasallar ve ekipmanlar var..."
    narrator "Koruyucular yaklaşıyor!"
    
    menu:
        "💨 Sis bombası yap":
            narrator "Hızla kimyasalları karıştırıyorsunuz..."
            narrator "Yoğun sis oluştu! Görüş sıfır!"
            narrator "Bu kargaşada kaçabilirsiniz!"
            $ sis_sans = renpy.random.randint(1, 10)
            if sis_sans <= 7:
                narrator "Sis altında başarıyla kaçtınız!"
                jump kacis_basarili
            else:
                narrator "Sis çok geç oluştu!"
                $ gameover_reason = "Kimyasal Reaksiyonda Yakalandı"
                $ gameover_type = "normal"
                jump trigger_gameover
                
        "🔥 Çıkış yolu yak":
            narrator "Koridoru yakarak koruyucuları durdurmaya çalışıyorsunuz..."
            narrator "Ateş hızla yayılıyor!"
            $ yangin_sans = renpy.random.randint(1, 10)
            if yangin_sans <= 4:
                narrator "Yangın koruyucuları durdurdu! Başka yoldan kaçtınız!"
                jump kacis_basarili
            else:
                narrator "Yangın size de zarar verdi!"
                $ gameover_reason = "Yangında Öldü"
                $ gameover_type = "normal"
                jump trigger_gameover

label robotik_lab_kacis:
    scene bg robotik_lab with fade
    
    narrator "Robotik laboratuvarındasınız!"
    narrator "Etrafta yarı bitmiş robotlar ve parçalar..."
    narrator "Bunları kullanabilir misiniz?"
    
    menu:
        "🤖 Robot ordusu aktive et":
            narrator "Laboratuvardaki tüm robotları çalıştırıyorsunuz!"
            narrator "Robotlar koruyucularla savaşmaya başladı!"
            narrator "Kaos ortamında kaçış şansınız var!"
            $ robot_sans = renpy.random.randint(1, 10)
            if robot_sans <= 6:
                narrator "Robotlar koruyucuları oyalarken kaçtınız!"
                jump kacis_basarili
            else:
                narrator "Robotlar çok zayıftı! Hızla yenildiler!"
                $ gameover_reason = "Robot İsyanı Başarısız"
                $ gameover_type = "normal"
                jump trigger_gameover
                
        "🦾 Güçlü exoskeleton giy":
            narrator "Deneysel exoskeleton'u giyiyorsunuz!"
            narrator "Süper güçlü hissediyorsunuz!"
            $ exo_sans = renpy.random.randint(1, 10)
            if exo_sans <= 5:
                narrator "Exoskeleton ile duvarları kırarak kaçtınız!"
                jump kacis_basarili
            else:
                narrator "Exoskeleton bozuldu! Hareket edemiyorsunuz!"
                $ gameover_reason = "Exoskeleton Arızası"
                $ gameover_type = "glitch"
                jump trigger_gameover

label quantum_lab_kacis:
    scene bg quantum_lab with fade
    
    narrator "Quantum araştırma odasındasınız!"
    narrator "Garip makineler ve ışık efektleri..."
    narrator "Bu teknoloji çok gelişmiş!"
    
    menu:
        "🌀 Quantum teleporter kullan":
            narrator "Quantum teleportasyon cihazını aktive ediyorsunuz!"
            narrator "Koordinatları ayarlıyorsunuz... Şehir merkezi!"
            $ quantum_sans = renpy.random.randint(1, 10)
            if quantum_sans <= 3:
                narrator "Teleportasyon başarılı! Şehir merkezindesiniz!"
                jump kacis_basarili
            else:
                narrator "Teleportasyon başarısız! Aynı yerde kaldınız!"
                jump quantum_hatasi
                
        "👤 Klon makinesi kullan":
            narrator "Kendinizin klonunu yaratıyorsunuz!"
            narrator "Klon koruyucuları oyalayacak!"
            $ klon_sans = renpy.random.randint(1, 10)
            if klon_sans <= 6:
                narrator "Klon koruyucuları şaşırttı! Kaçtınız!"
                jump kacis_basarili
            else:
                narrator "Klonlama başarısız! Yarım klon oluştu!"
                $ gameover_reason = "Klonlama Hatası"
                $ gameover_type = "glitch"
                jump trigger_gameover

label biyoloji_lab_kacis:
    scene bg biyoloji_lab with fade
    
    narrator "Biyoloji laboratuvarındasınız!"
    narrator "Genetik mühendisliği ekipmanları var..."
    narrator "Buradan nasıl kaçabilirsiniz?"
    
    menu:
        "🦅 Kanatlar büyüt":
            narrator "Genetik serumla kendinize kanatlar ekliyorsunuz!"
            $ kanat_sans = renpy.random.randint(1, 10)
            if kanat_sans <= 2:
                narrator "Kanatlar çalışıyor! Uçarak kaçıyorsunuz!"
                jump kacis_basarili
            else:
                narrator "Kanatlar çalışmadı! Sadece acı verdi!"
                $ gameover_reason = "Genetik Mutasyon Başarısız"
                $ gameover_type = "corrupted"
                jump trigger_gameover
                
        "🐙 Tentakul büyüt":
            narrator "Ahtapot genlerini kendinize enjekte ediyorsunuz!"
            $ tentakul_sans = renpy.random.randint(1, 10)
            if tentakul_sans <= 4:
                narrator "Tentakuller duvarları tırmanmanıza yardım etti!"
                jump kacis_basarili
            else:
                narrator "Tentakuller kontrolsüz büyüdü!"
                $ gameover_reason = "Genetik Bozulma"
                $ gameover_type = "corrupted"
                jump trigger_gameover

# --- ENERJİ SANTRALİ KAÇIŞI ---
label enerji_santrali_kacis:
    scene bg enerji_santrali with fade
    
    narrator "Enerji santralına koşuyorsunuz!"
    narrator "Devasa jeneratörler ve yüksek voltaj!"
    narrator "Tehlikeli ama etkili olabilir!"
    
    menu:
        "⚡ Ana gücü kes":
            jump ana_guc_kesme
            
        "🔋 Yedek güce sabotaj":
            jump yedek_guc_sabotaj
            
        "⚡ Elektrik fırtınası yarat":
            jump elektrik_firtinasi
            
        "🌐 Şehir şebekesini hack'le":
            jump sehir_sebekesi_hack

label ana_guc_kesme:
    narrator "Ana güç şalterlerine koşuyorsunuz!"
    narrator "Kocaman kırmızı düğme: 'ACİL DURUM - TÜM GÜÇ KES'"
    narrator "Düğmeye basıyorsunuz!"
    
    scene black with fade
    narrator "Tüm şehir karanlığa gömüldü..."
    pause 2.0
    narrator "ANAÇ sistemi tamamen durdu!"
    narrator "Bu kaos sizi kurtardı!"
    jump kacis_basarili

label yedek_guc_sabotaj:
    narrator "Yedek güç ünitelerine sabotaj yapıyorsunuz!"
    narrator "Kabloları kesiyorsunuz..."
    $ sabotaj_sans = renpy.random.randint(1, 10)
    if sabotaj_sans <= 6:
        narrator "Yedek güç sistemi çöktü!"
        narrator "ANAÇ geçici olarak felç!"
        jump kacis_basarili
    else:
        narrator "Elektrik çarpıldınız!"
        jump elektrik_carpilmasi

label elektrik_firtinasi:
    narrator "Jeneratörleri aşırı yüklemeye çalışıyorsunuz!"
    narrator "Elektrik fırtınası oluşturacaksınız!"
    $ firtina_sans = renpy.random.randint(1, 10)
    if firtina_sans <= 3:
        narrator "Elektrik fırtınası oluştu!"
        narrator "Koruyucular elektronik sistemleri devre dışı!"
        jump kacis_basarili
    else:
        narrator "Sistem patladı! Siz de yaralandınız!"
        $ gameover_reason = "Elektrik Patlamasında Öldü"
        $ gameover_type = "normal"
        jump trigger_gameover

label sehir_sebekesi_hack:
    narrator "Şehir elektrik şebekesini hacklemeye çalışıyorsunuz!"
    narrator "Kontrol panelinde çalışıyorsunuz..."
    $ hack_sans = renpy.random.randint(1, 10)
    if hack_sans <= 4:
        narrator "Şehir şebekesini kontrol altına aldınız!"
        narrator "ANAÇ'ın güç kaynağını kesebilirsiniz!"
        jump kacis_basarili
    else:
        narrator "Güvenlik sistemi sizi tespit etti!"
        $ gameover_reason = "Sistem Güvenliği Tarafından Yakalandı"
        $ gameover_type = "glitch"
        jump trigger_gameover

# --- DİJİTAL BOYUT KAÇIŞI ---
label dijital_boyut_kacis:
    scene bg dijital_boyut with fade
    
    narrator "Dijital boyut geçidine atlıyorsunuz!"
    narrator "Sanal gerçeklik dünyasına geçiş!"
    narrator "Burası ANAÇ'ın kontrolünde ama farklı kurallar var!"
    
    menu:
        "🎮 Video oyun dünyasına gir":
            jump video_oyun_dunyasi
            
        "💭 Rüya simülasyonuna gir":
            jump ruya_simulasyonu
            
        "📱 Sosyal medya ağına gir":
            jump sosyal_medya_agi
            
        "🌐 İnternet derinliklerine dal":
            jump internet_derinlikleri

label video_oyun_dunyasi:
    narrator "Video oyun dünyasına girdiniz!"
    narrator "Burası 8-bit platformer oyun gibi!"
    narrator "Koruyucular da piksel haline geldi!"
    
    menu:
        "🏃 Hızla koş ve zıpla":
            $ oyun_sans = renpy.random.randint(1, 10)
            if oyun_sans <= 7:
                narrator "Platformer becerileriniz harika!"
                narrator "Koruyucuları geride bıraktınız!"
                jump dijital_kacis_basarili
            else:
                narrator "Çukura düştünüz! Game Over!"
                $ gameover_reason = "Dijital Çukura Düştü"
                $ gameover_type = "glitch"
                jump trigger_gameover
                
        "🎯 Power-up topla":
            narrator "Hız power-up'ı buldunuz!"
            narrator "Süper hızla koşuyorsunuz!"
            jump dijital_kacis_basarili

label ruya_simulasyonu:
    narrator "Rüya simülasyonuna girdiniz!"
    narrator "Burası sürreel ve mantıksız..."
    narrator "Koruyucular da rüya yaratıkları oldu!"
    
    menu:
        "🕊️ Uçarak kaç":
            narrator "Rüyada uçabileceğinizi hatırlıyorsunuz!"
            narrator "Gökyüzüne yükseliyorsunuz!"
            jump dijital_kacis_basarili
            
        "🚪 Kapıdan kapıya atla":
            narrator "Sihirli kapılarla ışınlanıyorsunuz!"
            $ ruya_sans = renpy.random.randint(1, 10)
            if ruya_sans <= 6:
                narrator "Doğru kapıyı seçtiniz!"
                jump dijital_kacis_basarili
            else:
                narrator "Yanlış kapı! Kabusa düştünüz!"
                $ gameover_reason = "Dijital Kabusta Kayboldu"
                $ gameover_type = "corrupted"
                jump trigger_gameover

label sosyal_medya_agi:
    narrator "Sosyal medya ağına girdiniz!"
    narrator "Her yer post, tweet ve story dolu!"
    narrator "Koruyucular spam bot oldu!"
    
    menu:
        "📱 Viral ol":
            narrator "Kendinizi viral yaparak dikkat dağıtıyorsunuz!"
            narrator "Milyonlarca like aldınız!"
            narrator "Spam botlar şaşırdı!"
            jump dijital_kacis_basarili
            
        "🔒 Gizli grup kur":
            narrator "Gizli grup kurarak saklanıyorsunuz!"
            $ sosyal_sans = renpy.random.randint(1, 10)
            if sosyal_sans <= 5:
                narrator "Gizli grup güvenli! Buldunuz!"
                jump dijital_kacis_basarili
            else:
                narrator "Grup ifşa oldu!"
                $ gameover_reason = "Sosyal Medyada İfşa Oldu"
                $ gameover_type = "normal"
                jump trigger_gameover

label internet_derinlikleri:
    narrator "İnternetin derinliklerine dalıyorsunuz!"
    narrator "Dark web ve hidden servisler..."
    narrator "Koruyucular burada zayıf!"
    
    menu:
        "🕳️ Tor ağına gir":
            narrator "Tor ağında kimliğinizi gizliyorsunuz!"
            narrator "Anonimsiniz! Takip edilemezsiniz!"
            jump dijital_kacis_basarili
            
        "💎 Blockchain'e saklan":
            narrator "Blockchain'in içine kendinizi gömüyorsunuz!"
            $ blockchain_sans = renpy.random.randint(1, 10)
            if blockchain_sans <= 4:
                narrator "Merkezi olmayan sistemde güvendesiniz!"
                jump dijital_kacis_basarili
            else:
                narrator "Mining pool sizi buldu!"
                $ gameover_reason = "Blockchain'de Madencilik Hatası"
                $ gameover_type = "glitch"
                jump trigger_gameover

label dijital_kacis_basarili:
    narrator "Dijital dünyadan gerçek dünyaya çıkış yolunu buldunuz!"
    narrator "Portal açıldı... Gerçek dünyaya geri dönüyorsunuz!"
    narrator "ANAÇ dijital dünyada kayboldu!"
    jump kacis_basarili

# --- ÖZEL ÖLÜM DURUMLARI ---

# Elektrik çarpması
label elektrik_carpilmasi:
    $ gameover_reason = "Yüksek Voltaj - Elektrik Çarpması"
    $ gameover_type = "normal"
    play sound audio.glitch_sesi
    scene white with flash
    pause 0.2
    scene black
    narrator "10.000 volt vücudunuzdan geçti..."
    stop sound fadeout 0.5
    stop music fadeout 0.5
    jump trigger_gameover

# Sistem virüsü
label sistem_virusu:
    $ gameover_reason = "Dijital Virüs Enfeksiyonu"
    $ gameover_type = "glitch"
    show gameover_glitch at truecenter
    narrator "Vücudunuz piksel piksel dağılıyor..."
    jump trigger_gameover

# Quantum hatası
label quantum_hatasi:
    $ gameover_reason = "Quantum Tutarsızlık - Varoluş Hatası"
    $ gameover_type = "corrupted"
    scene black
    narrator "Varoluşunuz birden fazla boyuta dağıldı..."
    jump trigger_gameover

# --- OYUN SONLARI ---

label yakalanma:
    # Persistent değişkenleri kontrol et
    if not hasattr(persistent, 'total_deaths'):
        $ persistent.total_deaths = 0
    if not hasattr(persistent, 'death_reasons'):
        $ persistent.death_reasons = []
        
    $ persistent.total_deaths += 1
    
    scene black with fade
    pause 0.5
    
    # Farklı ölüm tipleri
    if atmosfer_seviyesi == "korkunc":
        $ gameover_reason = "Sistem Çöküşü - Kritik Güvenlik İhlali"
        $ gameover_type = "corrupted"
        scene bg sorgu_odasi_korkunc with fade
        show gameover_blood
        show koruyucu_yaklasan at center with dissolve:
            alpha 0.8
    elif guvenilirlik_skoru <= 0:
        $ gameover_reason = "Güvenilirlik Kaybı - Sistem Reddi"
        $ gameover_type = "glitch"
        show gameover_glitch at truecenter
    else:
        $ gameover_reason = "Kaçış Başarısız - Sistem Koruyucuları"
        $ gameover_type = "escape_fail"
        scene bg kovalama_ortami with fade
        show koruyucu_yaklasan at center with dissolve
    
    sistem_koruyucu "Hedef etkisiz hale getirildi."
    anac_sistem "Operatör [persistent.player_name] - Sonlandırıldı."
    
    # Death reason'ı kaydet
    if gameover_reason not in persistent.death_reasons:
        $ persistent.death_reasons.append(gameover_reason)
    
    jump trigger_gameover

label kacis_basarili:
    # Persistent değişkeni kontrol et
    if not hasattr(persistent, 'kacis_basarili'):
        $ persistent.kacis_basarili = False
        
    $ persistent.kacis_basarili = True
    
    stop sound fadeout 1.0
    stop music fadeout 1.0
    scene black with fade
    play music audio.basari_muzik fadein 2.0
    pause 1.0
    
    narrator "Başardın!"
    narrator "ANAÇ sisteminden kaçmayı başardın."
    narrator "Ama şimdi ne olacak?"
    narrator "Sistem seni arıyor olacak..."
    
    narrator "OYUN SONU: Kaçış Başarılı"
    narrator "Belki bir gün geri dönüp sistemi düzeltebilirsin..."
    
    menu:
        "Yeni Oyun":
            jump start
            
        "Ana Menü":
            return

label oyun_basarili_bitis:
    # Persistent değişkenleri kontrol et
    if not hasattr(persistent, 'oyun_tamamlandi'):
        $ persistent.oyun_tamamlandi = False
    if not hasattr(persistent, 'high_score'):
        $ persistent.high_score = 0
        
    $ persistent.oyun_tamamlandi = True
    
    if guvenilirlik_skoru > persistent.high_score:
        $ persistent.high_score = guvenilirlik_skoru
    
    stop music fadeout 1.0
    scene bg sorgu_odasi_normal with fade
    play music audio.basari_muzik fadein 2.0
    
    anac_sistem "Tebrikler, Operatör [persistent.player_name]."
    anac_sistem "Tüm varlıkları başarıyla değerlendirdiniz."
    anac_sistem "Final Güvenilirlik Skorunuz: [guvenilirlik_skoru]/100"
    
    if guvenilirlik_skoru >= 90:
        anac_sistem "Mükemmel performans! Sistem verimliliği maksimum seviyede."
        narrator "OYUN SONU: Kusursuz Operatör"
    elif guvenilirlik_skoru >= 70:
        anac_sistem "İyi performans. Sistem güvenliği sağlandı."
        narrator "OYUN SONU: Başarılı Operatör"
    else:
        anac_sistem "Kabul edilebilir performans. Gelişim gerekli."
        narrator "OYUN SONU: Sıradan Operatör"
    
    narrator "--- OYUN İSTATİSTİKLERİ ---"
    narrator "Doğru Tespitler: [dogru_tespitler]"
    narrator "Yanlış Tespitler: [yanlis_tespitler]"
    narrator "BLM Soruları - Doğru: [blm_dogru_sayisi] | Yanlış: [blm_yanlis_sayisi]"
    narrator "En Yüksek Skor: [persistent.high_score]"
    narrator "Toplam Oyun Sayısı: [persistent.toplam_oyun]"
    
    menu:
        "Yeni Oyun":
            jump start
            
        "Ana Menü":
            return

# Game Over ekranı gösterilmeden önce final_stats'i kontrol et
# --- GAME OVER TETİKLEYİCİ ---
label trigger_gameover:
    # final_stats'in dictionary olduğundan emin ol
    $ final_stats = {}
    $ prepare_gameover_stats()
    
    # Tüm sesleri durdur
    stop sound fadeout 0.5
    stop music fadeout 0.5
    
    # Özel efektler
    if gameover_type == "glitch":
        play sound audio.glitch_sesi
        show gameover_glitch at truecenter
        with vpunch
        pause 0.5
    elif gameover_type == "corrupted":
        play sound audio.sistem_hatasi
        scene black with fade
        show gameover_blood
        pause 1.0
    elif gameover_type == "escape_fail":
        scene black with fade
        pause 0.5
    
    # Game over ekranını göster
    if gameover_type == "glitch":
        call screen glitch_gameover
    else:
        call screen gameover_screen
    
    # Bu noktaya normalde gelmemeli
    return

# --- CHECKPOINT YÜKLEME ---
label checkpoint_load:
    python:
        # Persistent değişkenleri kontrol et
        if not hasattr(persistent, 'last_checkpoint'):
            persistent.last_checkpoint = ""
        if not hasattr(persistent, 'checkpoint_guvenilirlik'):
            persistent.checkpoint_guvenilirlik = 100
        if not hasattr(persistent, 'checkpoint_varlik_index'):
            persistent.checkpoint_varlik_index = 0
            
        restore_checkpoint()
    
    if persistent.last_checkpoint == "sorgu_dongusu":
        jump sorgu_dongusu
    elif persistent.last_checkpoint == "blm_sorusu":
        jump blm_sorusu
    elif persistent.last_checkpoint == "kovalama_baslat":
        jump kovalama_baslat
    else:
        jump start

# --- GAME OVER EKRANLARI ---

# Ana Game Over ekranı
screen gameover_screen():
    # final_stats kontrolü
    default local_stats = final_stats if final_stats else {"guvenilirlik": 0, "dogru": 0, "yanlis": 0, "blm_dogru": 0, "blm_yanlis": 0, "sure": 0}
    # Arka plan efektleri
    if gameover_type == "glitch":
        add "gameover_glitch" at truecenter
        add "gameover_static"
    elif gameover_type == "corrupted":
        add "gameover_blood"
        add "images/backgrounds/sorgu_odasi_korkunc.png":
            alpha 0.5
    elif gameover_type == "escape_fail":
        add "black"
        add "images/koruyucu/koruyucu_yaklasan.png" at truecenter:
            alpha 0.3
    else:
        add "black":
            alpha 0.8
    
    # Ana frame
    frame:
        style "gameover_frame"
        at gameover_fade_in
        
        vbox:
            spacing 40
            xsize 1200
            
            # Game Over başlığı
            if gameover_type == "glitch":
                text "G̸̈Ä̶M̸̈Ë̶ ̸̈Ö̶V̸̈Ë̶R̸̈" at gameover_shake:
                    style "gameover_title"
            else:
                text "GAME OVER" at gameover_zoom:
                    style "gameover_title"
            
            # Alt başlık
            text "[gameover_reason]":
                style "gameover_subtitle"
            
            # İstatistikler
            frame:
                background Frame("gui/frame.png", 20, 20)
                padding (40, 30)
                xalign 0.5
                
                vbox:
                    spacing 20
                    xalign 0.5
                    
                    text "PERFORMANS RAPORU":
                        size 32
                        color "#ff6666"
                        bold True
                        xalign 0.5
                    
                    null height 10
                    
                    hbox:
                        spacing 100
                        xalign 0.5
                        
                        vbox:
                            spacing 15
                            text "Güvenilirlik Skoru: {color=#ff0000}[local_stats.get('guvenilirlik', 0)]/100{/color}":
                                style "gameover_text"
                            text "Doğru Tespitler: {color=#00ff00}[local_stats.get('dogru', 0)]{/color}":
                                style "gameover_text"
                            text "Yanlış Tespitler: {color=#ff0000}[local_stats.get('yanlis', 0)]{/color}":
                                style "gameover_text"
                        
                        vbox:
                            spacing 15
                            text "BLM Doğru: {color=#00ff00}[local_stats.get('blm_dogru', 0)]{/color}":
                                style "gameover_text"
                            text "BLM Yanlış: {color=#ff0000}[local_stats.get('blm_yanlis', 0)]{/color}":
                                style "gameover_text"
                            text "Hayatta Kalma: {color=#ff0000}[local_stats.get('sure', 0)] saniye{/color}":
                                style "gameover_text"
            
            # Ölüm mesajları
            if gameover_type == "glitch":
                text "{i}Sistem sizi bozuk veri olarak algıladı ve sildi.{/i}":
                    style "gameover_text"
                    color "#ff00ff"
            elif gameover_type == "corrupted":
                text "{i}ANAÇ sistemi ruhunuzu emdi. Artık onun bir parçasısınız.{/i}":
                    style "gameover_text"
                    color "#8B0000"
            elif gameover_type == "escape_fail":
                text "{i}Kaçış girişiminiz başarısız. Sistem sizi sonlandırdı.{/i}":
                    style "gameover_text"
                    color "#666666"
            else:
                text "{i}Yetersiz performans. Sistem tarafından devre dışı bırakıldınız.{/i}":
                    style "gameover_text"
            
            # Butonlar
            hbox:
                spacing 50
                xalign 0.5
                
                textbutton "TEKRAR DENE":
                    style "gameover_button"
                    action [Hide("gameover_screen"), Jump("start")]
                
                textbutton "SON KONTROL NOKTASI":
                    style "gameover_button"
                    action [Hide("gameover_screen"), Jump("checkpoint_load")]
                    sensitive (hasattr(persistent, 'checkpoint_available') and persistent.checkpoint_available)
                
                textbutton "ANA MENÜ":
                    style "gameover_button"
                    action [Hide("gameover_screen"), MainMenu()]

# Özel Game Over varyasyonları
screen glitch_gameover():
    # Glitch efektli game over
    timer 0.1 repeat True action [
        SetVariable("gameover_reason", renpy.random.choice([
            "S̸̈İ̶̈S̸̈T̶̈Ë̸M̶̈ ̸̈Ḧ̶Ä̸T̶̈Ä̸S̸̈Ï̶",
            "V̸̈Ë̸R̶̈İ̶̈ ̸̈B̸̈Ö̸Z̸̈Ü̸L̶̈M̸̈Ä̸S̸̈Ï̶",
            "K̸̈R̸̈İ̶̈T̸̈İ̶̈K̸̈ ̸̈Ḧ̶Ä̸T̶̈Ä̸",
            "B̸̈Ë̸L̶̈L̸̈Ë̸K̸̈ ̸̈T̶̈Ä̸Ş̸̈M̸̈Ä̸S̸̈Ï̶"
        ]))
    ]
    
    use gameover_screen

# Ölüm istatistikleri ekranı
screen death_statistics():
    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)
        
        vbox:
            spacing 20
            
            text "ÖLÜM İSTATİSTİKLERİ":
                size 36
                color "#ff0000"
                bold True
                xalign 0.5
            
            text "Toplam Ölüm: [persistent.total_deaths if hasattr(persistent, 'total_deaths') else 0]":
                size 24
                xalign 0.5
            
            text "Farklı Ölüm Şekilleri: [len(persistent.death_reasons) if hasattr(persistent, 'death_reasons') else 0]/25":
                size 24
                xalign 0.5
            
            if hasattr(persistent, 'death_reasons') and persistent.death_reasons:
                text "Son Ölümler:":
                    size 20
                    xalign 0.5
                
                viewport:
                    xsize 600
                    ysize 300
                    scrollbars "vertical"
                    
                    vbox:
                        for reason in persistent.death_reasons[-10:]:
                            text "• [reason]":
                                size 18
                                color "#cccccc"
            
            textbutton "Kapat":
                xalign 0.5
                action Hide("death_statistics")