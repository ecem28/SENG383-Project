# SENG383-Project
## Update Log — Student A
- Added BeePlan implementation files.
- Organized BeePlan folder structure.
- Prepared initial commit history for coding tasks.

---

## KidTask GUI Update — Student A

- Added initial Python GUI using Tkinter.
- Includes Login, Dashboard, Tasks, Wishes, and Progress screens.
- Data saved in JSON files for persistence.
- Next step: integrate parent-child task assignment logic.


  # KidTask — Final Proje (Student A)

KidTask, çocukların görevlerini ve isteklerini takip etmeyi sağlayan bir Tkinter GUI uygulamasıdır.  
Parent ve Teacher görev ekleyebilir, Child görevleri tamamlayıp puan kazanabilir.  
Wishes (istekler) puanla alınır ve parent tarafından onaylanır.

---

## Kurulum

Python 3.10+ ile çalışır. Çalıştırmak için:

```bash
## Video 📽 [Final Sunum Videosu](https://drive.google.com/file/d/1IdtM7Dm0FOJFfyKawfD31iNhTTZdERrd/view?usp=drive_link) 
python main.py
# Default kullanıcılar
ecem — child

veli — parent

teacher — teacher
Senaryo Akışı (Demo)
Parent (veli) login → görev ekler

Child (ecem) login → görevi tamamlar, wish ekler

Parent login → görevi ve wish’i onaylar

Teacher login → görev ekler, tüm çocukların ilerlemesini görür

Child tekrar login → Progress ekranında kendi görev ve wish durumunu görür (APPROVED)
AI Analiz Kartları
İşlem           Kullanılan Araç	                   Prompt	                                                  AI Çıktısı	                    Revizyon
Görev ekleme    	Copilot	                      "Create Tkinter views for parent/teacher to add tasks"	Teacher yetkisi eksikti	        ["parent","teacher"] kontrolü eklendi
Wish onayı	      Copilot	                       "Add wish approval flow"	                               Sadece bilgi mesajı vardı	    update_status("APPROVED") eklendi
Progress görünümü	Copilot	                        "Show tasks/wishes for all children"	                 Sadece child görünüyordu	       Parent/teacher için tüm çocuklar listelendi
Notlar
Kod tek dosyada (main.py) çalışır

data/ klasörü boş bırakılabilir, program çalışınca dosyalar oluşur

GUI ekranları: Login, Dashboard, Tasks, Wishes, Progress

Parent-Child ekranı: görev ve wish onayı için özel görünüm

Puanlar sadece child görev tamamladığında artar, onayda tekrar artmaz

Teacher tüm çocukları görebilir ama wish onayı sadece parent tarafından yapılır
