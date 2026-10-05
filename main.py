import base64
import requests
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

PASSWORD = "148923"
API_KEY = "AQ.Ab8RN6LKtId-iEqkiXDyItTmojNHKeu2Jy8HJCiXOTfg7vaUGA"
WHATSAPP_LINK = "https://wa.me/Saidelmohitat7"

PROMPT = """
أنت معلم أول رياضيات خبير لمنهج الصف الأول الثانوي المصري (النظام العربي القديم).
المطلوب منك حل المسألة المرفقة بالبرهان العربي الكامل:
- الفرع واسم الدرس.
- المعطيات والمطلوب.
- خطوات البرهان بـ (∵ بما أن) و (∴ إذاً).
- الرموز عربية خالصة: س، ص، ت، جا، جتا، ظا، أ ب جـ.
- مجموعة الحل النهائية م . ح.
"""

class SayedElMoheetatApp(App):
    def build(self):
        self.title = "سيد المحيطات رياضة أولى ثانوي"
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        self.dev_lbl = Label(text="★ المطور: سيد المحيطات ★", font_size='18sp', color=(0.2, 0.7, 1, 1), size_hint_y=None, height=35)
        self.layout.add_widget(self.dev_lbl)

        self.title_lbl = Label(text="سيد المحيطات رياضة أولى ثانوي", font_size='18sp', size_hint_y=None, height=45)
        self.layout.add_widget(self.title_lbl)
        
        self.pwd_input = TextInput(hint_text="أدخل كلمة المرور (148923)", password=True, multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.pwd_input)
        
        self.btn_login = Button(text="تسجيل الدخول", size_hint_y=None, height=50, background_color=(0, 0.7, 0.3, 1))
        self.btn_login.bind(on_press=self.check_login)
        self.layout.add_widget(self.btn_login)
        
        self.btn_support = Button(text="💬 تواصل واتساب مع المطور (خدمة العملاء)", size_hint_y=None, height=45, background_color=(0.15, 0.68, 0.38, 1))
        self.btn_support.bind(on_press=self.open_whatsapp)
        self.layout.add_widget(self.btn_support)
        
        return self.layout

    def check_login(self, instance):
        if self.pwd_input.text.strip() == PASSWORD:
            self.show_solver_screen()
        else:
            self.title_lbl.text = "❌ كلمة المرور غير صحيحة!"

    def open_whatsapp(self, instance):
        webbrowser.open(WHATSAPP_LINK)

    def show_solver_screen(self):
        self.layout.clear_widgets()
        
        self.layout.add_widget(Label(text="★ المطور: سيد المحيطات ★", font_size='18sp', color=(0.2, 0.7, 1, 1), size_hint_y=None, height=35))
        self.layout.add_widget(Label(text="ضع مسار صورة المسألة:", font_size='15sp', size_hint_y=None, height=35))
        
        self.img_input = TextInput(hint_text="/sdcard/math.jpg", multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.img_input)
        
        self.btn_solve = Button(text="حل المسألة بالبرهان العربي 🚀", size_hint_y=None, height=50, background_color=(0.1, 0.5, 0.9, 1))
        self.btn_solve.bind(on_press=self.solve_image)
        self.layout.add_widget(self.btn_solve)

        self.btn_support2 = Button(text="💬 الدعم الفني وخدمة العملاء (واتساب)", size_hint_y=None, height=40, background_color=(0.15, 0.68, 0.38, 1))
        self.btn_support2.bind(on_press=self.open_whatsapp)
        self.layout.add_widget(self.btn_support2)
        
        self.scroll = ScrollView()
        self.res_lbl = Label(text="", size_hint_y=None, font_size='16sp')
        self.res_lbl.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.scroll.add_widget(self.res_lbl)
        self.layout.add_widget(self.scroll)

    def solve_image(self, instance):
        path = self.img_input.text.strip()
        self.res_lbl.text = "⏳ جاري قراءة المسألة واستخراج البرهان..."
        try:
            with open(path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
            payload = {
                "contents": [{
                    "parts": [
                        {"text": PROMPT},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                    ]
                }]
            }
            res = requests.post(url, json=payload).json()
            solution = res["candidates"][0]["content"]["parts"][0]["text"]
            self.res_lbl.text = solution
        except Exception as e:
            self.res_lbl.text = f"❌ خطأ: تأكد من صحة مسار الصورة ({e})"

if __name__ == '__main__':
    SayedElMoheetatApp().run()
      
