import flet as ft
import traceback

def main(page: ft.Page):
    try:
        # Усі імпорти робимо всередині, щоб спіймати ModuleNotFoundError
        import sqlite3
        from datetime import datetime
        import os
        import shutil
        import tempfile
        import json
        import time
        import base64
        import requests

        # ==========================================
        # 📚 БАЗА ДАНИХ
        # ==========================================
        NAKAZ_28_DB = {
            "сибірка": "НАКАЗ 28: КАТЕГОРИЧНО ЗАБОРОНЕНО випуск! Тушу з органами спалюють...",
            "сказ": "НАКАЗ 28: Забій заборонено. Тушу та всі органи знищують.",
            "правець": "НАКАЗ 28: Забій заборонено. Тушу та органи утилізують.",
            "отруєння": "НАКАЗ 28: Забій тварин у стані агонії від отруєння заборонено."
            # Я скоротив словник ТІЛЬКИ для тесту помилки, щоб код був коротшим.
            # Потім ми повернемо весь ваш словник хвороб.
        }

        page.title = "VetAI Pro (X-Ray Mode)"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.scroll = ft.ScrollMode.ADAPTIVE
        page.window_width = 400
        page.window_height = 800
        page.padding = 10
        
        CURRENT_LANG = ["UA"]
        active_shift = {"id": None, "batch": "", "total": 0, "current": 1}

        # === МОБІЛЬНІ ШЛЯХИ ТА БАЗА ===
        safe_dir = os.environ.get("FLET_APP_STORAGE", ".") 
        DB_NAME = os.path.join(safe_dir, "vet_mobile.db")
        PHOTOS_DIR = os.path.join(safe_dir, "photos")
        DOWNLOADS_DIR = "/storage/emulated/0/Download"
        if not os.path.exists(DOWNLOADS_DIR): DOWNLOADS_DIR = safe_dir
        if not os.path.exists(PHOTOS_DIR): os.makedirs(PHOTOS_DIR, exist_ok=True)

        conn = sqlite3.connect(DB_NAME)
        conn.execute('''CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, enterprise TEXT, farm TEXT, 
            type TEXT, count INTEGER, vet TEXT, temp TEXT, status TEXT DEFAULT 'OPEN',
            final_notes TEXT, final_photo TEXT, doc_vet TEXT, doc_waybill TEXT, doc_chain TEXT, doc_thermal TEXT, culled_kg TEXT, animal_ids TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT, shift_id INTEGER, batch TEXT, num INTEGER, 
            organ TEXT, status TEXT, time TEXT, photo TEXT, diagnosis TEXT, ai_result TEXT, orders_action TEXT, notes TEXT)''')
        conn.commit()
        conn.close()

        page.add(
            ft.Text("✅ СИСТЕМА ЗАПУЩЕНА УСПІШНО!", color="green", size=24, weight="bold"),
            ft.Text("Якщо ви бачите цей текст, значить помилок при старті немає. Можемо повертати повний код.", size=16)
        )
        page.update()

    except Exception as e:
        # ЯКЩО ЩОСЬ ВПАДЕ - ВИ ПОБАЧИТЕ ЦЕ НА ЕКРАНІ
        page.clean()
        page.scroll = ft.ScrollMode.ADAPTIVE
        page.add(
            ft.Text("❌ КРИТИЧНА ПОМИЛКА:", color="red", weight="bold", size=24),
            ft.Text(traceback.format_exc(), selectable=True, size=14, color="black"),
            ft.Text("Зробіть скріншот цього екрану!", weight="bold", size=16, color="blue")
        )
        page.update()

ft.app(target=main)
