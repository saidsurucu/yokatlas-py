"""Form data extracted from YOKATLAS search interface."""

# Score types
SCORE_TYPES = [
    "say",
    "söz", 
    "ea",
    "dil"
]

# Universities (235 total)
UNIVERSITIES = [
    "ABDULLAH GÜL ÜNİVERSİTESİ",
    "ACIBADEM MEHMET ALİ AYDINLAR ÜNİVERSİTESİ",
    "ADA KENT ÜNİVERSİTESİ",
    "ADANA ALPARSLAN TÜRKEŞ BİLİM VE TEKNOLOJİ ÜNİVERSİTESİ",
    "ADIYAMAN ÜNİVERSİTESİ",
    "AFYON KOCATEPE ÜNİVERSİTESİ",
    "AFYONKARAHİSAR SAĞLIK BİLİMLERİ ÜNİVERSİTESİ",
    "AĞRI İBRAHİM ÇEÇEN ÜNİVERSİTESİ",
    "AKDENİZ KARPAZ ÜNİVERSİTESİ",
    "AKDENİZ ÜNİVERSİTESİ",
    "AKSARAY ÜNİVERSİTESİ",
    "ALANYA ALAADDİN KEYKUBAT ÜNİVERSİTESİ",
    "ALANYA ÜNİVERSİTESİ",
    "ALTINBAŞ ÜNİVERSİTESİ",
    "AMASYA ÜNİVERSİTESİ",
    "ANADOLU ÜNİVERSİTESİ",
    "ANKARA BİLİM ÜNİVERSİTESİ",
    "ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ",
    "ANKARA MEDİPOL ÜNİVERSİTESİ",
    "ANKARA SOSYAL BİLİMLER ÜNİVERSİTESİ",
    "ANKARA ÜNİVERSİTESİ",
    "ANKARA YILDIRIM BEYAZIT ÜNİVERSİTESİ",
    "ANTALYA BELEK ÜNİVERSİTESİ",
    "ANTALYA BİLİM ÜNİVERSİTESİ",
    "ARDAHAN ÜNİVERSİTESİ",
    "ARKIN YARATICI SANATLAR VE TASARIM ÜNİVERSİTESİ",
    "ARTVİN ÇORUH ÜNİVERSİTESİ",
    "ATATÜRK ÜNİVERSİTESİ",
    "ATILIM ÜNİVERSİTESİ",
    "AVRASYA ÜNİVERSİTESİ",
    "AYDIN ADNAN MENDERES ÜNİVERSİTESİ",
    "AZERBAYCAN DEVLET PEDAGOJİ ÜNİVERSİTESİ",
    "AZERBAYCAN DİLLER ÜNİVERSİTESİ",
    "AZERBAYCAN TIP ÜNİVERSİTESİ",
    "BAHÇEŞEHİR KIBRIS ÜNİVERSİTESİ",
    "BAHÇEŞEHİR ÜNİVERSİTESİ",
    "BAKÜ DEVLET ÜNİVERSİTESİ",
    "BALIKESİR ÜNİVERSİTESİ",
    "BANDIRMA ONYEDİ EYLÜL ÜNİVERSİTESİ",
    "BARTIN ÜNİVERSİTESİ",
    "BAŞKENT ÜNİVERSİTESİ",
    "BATMAN ÜNİVERSİTESİ",
    "BAYBURT ÜNİVERSİTESİ",
    "BEYKOZ ÜNİVERSİTESİ",
    "BEZM-İ ÂLEM VAKIF ÜNİVERSİTESİ",
    "BİLECİK ŞEYH EDEBALİ ÜNİVERSİTESİ",
    "BİNGÖL ÜNİVERSİTESİ",
    "BİRUNİ ÜNİVERSİTESİ",
    "BİTLİS EREN ÜNİVERSİTESİ",
    "BOĞAZİÇİ ÜNİVERSİTESİ",
    "BOLU ABANT İZZET BAYSAL ÜNİVERSİTESİ",
    "BURDUR MEHMET AKİF ERSOY ÜNİVERSİTESİ",
    "BURSA TEKNİK ÜNİVERSİTESİ",
    "BURSA ULUDAĞ ÜNİVERSİTESİ",
    "ÇAĞ ÜNİVERSİTESİ",
    "ÇANAKKALE ONSEKİZ MART ÜNİVERSİTESİ",
    "ÇANKAYA ÜNİVERSİTESİ",
    "ÇANKIRI KARATEKİN ÜNİVERSİTESİ",
    "ÇUKUROVA ÜNİVERSİTESİ",
    "DEMİROĞLU BİLİM ÜNİVERSİTESİ",
    "DİCLE ÜNİVERSİTESİ",
    "DOĞU AKDENİZ ÜNİVERSİTESİ",
    "DOĞUŞ ÜNİVERSİTESİ",
    "DOKUZ EYLÜL ÜNİVERSİTESİ",
    "DÜZCE ÜNİVERSİTESİ",
    "EGE ÜNİVERSİTESİ",
    "ERCİYES ÜNİVERSİTESİ",
    "ERZİNCAN BİNALİ YILDIRIM ÜNİVERSİTESİ",
    "ERZURUM TEKNİK ÜNİVERSİTESİ",
    "ESKİŞEHİR OSMANGAZİ ÜNİVERSİTESİ",
    "ESKİŞEHİR TEKNİK ÜNİVERSİTESİ",
    "FATİH SULTAN MEHMET VAKIF ÜNİVERSİTESİ",
    "FENERBAHÇE ÜNİVERSİTESİ",
    "FIRAT ÜNİVERSİTESİ",
    "GALATASARAY ÜNİVERSİTESİ",
    "GAZİ ÜNİVERSİTESİ",
    "GAZİANTEP İSLAM BİLİM VE TEKNOLOJİ ÜNİVERSİTESİ",
    "GAZİANTEP ÜNİVERSİTESİ",
    "GEBZE TEKNİK ÜNİVERSİTESİ",
    "GİRESUN ÜNİVERSİTESİ",
    "GİRNE AMERİKAN ÜNİVERSİTESİ",
    "GİRNE ÜNİVERSİTESİ",
    "GÜMÜŞHANE ÜNİVERSİTESİ",
    "HACETTEPE ÜNİVERSİTESİ",
    "HAKKARİ ÜNİVERSİTESİ",
    "HALİÇ ÜNİVERSİTESİ",
    "HARRAN ÜNİVERSİTESİ",
    "HASAN KALYONCU ÜNİVERSİTESİ",
    "HATAY MUSTAFA KEMAL ÜNİVERSİTESİ",
    "HİTİT ÜNİVERSİTESİ",
    "HOCA AHMET YESEVİ ULUSLARARASI TÜRK-KAZAK ÜNİVERSİTESİ",
    "IĞDIR ÜNİVERSİTESİ",
    "ISPARTA UYGULAMALI BİLİMLER ÜNİVERSİTESİ",
    "IŞIK ÜNİVERSİTESİ",
    "İBN HALDUN ÜNİVERSİTESİ",
    "İHSAN DOĞRAMACI BİLKENT ÜNİVERSİTESİ",
    "İNÖNÜ ÜNİVERSİTESİ",
    "İSKENDERUN TEKNİK ÜNİVERSİTESİ",
    "İSTANBUL 29 MAYIS ÜNİVERSİTESİ",
    "İSTANBUL AREL ÜNİVERSİTESİ",
    "İSTANBUL ATLAS ÜNİVERSİTESİ",
    "İSTANBUL AYDIN ÜNİVERSİTESİ",
    "İSTANBUL BEYKENT ÜNİVERSİTESİ",
    "İSTANBUL BİLGİ ÜNİVERSİTESİ",
    "İSTANBUL ESENYURT ÜNİVERSİTESİ",
    "İSTANBUL GALATA ÜNİVERSİTESİ",
    "İSTANBUL GEDİK ÜNİVERSİTESİ",
    "İSTANBUL GELİŞİM ÜNİVERSİTESİ",
    "İSTANBUL KENT ÜNİVERSİTESİ",
    "İSTANBUL KÜLTÜR ÜNİVERSİTESİ",
    "İSTANBUL MEDENİYET ÜNİVERSİTESİ",
    "İSTANBUL MEDİPOL ÜNİVERSİTESİ",
    "İSTANBUL NİŞANTAŞI ÜNİVERSİTESİ",
    "İSTANBUL OKAN ÜNİVERSİTESİ",
    "İSTANBUL RUMELİ ÜNİVERSİTESİ",
    "İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ",
    "İSTANBUL SAĞLIK VE TEKNOLOJİ ÜNİVERSİTESİ",
    "İSTANBUL TEKNİK ÜNİVERSİTESİ",
    "İSTANBUL TİCARET ÜNİVERSİTESİ",
    "İSTANBUL TOPKAPI ÜNİVERSİTESİ",
    "İSTANBUL ÜNİVERSİTESİ",
    "İSTANBUL ÜNİVERSİTESİ-CERRAHPAŞA",
    "İSTANBUL YENİ YÜZYIL ÜNİVERSİTESİ ",
    "İSTİNYE ÜNİVERSİTESİ",
    "İZMİR BAKIRÇAY ÜNİVERSİTESİ",
    "İZMİR DEMOKRASİ ÜNİVERSİTESİ",
    "İZMİR EKONOMİ ÜNİVERSİTESİ",
    "İZMİR KATİP ÇELEBİ ÜNİVERSİTESİ",
    "İZMİR TINAZTEPE ÜNİVERSİTESİ",
    "İZMİR YÜKSEK TEKNOLOJİ ENSTİTÜSÜ",
    "KADİR HAS ÜNİVERSİTESİ",
    "KAFKAS ÜNİVERSİTESİ",
    "KAHRAMANMARAŞ İSTİKLAL ÜNİVERSİTESİ",
    "KAHRAMANMARAŞ SÜTÇÜ İMAM ÜNİVERSİTESİ",
    "KAPADOKYA ÜNİVERSİTESİ",
    "KARABÜK ÜNİVERSİTESİ",
    "KARADENİZ TEKNİK ÜNİVERSİTESİ",
    "KARAMANOĞLU MEHMETBEY ÜNİVERSİTESİ",
    "KASTAMONU ÜNİVERSİTESİ",
    "KAYSERİ ÜNİVERSİTESİ",
    "KIBRIS AMERİKAN ÜNİVERSİTESİ",
    "KIBRIS BATI ÜNİVERSİTESİ",
    "KIBRIS İLİM ÜNİVERSİTESİ",
    "KIBRIS SAĞLIK VE TOPLUM BİLİMLERİ ÜNİVERSİTESİ",
    "KIRGIZİSTAN-TÜRKİYE MANAS ÜNİVERSİTESİ",
    "KIRIKKALE ÜNİVERSİTESİ",
    "KIRKLARELİ ÜNİVERSİTESİ",
    "KIRŞEHİR AHİ EVRAN ÜNİVERSİTESİ",
    "KİLİS 7 ARALIK ÜNİVERSİTESİ",
    "KOCAELİ SAĞLIK VE TEKNOLOJİ ÜNİVERSİTESİ",
    "KOCAELİ ÜNİVERSİTESİ",
    "KOÇ ÜNİVERSİTESİ",
    "KONYA GIDA VE TARIM ÜNİVERSİTESİ",
    "KONYA TEKNİK ÜNİVERSİTESİ",
    "KTO KARATAY ÜNİVERSİTESİ",
    "KÜTAHYA DUMLUPINAR ÜNİVERSİTESİ",
    "KÜTAHYA SAĞLIK BİLİMLERİ ÜNİVERSİTESİ",
    "LEFKE AVRUPA ÜNİVERSİTESİ",
    "LOKMAN HEKİM ÜNİVERSİTESİ",
    "MALATYA TURGUT ÖZAL ÜNİVERSİTESİ",
    "MALTEPE ÜNİVERSİTESİ",
    "MANİSA CELÂL BAYAR ÜNİVERSİTESİ ",
    "MARDİN ARTUKLU ÜNİVERSİTESİ",
    "MARMARA ÜNİVERSİTESİ",
    "MEF ÜNİVERSİTESİ",
    "MERSİN ÜNİVERSİTESİ",
    "MİMAR SİNAN GÜZEL SANATLAR ÜNİVERSİTESİ",
    "MUDANYA ÜNİVERSİTESİ",
    "MUĞLA SITKI KOÇMAN ÜNİVERSİTESİ",
    "MUNZUR ÜNİVERSİTESİ",
    "MUŞ ALPARSLAN ÜNİVERSİTESİ",
    "NECMETTİN ERBAKAN ÜNİVERSİTESİ",
    "NEVŞEHİR HACI BEKTAŞ VELİ ÜNİVERSİTESİ",
    "NİĞDE ÖMER HALİSDEMİR ÜNİVERSİTESİ",
    "NUH NACİ YAZGAN ÜNİVERSİTESİ",
    "ONDOKUZ MAYIS ÜNİVERSİTESİ",
    "ORDU ÜNİVERSİTESİ",
    "ORTA DOĞU TEKNİK ÜNİVERSİTESİ",
    "OSMANİYE KORKUT ATA ÜNİVERSİTESİ",
    "OSTİM TEKNİK ÜNİVERSİTESİ",
    "ÖZYEĞİN ÜNİVERSİTESİ",
    "PAMUKKALE ÜNİVERSİTESİ",
    "PİRİ REİS ÜNİVERSİTESİ",
    "RAUF DENKTAŞ ÜNİVERSİTESİ",
    "RECEP TAYYİP ERDOĞAN ÜNİVERSİTESİ",
    "SABANCI ÜNİVERSİTESİ",
    "SAĞLIK BİLİMLERİ ÜNİVERSİTESİ",
    "SAKARYA UYGULAMALI BİLİMLER ÜNİVERSİTESİ",
    "SAKARYA ÜNİVERSİTESİ",
    "SAMSUN ÜNİVERSİTESİ",
    "SANKO ÜNİVERSİTESİ",
    "SELÇUK ÜNİVERSİTESİ",
    "SİİRT ÜNİVERSİTESİ",
    "SİNOP ÜNİVERSİTESİ",
    "SİVAS BİLİM VE TEKNOLOJİ ÜNİVERSİTESİ",
    "SİVAS CUMHURİYET ÜNİVERSİTESİ",
    "SÜLEYMAN DEMİREL ÜNİVERSİTESİ",
    "ŞIRNAK ÜNİVERSİTESİ",
    "TARSUS ÜNİVERSİTESİ",
    "TED ÜNİVERSİTESİ",
    "TEKİRDAĞ NAMIK KEMAL ÜNİVERSİTESİ",
    "TOBB EKONOMİ VE TEKNOLOJİ ÜNİVERSİTESİ",
    "TOKAT GAZİOSMANPAŞA ÜNİVERSİTESİ",
    "TOROS ÜNİVERSİTESİ",
    "TRABZON ÜNİVERSİTESİ",
    "TRAKYA ÜNİVERSİTESİ",
    "TÜRK HAVA KURUMU ÜNİVERSİTESİ",
    "TÜRK-ALMAN ÜNİVERSİTESİ",
    "UFUK ÜNİVERSİTESİ",
    "ULUSLARARASI BALKAN ÜNİVERSİTESİ",
    "ULUSLARARASI FİNAL ÜNİVERSİTESİ",
    "ULUSLARARASI KIBRIS ÜNİVERSİTESİ",
    "ULUSLARARASI SARAYBOSNA ÜNİVERSİTESİ",
    "UŞAK ÜNİVERSİTESİ",
    "ÜSKÜDAR ÜNİVERSİTESİ",
    "VAN YÜZÜNCÜ YIL ÜNİVERSİTESİ ",
    "YAKIN DOĞU ÜNİVERSİTESİ",
    "YALOVA ÜNİVERSİTESİ",
    "YAŞAR ÜNİVERSİTESİ",
    "YEDİTEPE ÜNİVERSİTESİ",
    "YILDIZ TEKNİK ÜNİVERSİTESİ",
    "YOZGAT BOZOK ÜNİVERSİTESİ",
    "YÜKSEK İHTİSAS ÜNİVERSİTESİ",
    "ZONGULDAK BÜLENT ECEVİT ÜNİVERSİTESİ"
]

# Programs (200+ total)
PROGRAMS = [
    "Acil Yardım ve Afet Yönetimi (Fakülte)",
    "Acil Yardım ve Afet Yönetimi (Yüksekokul)",
    "Adli Bilimler",
    "Adli Bilişim Mühendisliği",
    "Adli Bilişim Mühendisliği (M.T.O.K.)",
    "Ağaç İşleri Endüstri Mühendisliği",
    "Ağaç İşleri Endüstri Mühendisliği (M.T.O.K.)",
    "Aktüerya Bilimleri",
    "Astronomi ve Uzay Bilimleri",
    "Bahçe Bitkileri",
    "Balıkçılık Teknolojisi Mühendisliği",
    "Basım Teknolojileri",
    "Beslenme ve Diyetetik (Fakülte)",
    "Beslenme ve Diyetetik (Yüksekokul)",
    "Bilgi Güvenliği Teknolojisi (Fakülte)",
    "Bilgi Güvenliği Teknolojisi (Yüksekokul)",
    "Bilgisayar Bilimleri",
    "Bilgisayar Bilimleri ve Mühendisliği",
    "Bilgisayar Mühendisliği",
    "Bilgisayar Mühendisliği (M.T.O.K.)",
    "Bilgisayar Teknolojisi ve Bilişim Sistemleri",
    "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği",
    "Bilişim Sistemleri Mühendisliği",
    "Bilişim Sistemleri Mühendisliği (M.T.O.K.)",
    "Bilişim Sistemleri ve Teknolojileri (Fakülte)",
    "Bilişim Sistemleri ve Teknolojileri (Yüksekokul)",
    "Bitki Koruma",
    "Bitkisel Üretim ve Teknolojileri",
    "Biyokimya",
    "Biyoloji",
    "Biyoloji Öğretmenliği",
    "Biyomedikal Mühendisliği",
    "Biyomedikal Mühendisliği (M.T.O.K.)",
    "Biyomühendislik",
    "Biyosistem Mühendisliği",
    "Biyoteknoloji",
    "Cevher Hazırlama Mühendisliği",
    "Çevre Mühendisliği",
    "Deniz Ulaştırma İşletme Mühendisliği (Fakülte)",
    "Deniz Ulaştırma İşletme Mühendisliği (Yüksekokul)",
    "Deri Mühendisliği",
    "Dijital Oyun Tasarımı",
    "Dil ve Konuşma Terapisi (Fakülte)",
    "Dil ve Konuşma Terapisi (Yüksekokul)",
    "Diş Hekimliği",
    "Ebelik (Fakülte)",
    "Ebelik (Yüksekokul)",
    "Eczacılık",
    "Elektrik Mühendisliği",
    "Elektrik-Elektronik Mühendisliği",
    "Elektrik-Elektronik Mühendisliği (M.T.O.K.)",
    "Elektronik Mühendisliği",
    "Elektronik ve Haberleşme Mühendisliği",
    "Endüstri Mühendisliği",
    "Endüstri Yönetimi Mühendisliği",
    "Endüstriyel Tasarım (Fakülte)",
    "Endüstriyel Tasarım (Yüksekokul)",
    "Endüstriyel Tasarım Mühendisliği",
    "Endüstriyel Tasarım Mühendisliği (M.T.O.K.)",
    "Enerji Bilimi ve Teknolojileri",
    "Enerji Sistemleri Mühendisliği",
    "Enerji Sistemleri Mühendisliği (M.T.O.K.)",
    "Ergoterapi",
    "Fen Bilgisi Öğretmenliği",
    "Fizik",
    "Fizik Mühendisliği",
    "Fizik Öğretmenliği",
    "Fizyoterapi ve Rehabilitasyon (Fakülte)",
    "Fizyoterapi ve Rehabilitasyon (Yüksekokul)",
    "Fotonik",
    "Gemi İnşaatı ve Gemi Makineleri Mühendisliği",
    "Gemi Makineleri İşletme Mühendisliği",
    "Gemi ve Deniz Teknolojisi Mühendisliği",
    "Gemi ve Yat Tasarımı",
    "Genetik ve Biyomühendislik",
    "Gerontoloji",
    "Gıda Mühendisliği",
    "Gıda Teknolojisi (Fakülte)",
    "Gıda Teknolojisi (Yüksekokul)",
    "Harita Mühendisliği",
    "Havacılık Elektrik ve Elektroniği (Fakülte)",
    "Havacılık Elektrik ve Elektroniği (Yüksekokul)",
    "Havacılık ve Uzay Mühendisliği",
    "Hayvansal Üretim ve Teknolojileri (Fakülte)",
    "Hayvansal Üretim ve Teknolojileri (Yüksekokul)",
    "Hemşirelik (Fakülte)",
    "Hemşirelik (Yüksekokul)",
    "Hidrojeoloji Mühendisliği",
    "İç Mimarlık",
    "İç Mimarlık ve Mobilya Tasarımı",
    "İklim Bilimi ve Meteoroloji Mühendisliği",
    "İlköğretim Matematik Öğretmenliği",
    "İmalat Mühendisliği",
    "İnşaat Mühendisliği",
    "İnşaat Mühendisliği (M.T.O.K.)",
    "İstatistik",
    "İstatistik ve Bilgisayar Bilimleri",
    "İş Sağlığı ve Güvenliği (Açıköğretim)",
    "İş Sağlığı ve Güvenliği (Fakülte)",
    "İş Sağlığı ve Güvenliği (Yüksekokul)",
    "İşletme Mühendisliği",
    "Jeofizik Mühendisliği",
    "Jeoloji Mühendisliği",
    "Kanatlı Hayvan Yetiştiriciliği",
    "Kentsel Tasarım ve Peyzaj Mimarlığı",
    "Kimya",
    "Kimya Mühendisliği",
    "Kimya Öğretmenliği",
    "Kimya-Biyoloji Mühendisliği",
    "Kontrol ve Otomasyon Mühendisliği",
    "Maden Mühendisliği",
    "Makine Mühendisliği",
    "Makine Mühendisliği (M.T.O.K.)",
    "Malzeme Bilimi ve Mühendisliği",
    "Malzeme Bilimi ve Nanoteknoloji Mühendisliği",
    "Malzeme Bilimi ve Teknolojileri",
    "Matematik",
    "Matematik Mühendisliği",
    "Matematik Öğretmenliği",
    "Matematik ve Bilgisayar Bilimleri",
    "Mekatronik Mühendisliği",
    "Mekatronik Mühendisliği (M.T.O.K.)",
    "Metalurji ve Malzeme Mühendisliği",
    "Metalurji ve Malzeme Mühendisliği (M.T.O.K.)",
    "Meteoroloji Mühendisliği",
    "Mimarlık",
    "Moleküler Biyoloji ve Genetik",
    "Moleküler Biyoteknoloji",
    "Mühendislik Programları",
    "Mühendislik ve Doğa Bilimleri Programları",
    "Nanobilim ve Nanoteknoloji",
    "Nanoteknoloji Mühendisliği",
    "Nükleer Enerji Mühendisliği",
    "Odyoloji (Fakülte)",
    "Odyoloji (Yüksekokul)",
    "Optik ve Akustik Mühendisliği",
    "Orman Endüstrisi Mühendisliği",
    "Orman Mühendisliği",
    "Ortez ve Protez",
    "Otomotiv Mühendisliği",
    "Otomotiv Mühendisliği (M.T.O.K.)",
    "Perfüzyon",
    "Petrol ve Doğalgaz Mühendisliği",
    "Peyzaj Mimarlığı",
    "Pilotaj (Fakülte)",
    "Pilotaj (Yüksekokul)",
    "Polimer Malzeme Mühendisliği",
    "Raylı Sistemler Mühendisliği",
    "Robotik ve Otonom Sistemleri Mühendisliği",
    "Siber Güvenlik Mühendisliği",
    "Su Bilimleri ve Mühendisliği",
    "Su Ürünleri Endüstrisi Mühendisliği",
    "Su Ürünleri Mühendisliği",
    "Süt Teknolojisi",
    "Şehir ve Bölge Planlama",
    "Tarım Makineleri ve Teknolojileri Mühendisliği",
    "Tarımsal Biyoteknoloji",
    "Tarımsal Genetik Mühendisliği",
    "Tarımsal Yapılar ve Sulama",
    "Tarla Bitkileri",
    "Tekstil Mühendisliği",
    "Tekstil Mühendisliği (M.T.O.K.)",
    "Tıp",
    "Tohum Bilimi ve Teknolojisi",
    "Toprak Bilimi ve Bitki Besleme",
    "Tütün Eksperliği",
    "Uçak Bakım ve Onarım (Fakülte)",
    "Uçak Bakım ve Onarım (Yüksekokul)",
    "Uçak Elektrik ve Elektroniği",
    "Uçak Gövde ve Motor Bakımı (Fakülte)",
    "Uçak Gövde ve Motor Bakımı (Yüksekokul)",
    "Uçak Mühendisliği",
    "Uzay Bilimleri ve Teknolojileri",
    "Uzay Mühendisliği",
    "Veri Bilimi ve Analitiği",
    "Veterinerlik",
    "Yaban Hayatı Ekolojisi ve Yönetimi",
    "Yapay Zeka Mühendisliği",
    "Yapay Zeka ve Makine Öğrenmesi",
    "Yapay Zeka ve Veri Mühendisliği",
    "Yazılım Geliştirme (Fakülte)",
    "Yazılım Geliştirme (Yüksekokul)",
    "Yazılım Mühendisliği",
    "Yazılım Mühendisliği (M.T.O.K.)",
    "Ziraat Mühendisliği Programları",
    "Zootekni"
]

# Cities (81 total)
CITIES = [
    "ADANA",
    "ADIYAMAN",
    "AFYONKARAHİSAR",
    "AĞRI",
    "AKSARAY",
    "AMASYA",
    "ANKARA",
    "ANTALYA",
    "ARDAHAN",
    "ARTVİN",
    "AYDIN",
    "BALIKESİR",
    "BARTIN",
    "BATMAN",
    "BAYBURT",
    "BİLECİK",
    "BİNGÖL",
    "BİTLİS",
    "BOLU",
    "BURDUR",
    "BURSA",
    "ÇANAKKALE",
    "ÇANKIRI",
    "ÇORUM",
    "DENİZLİ",
    "DİYARBAKIR",
    "DÜZCE",
    "EDİRNE",
    "ELAZIĞ",
    "ERZİNCAN",
    "ERZURUM",
    "ESKİŞEHİR",
    "GAZİANTEP",
    "GİRESUN",
    "GÜMÜŞHANE",
    "HAKKARİ",
    "HATAY",
    "IĞDIR",
    "ISPARTA",
    "İSTANBUL",
    "İZMİR",
    "KAHRAMANMARAŞ",
    "KARABÜK",
    "KARAMAN",
    "KARS",
    "KASTAMONU",
    "KAYSERİ",
    "KIRIKKALE",
    "KIRKLARELİ",
    "KIRŞEHİR",
    "KİLİS",
    "KOCAELİ",
    "KONYA",
    "KÜTAHYA",
    "MALATYA",
    "MANİSA",
    "MARDİN",
    "MERSİN",
    "MUĞLA",
    "MUŞ",
    "NEVŞEHİR",
    "NİĞDE",
    "ORDU",
    "OSMANİYE",
    "RİZE",
    "SAKARYA",
    "SAMSUN",
    "SİİRT",
    "SİNOP",
    "SİVAS",
    "ŞANLIURFA",
    "ŞIRNAK",
    "TEKİRDAĞ",
    "TOKAT",
    "TRABZON",
    "TUNCELİ",
    "UŞAK",
    "VAN",
    "YALOVA",
    "YOZGAT",
    "ZONGULDAK"
]

# University types
UNIVERSITY_TYPES = [
    "Devlet",
    "Vakıf",
    "KKTC",
    "Yurt Dışı"
]

# Fee/Scholarship types
FEE_TYPES = [
    "Ücretsiz",
    "Ücretli",
    "İÖ-Ücretli",
    "Burslu",
    "%50 İndirimli",
    "%25 İndirimli",
    "AÖ-Ücretli",
    "UÖ-Ücretli"
]

# Education types
EDUCATION_TYPES = [
    "Örgün",
    "İkinci",
    "Açıköğretim",
    "Uzaktan"
]

# Fill status types
FILL_STATUS = [
    "Doldu",
    "Doldu#",
    "Dolmadı",
    "Yeni"
]