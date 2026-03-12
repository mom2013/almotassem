# main.py – منبر المسلمين النهائي ملف واحد
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime, timedelta
import requests, tempfile, random

# ====== إعدادات عامة ======
font_size = 26
bg_color = (1,1,1,1)
text_color = (0,0,0,1)
Window.clearcolor = bg_color

# ====== الأصوات من مجلد audio/ ======
sound_fajr = SoundLoader.load("audio/fajr_alarm.mp3")               
sound_other = SoundLoader.load("audio/adhan_masjid.mp3")            
sound_before_adhan = SoundLoader.load("audio/before_adhan.mp3")     
sound_reminder = SoundLoader.load("audio/salawat.mp3")              

def play_fajr_alarm(*args):
    if sound_fajr: sound_fajr.play()
def play_other_adhan(*args):
    if sound_other: sound_other.play()
def play_before_adhan(*args):
    if sound_before_adhan: sound_before_adhan.play()
def play_reminder(*args):
    if sound_reminder: sound_reminder.play()

# ====== الأذكار ======
azkar_sabah = ["سبحان الله","الحمد لله","لا إله إلا الله","الله أكبر","أستغفر الله","اللهم صل وسلم على نبينا محمد"]
azkar_masa = ["اللهم بك أمسينا وبك أصبحنا","سبحان الله وبحمده","أعوذ بكلمات الله التامة"]
azkar_nawm = ["باسمك اللهم أموت وأحيا","أعوذ بكلمات الله التامة","آية الكرسي"]

# ====== القرآن والسور ======
quran_readers = ["ar.alafasy","ar.abdulbasetmurattal","ar.shaatree","ar.yaserdosari","ar.husary","ar.saadghamdi"]

def get_surah_list():
    r = requests.get("https://api.alquran.cloud/v1/surah").json()
    if r["code"] == 200: return r["data"]
    return []

def play_quran_audio(surah_num, reciter="ar.alafasy"):
    try:
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".mp3")
        data = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_num}/{reciter}").content
        tf.write(data); tf.close()
        sound = SoundLoader.load(tf.name)
        if sound: sound.play()
    except Exception as e:
        print("Error:", e)

# ====== البيانات المضمّنة ======
hadiths = [
    "عن أبي هريرة رضي الله عنه قال: قال رسول الله ﷺ: «من صلى علي واحدة صلى الله عليه عشرًا»",
    "عن أنس بن مالك رضي الله عنه قال: قال رسول الله ﷺ: «لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه»",
    "عن عبدالله بن عباس رضي الله عنهما: «خيركم من تعلم القرآن وعلمه»"
]
stories = [
    "قصة النبي محمد ﷺ: حياته المباركة منذ ولادته حتى الهجرة.",
    "قصة أبو بكر الصديق رضي الله عنه: وفاته وأعماله بعد النبي ﷺ.",
    "قصة عمر بن الخطاب رضي الله عنه: عدله وحكمه في الإسلام.",
    "قصة صلاح الدين الأيوبي: تحرير القدس وفضائل أعماله."
]
jokes = [
    "نكتة 1: لماذا لا يلعب الحاسوب كرة القدم؟ لأنه يخاف من الفيروسات 😂",
    "نكتة 2: لماذا الحاسوب حزين؟ لأنه عنده مشكلة في WINDOWS 😅",
    "نكتة 3: لماذا المطورون يحبون القهوة؟ لأنها توقفهم عن النوم أثناء الكود ☕"
]
hikma = [
    "الحكمة 1: الصبر مفتاح الفرج.",
    "الحكمة 2: العلم نور والجهل ظلام.",
    "الحكمة 3: من جدّ وجد ومن زرع حصد."
]

# ====== التطبيق ======
class ManbarMusliminApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation="vertical", spacing=5, padding=5)
        
        # ====== إعدادات عامة ======
        settings_layout = GridLayout(cols=3, size_hint_y=None, height=80)
        settings_layout.add_widget(Button(text="🌙 الوضع الليلي", on_press=lambda x: self.toggle_dark_mode()))
        settings_layout.add_widget(Button(text="🎨 تغيير الألوان", on_press=lambda x: self.change_colors()))
        settings_layout.add_widget(Button(text="🔄 إعادة جدولة الأصوات", on_press=lambda x: self.schedule_prayers_sounds()))
        self.root_layout.add_widget(settings_layout)

        # ====== أذكار ======
        azkar_layout = GridLayout(cols=2, size_hint_y=None, height=80)
        azkar_layout.add_widget(Button(text="📿 أذكار الصباح", on_press=lambda x: self.show_azkar(azkar_sabah)))
        azkar_layout.add_widget(Button(text="📿 أذكار المساء", on_press=lambda x: self.show_azkar(azkar_masa)))
        azkar_layout.add_widget(Button(text="📿 أذكار قبل النوم", on_press=lambda x: self.show_azkar(azkar_nawm)))
        self.root_layout.add_widget(azkar_layout)

        # ====== القرآن ======
        quran_layout = GridLayout(cols=2, size_hint_y=None, height=80)
        quran_layout.add_widget(Button(text="📖 فهرس السور", on_press=lambda x: self.show_surah_list()))
        quran_layout.add_widget(Button(text="🎧 تشغيل الفاتحة", on_press=lambda x: play_quran_audio(1)))
        quran_layout.add_widget(Button(text="🔍 بحث في القرآن", on_press=lambda x: self.search_quran()))
        self.root_layout.add_widget(quran_layout)

        # ====== الأحاديث والقصص ======
        extra_layout = GridLayout(cols=2, size_hint_y=None, height=80)
        extra_layout.add_widget(Button(text="📜 حديث اليوم", on_press=lambda x: self.show_hadith_today()))
        extra_layout.add_widget(Button(text="💡 حكمة اليوم", on_press=lambda x: self.show_hikma_today()))
        extra_layout.add_widget(Button(text="😂 نكتة اليوم", on_press=lambda x: self.show_joke_today()))
        extra_layout.add_widget(Button(text="📖 قصص دينية", on_press=lambda x: self.show_stories()))
        extra_layout.add_widget(Button(text="🎮 لعبة الشجرة", on_press=lambda x: self.show_tree_game()))
        self.root_layout.add_widget(extra_layout)

        # ====== إضافات misc ======
        misc_layout = GridLayout(cols=2, size_hint_y=None, height=80)
        misc_layout.add_widget(Button(text="🕌 مواقيت الصلاة", on_press=lambda x: self.show_prayer_times()))
        misc_layout.add_widget(Button(text="🧭 بوصلة القبلة", on_press=lambda x: self.show_qibla()))
        misc_layout.add_widget(Button(text="📿 مسبحة إلكترونية", on_press=lambda x: self.show_misbah()))
        misc_layout.add_widget(Button(text="📅 التقويم الهجري", on_press=lambda x: self.show_hijri_calendar()))
        misc_layout.add_widget(Button(text="⭐ قيمنا", on_press=lambda x: self.rate_app()))
        misc_layout.add_widget(Button(text="👤 نبذة عن المبرمج", on_press=lambda x: self.show_info()))
        self.root_layout.add_widget(misc_layout)

        # ====== بدء جدولة الأصوات تلقائيًا ======
        self.schedule_prayers_sounds()

        return self.root_layout

    # ====== دوال misc ======
    def toggle_dark_mode(self):
        global bg_color, text_color
        if Window.clearcolor == (1,1,1,1):
            bg_color = (0.05,0.05,0.05,1)
            text_color = (1,1,1,1)
        else:
            bg_color = (1,1,1,1)
            text_color = (0,0,0,1)
        Window.clearcolor = bg_color

    def change_colors(self):
        global bg_color, text_color
        bg_color = (random.random(), random.random(), random.random(), 1)
        text_color = (random.random(), random.random(), random.random(),1)
        Window.clearcolor = bg_color

    def show_azkar(self, azkar_list):
        box = BoxLayout(orientation="vertical", size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        for z in azkar_list:
            label = Label(text=z, font_size=font_size, color=text_color, size_hint_y=None, height=80)
            box.add_widget(label)
        scroll = ScrollView()
        scroll.add_widget(box)
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(scroll)

    def show_surah_list(self):
        surahs = get_surah_list()
        box = GridLayout(cols=1, size_hint_y=None, spacing=5)
        box.bind(minimum_height=box.setter("height"))
        for s in surahs:
            btn = Button(text=f"{s['number']} - {s['englishName']}", size_hint_y=None, height=80)
            btn.bind(on_press=lambda x, n=s['number']: self.open_surah(n))
            box.add_widget(btn)
        scroll = ScrollView()
        scroll.add_widget(box)
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(scroll)

    def open_surah(self, number):
        r = requests.get(f"https://api.alquran.cloud/v1/surah/{number}").json()
        ayat = r["data"]["ayahs"]
        box = BoxLayout(orientation="vertical", size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        for a in ayat:
            ayah = f"{a['text']} ۝{a['numberInSurah']}"
            label = Label(text=ayah, font_size=font_size, color=text_color, size_hint_y=None, height=120)
            box.add_widget(label)
        scroll = ScrollView()
        scroll.add_widget(box)
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(scroll)

    def search_quran(self):
        box = BoxLayout(orientation="vertical")
        txt = TextInput(hint_text="اكتب اسم السورة أو كلمة", multiline=False)
        btn = Button(text="بحث", size_hint_y=None, height=50)
        box.add_widget(txt)
        box.add_widget(btn)
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(box)

    def show_hadith_today(self):
        self.show_popup("حديث اليوم", random.choice(hadiths))

    def show_hikma_today(self):
        self.show_popup("حكمة اليوم", random.choice(hikma))

    def show_joke_today(self):
        self.show_popup("نكته اليوم", random.choice(jokes))

    def show_stories(self):
        self.show_popup("قصص دينية", random.choice(stories))

    def show_tree_game(self):
        box = GridLayout(cols=3, spacing=5, size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        items = [
            {"type":"nabi","name":"محمد ﷺ","desc":"آخر الأنبياء"},
            {"type":"asma","name":"الرحمن","desc":"اسم من أسماء الله الحسنى"},
            {"type":"tajweed","name":"مد","desc":"حكم التجويد"}
        ]
        for item in items:
            btn = Button(text=item["name"], size_hint_y=None, height=80)
            btn.bind(on_press=lambda x, i=item: self.show_popup(i["name"], i["desc"]))
            box.add_widget(btn)
        scroll = ScrollView()
        scroll.add_widget(box)
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(scroll)

    # ====== misc ======
    def show_prayer_times(self):
        city = "Tripoli"
        country = "Libya"
        r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2").json()
        if r["code"] == 200:
            times = r["data"]["timings"]
            content = "\n".join([f"{k}: {v}" for k,v in times.items()])
        else:
            content = "خطأ في جلب مواقيت الصلاة"
        self.show_popup("مواقيت الصلاة", content)

    def show_qibla(self):
        self.show_popup("بوصلة القبلة","اتجه نحو القبلة بناءً على التطبيق")

    def show_misbah(self):
        self.show_popup("مسبحة إلكترونية","اضغط على العدادات لتسبيح")

    def show_hijri_calendar(self):
        self.show_popup("التقويم الهجري","اليوم 10 رجب 1447 هـ")

    def rate_app(self):
        self.show_popup("قيمنا","ضع تقييمك على المتجر")

    def show_info(self):
        info = "الاسم: محمد المعتصم شمس الدين\nالعمر: 13 سنة\nالسلام عليكم ورحمة الله وبركاته\nنرجو نشر التطبيق ولكم الأجر إن شاء الله"
        self.show_popup("نبذة عن المبرمج", info)

    # ====== Popup عام ======
    def show_popup(self, title, content):
        box = BoxLayout(orientation="vertical")
        lbl = Label(text=content)
        btn = Button(text="إغلاق", size_hint_y=None, height=50)
        box.add_widget(lbl)
        box.add_widget(btn)
        popup = Popup(title=title, content=box, size_hint=(0.9,0.5))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    # ====== جدولة الأصوات التلقائية ======
    def schedule_prayers_sounds(self):
        city = "Tripoli"
        country = "Libya"
        try:
            r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2").json()
            if r["code"] == 200:
                timings = r["data"]["timings"]
                now = datetime.now()
                for prayer, time_str in timings.items():
                    h, m = map(int, time_str.split(":"))
                    prayer_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
                    if prayer_time < now:
                        prayer_time += timedelta(days=1)
                    if prayer.lower() == "fajr":
                        Clock.schedule_once(lambda dt: play_fajr_alarm(), (prayer_time - now).total_seconds())
                        # قبل الأذان بدقيقتين
                        before_time = prayer_time - timedelta(minutes=2)
                        Clock.schedule_once(lambda dt: play_before_adhan(), (before_time - now).total_seconds())
                    else:
                        Clock.schedule_once(lambda dt: play_other_adhan(), (prayer_time - now).total_seconds())
        except Exception as e:
            print("Error scheduling prayers:", e)
        Clock.schedule_interval(play_reminder, 300)

if _name_ == "_main_":
    ManbarMusliminApp().run()