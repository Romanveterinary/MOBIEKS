import traceback

try:
    import flet as ft
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
    # 📚 ПОВНА ОФЛАЙН БАЗА ДАНИХ (НАКАЗ 28 + НАКАЗ 1032)
    # ==========================================
    NAKAZ_28_DB = {
        "сибірка": "НАКАЗ 28: КАТЕГОРИЧНО ЗАБОРОНЕНО випуск! Тушу з органами спалюють. Дезінфекція. [❗️Наказ 1032 (діє з 03.2027): М'ясо визнається повністю непридатним для споживання].",
        "сказ": "НАКАЗ 28: Забій заборонено. Тушу та всі органи знищують. [❗️Наказ 1032 (діє з 03.2027): Повна утилізація].",
        "правець": "НАКАЗ 28: Забій заборонено. Тушу та органи утилізують. [❗️Наказ 1032 (діє з 03.2027): Повна утилізація].",
        "ботулізм": "НАКАЗ 28: Забій заборонено. Тушу та органи утилізують.",
        "туберкульоз": "НАКАЗ 28: Локалізований - уражений орган утилізують, тушу на проварку/ковбаси. Генералізований (виснаження) - тушу та всі органи на утилізацію. [❗️Наказ 1032: М'ясо непридатне, якщо уражено більше одного органу].",
        "бруцельоз": "НАКАЗ 28: М'ясо на проварку. Вим'я, внутрішні органи та кров - на технічну утилізацію.",
        "ящур": "НАКАЗ 28: М'ясо випускають після проварки. Кістки, кров та уражені органи - утилізують.",
        "пастерельоз": "НАКАЗ 28: Без виснаження - органи утилізують, тушу на проварку. З виснаженням - утилізація всієї туші.",
        "сальмонельоз": "НАКАЗ 28: Внутрішні органи утилізують. Тушу обов'язково направляють на проварку.",
        "лептоспіроз": "НАКАЗ 28: При жовтяниці/виснаженні - утилізація всієї туші. Без жовтяниці - проварка.",
        "лістеріоз": "НАКАЗ 28: Уражені органи (особливо голову) утилізують. Тушу на проварку.",
        "ку-лихоманка": "НАКАЗ 28: М'ясо на проварку, органи утилізують.",
        "чума врх": "НАКАЗ 28: Всю тушу та органи утилізують. Жорсткий карантин. [❗️Наказ 1032 (діє з 03.2027): М'ясо непридатне].",
        "лейкоз": "НАКАЗ 28: При пухлинах у м'язах/лімфовузлах - туша і органи утилізуються. При змінах лише в окремих органах - органи утилізують, тушу на проварку.",
        "емфізематозний карбункул": "НАКАЗ 28 (Емкар): Забій заборонено. Утилізація всієї туші зі шкірою (спалювання).",
        "паратуберкульоз": "НАКАЗ 28: При виснаженні - утилізація. Без виснаження - органи утилізують, тушу випускають без обмежень.",
        "цистицеркоз": "НАКАЗ 28 (Фіноз): Більше 3 фінок на 40 кв.см - тушу та органи на утилізацію. Менше 3 - знешкодження (заморожування/проварка). [❗️Наказ 1032: При виявленні хоча б однієї фіни застосовуються жорсткі обмеження].",
        "фасціольоз": "НАКАЗ 28: Уражену печінку зачищають/утилізують. Тушу випускають.",
        "диктіокаульоз": "НАКАЗ 28: Легені утилізують. Тушу випускають.",
        "ачс": "НАКАЗ 28 (Африканська чума свиней): Утилізація (спалювання) всієї туші та органів. Карантин. [❗️Наказ 1032 (діє з 03.2027): М'ясо непридатне].",
        "чума свиней": "НАКАЗ 28 (Класична чума): Всю тушу та органи на технічну утилізацію.",
        "бешиха": "НАКАЗ 28 (Рожа): Шкірні плями - зачистка шкіри, тушу на проварку. Септична форма - утилізація всієї туші.",
        "хвороба ауєскі": "НАКАЗ 28: Внутрішні органи та голову утилізують. Тушу на проварку.",
        "трихінельоз": "НАКАЗ 28 (Трихінелоскопія): При виявленні хоча б однієї трихінели - ТУША ТА ОРГАНИ ПІДЛЯГАЮТЬ УТИЛІЗАЦІЇ! [❗️Наказ 1032 (діє з 03.2027): Обов'язковий європейський контроль кожної туші].",
        "аскаридоз": "НАКАЗ 28: Уражені частини печінки/легень зачищають або утилізують. М'ясо випускають.",
        "сап": "НАКАЗ 28: КАТЕГОРИЧНО ЗАБОРОНЕНО забій! Утилізація разом зі шкірою. [❗️Наказ 1032: М'ясо непридатне].",
        "інак": "НАКАЗ 28 (Інфекційна анемія коней): При клінічних ознаках - утилізація. При позитивній реакції без ознак - забій ізольовано, м'ясо на проварку.",
        "мит коней": "НАКАЗ 28: Гнійники зачищають, уражені органи утилізують, тушу випускають.",
        "меланосаркома": "НАКАЗ 28: При множинних метастазах тушу утилізують.",
        "ньюкасла": "НАКАЗ 28 (Хвороба Ньюкасла): Утилізація всієї туші та органів.",
        "грип птиці": "НАКАЗ 28: Забій хворої птиці заборонено. Знищення.",
        "пулороз": "НАКАЗ 28: Змінені органи утилізують. Тушу на проварку.",
        "кокцидіоз": "НАКАЗ 28: При виснаженні - утилізація. Без виснаження - органи утилізують, тушу випускають.",
        "хвороба марека": "НАКАЗ 28: Туші та органи від хворої птиці підлягають утилізації.",
        "інфекційна агалактія": "НАКАЗ 28: Уражене вим'я утилізують. Тушу на проварку.",
        "брадзот": "НАКАЗ 28: Забій заборонено. Туші утилізують (спалюють).",
        "ентеротоксемія": "НАКАЗ 28: Забій заборонено. Утилізація.",
        "віспа": "НАКАЗ 28: При доброякісній формі - зачистка і проварка. При зливній - утилізація.",
        "міксоматоз": "НАКАЗ 28: Забій хворих заборонено. Туші разом зі шкуркою спалюють.",
        "вгхк": "НАКАЗ 28 (Геморагічна хвороба кролів): Утилізація всієї туші та органів.",
        "гемоаспірація": "НАКАЗ 28: При потраплянні крові в дихальні шляхи (гемоаспірація) під час забою - легені утилізують на технічні цілі. При відсутності інших патологій тушу випускають без обмежень.",
        "пневмонія": "НАКАЗ 28 (Запалення легень): Легені утилізують. При відсутності сепсису в інших органах, тушу випускають.",
        "абсцес": "НАКАЗ 28: Гнійник акуратно вирізають і утилізують. [❗️Наказ 1032 (діє з 03.2027): М'ясо з множинними абсцесами визнається непридатним].",
        "флегмона": "НАКАЗ 28: При великих ураженнях і запаленні лімфовузлів - тушу утилізують.",
        "жовтяниця": "НАКАЗ 28: Якщо жовте забарвлення не зникає протягом 2 діб остигання - тушу утилізують.",
        "виснаження": "НАКАЗ 28: Утилізація всієї туші (при наявності драглистого набряку тканин або атрофії м'язів).",
        "урія": "НАКАЗ 28 (Запах сечі): Тушу провітрюють 48 годин. Якщо запах залишається - утилізація.",
        "отруєння": "НАКАЗ 28: Забій тварин у стані агонії від отруєння заборонено. Туша непридатна. [❗️Наказ 1032: Сувора заборона]."
    }

    def main(page: ft.Page):
        page.title = "VetAI Pro v16.9 (Global)"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.scroll = ft.ScrollMode.ADAPTIVE
        page.window_width = 400
        page.window_height = 800
        page.padding = 10
        
        CURRENT_LANG = ["UA"]
        active_shift = {"id": None, "batch": "", "total": 0, "current": 1}

        def show_snack(msg, color="green"):
            page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=color)
            page.snack_bar.open = True
            page.update()

        # ⚙️ НАЛАШТУВАННЯ API КЛЮЧА
        DEFAULT_API_KEY = "AIzaSyCoi5-6zcMFWW6aB5Gul6dPm5i1frn_EFI"
        
        tf_api_key = ft.TextField(
            label="Google Gemini API Key",
            value=page.client_storage.get("api_key") or DEFAULT_API_KEY, 
            password=True,
            can_reveal_password=True,
            width=300
        )

        def close_settings(e=None):
            dlg_settings.open = False
            page.update()

        def save_api_key(e):
            new_key = tf_api_key.value.strip()
            page.client_storage.set("api_key", new_key) 
            close_settings()
            show_snack("✅ Ключ API успішно збережено!", "green")

        dlg_settings = ft.AlertDialog(
            title=ft.Text("⚙️ Налаштування API", weight="bold"),
            content=ft.Column([
                ft.Text("Вставте ваш новий ключ доступу від Google Gemini:", size=12, color="grey"),
                tf_api_key
            ], tight=True),
            actions=[
                ft.TextButton("Скасувати", on_click=close_settings),
                ft.ElevatedButton("ЗБЕРЕГТИ", on_click=save_api_key, bgcolor="blue", color="white")
            ]
        )

        def open_settings(e):
            tf_api_key.value = page.client_storage.get("api_key") or DEFAULT_API_KEY
            page.dialog = dlg_settings
            dlg_settings.open = True
            page.update()

        btn_settings = ft.IconButton(icon=ft.icons.SETTINGS, icon_color="grey", tooltip="Налаштування ШІ", on_click=open_settings)

        # === МОБІЛЬНІ ШЛЯХИ ===
        safe_dir = os.environ.get("FLET_APP_STORAGE", ".") 
        DB_NAME = os.path.join(safe_dir, "vet_mobile.db")
        PHOTOS_DIR = os.path.join(safe_dir, "photos")
        DOWNLOADS_DIR = "/storage/emulated/0/Download"
        if not os.path.exists(DOWNLOADS_DIR): DOWNLOADS_DIR = safe_dir
        if not os.path.exists(PHOTOS_DIR): os.makedirs(PHOTOS_DIR, exist_ok=True)

        # ІНІЦІАЛІЗАЦІЯ ФАЙЛОВИХ МЕНЕДЖЕРІВ
        fp_docs = ft.FilePicker()
        fp_photo = ft.FilePicker()
        fp_final = ft.FilePicker()
        fp_chat_image = ft.FilePicker() 
        
        page.overlay.extend([fp_docs, fp_photo, fp_final, fp_chat_image])
        page.update()

        # --- БАЗА ДАНИХ ---
        conn = sqlite3.connect(DB_NAME)
        conn.execute('''CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, enterprise TEXT, farm TEXT, 
            type TEXT, count INTEGER, vet TEXT, temp TEXT, status TEXT DEFAULT 'OPEN',
            final_notes TEXT, final_photo TEXT, doc_vet TEXT, doc_waybill TEXT, doc_chain TEXT, doc_thermal TEXT, culled_kg TEXT, animal_ids TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT, shift_id INTEGER, batch TEXT, num INTEGER, 
            organ TEXT, status TEXT, time TEXT, photo TEXT, diagnosis TEXT, ai_result TEXT, orders_action TEXT, notes TEXT)''')
        try: conn.execute("ALTER TABLE shifts ADD COLUMN doc_thermal TEXT")
        except: pass
        try: conn.execute("ALTER TABLE shifts ADD COLUMN culled_kg TEXT")
        except: pass
        try: conn.execute("ALTER TABLE shifts ADD COLUMN final_photo TEXT")
        except: pass
        conn.commit(); conn.close()

        def get_img_base64(path):
            if not path or not os.path.exists(path): return ""
            try:
                with open(path, "rb") as f: return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
            except: return ""

        # ==========================================
        # 🤖 ЛЕГКІ ШІ-АГЕНТИ ЧЕРЕЗ REST API
        # ==========================================
        def ask_ai_opinion(image_paths, user_desc, organ):
            try:
                current_api_key = page.client_storage.get("api_key") or DEFAULT_API_KEY
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={current_api_key}"
                
                parts = []
                for path in image_paths:
                    with open(path, "rb") as f:
                        b64_data = base64.b64encode(f.read()).decode("utf-8")
                        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64_data}})
                
                lang_instruction = "Обов'язково відповідай АНГЛІЙСЬКОЮ мовою (Respond in English)." if CURRENT_LANG[0] == "EN" else "Відповідай УКРАЇНСЬКОЮ мовою."
                prompt = f"""УВАГА: Ти — державний ветеринарно-санітарний експерт. Тобі ЗАБОРОНЕНО аналізувати фото, що не стосуються ветеринарії.
                Якщо фото не по темі - поверни JSON: {{"diagnosis": "БЛОКУВАННЯ", "analysis": "Запит не стосується ветеринарії.", "orders": "Відмова."}}
                Якщо по темі: Проаналізуй фото. Орган: {organ}. Опис: {user_desc}. База: Наказ №28.
                {lang_instruction}
                Поверни JSON: "diagnosis", "analysis", "orders"."""
                
                parts.append({"text": prompt})
                
                payload = {
                    "contents": [{"parts": parts}],
                    "generationConfig": {"responseMimeType": "application/json"}
                }
                
                resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
                if resp.status_code != 200:
                    return {"diagnosis": "Error API", "analysis": str(resp.text), "orders": "-"}
                    
                raw_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                raw_text = raw_text.strip().replace("```json", "").replace("```", "")
                return json.loads(raw_text)
            except Exception as e: 
                return {"diagnosis": "Error", "analysis": str(e), "orders": "-"}

        def ask_ai_consultant_multimodal(question, chat_image_path=None):
            try:
                current_api_key = page.client_storage.get("api_key") or DEFAULT_API_KEY
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={current_api_key}"
                
                lang_instruction = "Respond in English." if CURRENT_LANG[0] == "EN" else "Відповідай українською."
                prompt = f"Ти ветеринарний ШІ-Консультант. Допоможи лікарю з цим питанням: '{question}'. {lang_instruction}"
                
                parts = []
                if chat_image_path and os.path.exists(chat_image_path):
                    prompt += " Також проаналізуй додане фото зразка."
                    with open(chat_image_path, "rb") as f:
                        b64_data = base64.b64encode(f.read()).decode("utf-8")
                        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64_data}})
                
                parts.append({"text": prompt})
                
                payload = {"contents": [{"parts": parts}]}
                resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
                
                if resp.status_code != 200:
                    return f"Помилка API: {resp.text}"
                    
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e: 
                return f"Помилка: {str(e)}"

        # --- КАМЕРА ДОКУМЕНТІВ ---
        doc_paths = {"vet": None, "waybill": None, "chain": None, "thermal": None}
        cur_doc_type = [None]
        lbl_doc_vet = ft.Text("❌", color="red", size=14)
        lbl_doc_waybill = ft.Text("❌", color="red", size=14)
        lbl_doc_chain = ft.Text("❌", color="red", size=14)
        lbl_doc_thermal = ft.Text("❌", color="grey", size=14)

        def on_doc_photo(e):
            if e.files:
                dtype = cur_doc_type[0]
                new_path = os.path.join(PHOTOS_DIR, f"DOC_{dtype.upper()}_{datetime.now().strftime('%H%M%S')}.jpg")
                shutil.copy(e.files[0].path, new_path)
                doc_paths[dtype] = new_path
                msg = "✅ Done" if CURRENT_LANG[0] == "EN" else "✅ Додано"
                if dtype == "vet": lbl_doc_vet.value, lbl_doc_vet.color = msg, "green"
                elif dtype == "waybill": lbl_doc_waybill.value, lbl_doc_waybill.color = msg, "green"
                elif dtype == "chain": lbl_doc_chain.value, lbl_doc_chain.color = msg, "green"
                elif dtype == "thermal": lbl_doc_thermal.value, lbl_doc_thermal.color = msg, "green"
                page.update()
                
        fp_docs.on_result = on_doc_photo
        def snap_doc(dtype): cur_doc_type[0] = dtype; fp_docs.pick_files()

        # --- РЕЄСТРАЦІЯ ---
        switch_lang = ft.Switch(label="🇺🇦 УКР / 🇬🇧 ENG Mode", value=False)
        tf_ent = ft.TextField(label="Підприємство", value="ФОП Стельмах В.Д.")
        tf_farm = ft.TextField(label="Партія / Постачальник", value="ПП Аграрна технологія")
        tf_count = ft.TextField(label="Кількість голів", value="5", keyboard_type=ft.KeyboardType.NUMBER)
        tf_animal_ids = ft.TextField(label="Груповий номер", multiline=True, min_lines=1)
        tf_vet = ft.TextField(label="Лікар", value="Шутяк Р.В.")
        tf_temp = ft.TextField(label="Температура тіла", value="В нормі, 38,0 - 38,5 °C")
        tf_type = ft.Dropdown(label="Вид тварин", options=[ft.dropdown.Option(x) for x in ["Свині", "ВРХ", "ДРХ", "Птиця", "Коні"]], value="Свині")
        
        btn_tab_reg = ft.ElevatedButton("📝 СТАРТ")
        btn_tab_work = ft.ElevatedButton("🔨 РОБОТА")
        btn_tab_chat = ft.ElevatedButton("💬 ШІ-ЧАТ")
        
        lbl_status = ft.Text("Немає активної партії", size=18, weight="bold", color="red")
        lv_hist = ft.ListView(height=350, spacing=10)
        
        btn_norm = ft.ElevatedButton("✅ НОРМА", style=ft.ButtonStyle(bgcolor="green", color="white"), width=340, height=60, on_click=lambda e: save_norm())
        btn_bad = ft.ElevatedButton("🛑 ПАТОЛОГІЯ", style=ft.ButtonStyle(bgcolor="red", color="white"), width=340, height=60)
        btn_close = ft.ElevatedButton("🔒 ЗАКРИТИ ПАРТІЮ", style=ft.ButtonStyle(bgcolor="blue", color="white"), width=340, height=60, visible=False)
        btn_open_sh = ft.ElevatedButton("ВІДКРИТИ ПАРТІЮ", style=ft.ButtonStyle(bgcolor="blue", color="white"), width=340, height=50)

        def trigger_doc_vet(e): snap_doc("vet")
        def trigger_doc_waybill(e): snap_doc("waybill")
        def trigger_doc_chain(e): snap_doc("chain")
        def trigger_doc_thermal(e): snap_doc("thermal")

        btn_doc_vet = ft.ElevatedButton("📄 Вет. Свідоцтво", on_click=trigger_doc_vet, width=160)
        btn_doc_waybill = ft.ElevatedButton("🚚 Відомість", on_click=trigger_doc_waybill, width=160)
        btn_doc_chain = ft.ElevatedButton("🔗 Ланцюг", on_click=trigger_doc_chain, width=160)
        btn_doc_thermal = ft.ElevatedButton("🌡️ Тепловізор", on_click=trigger_doc_thermal, width=160, bgcolor="orange", color="black")

        def change_language(e):
            CURRENT_LANG[0] = "EN" if switch_lang.value else "UA"
            is_en = (CURRENT_LANG[0] == "EN")
            btn_tab_reg.text = "📝 START" if is_en else "📝 СТАРТ"
            btn_tab_work.text = "🔨 WORK" if is_en else "🔨 РОБОТА"
            btn_tab_chat.text = "💬 AI CHAT" if is_en else "💬 ШІ-ЧАТ"
            btn_open_sh.text = "OPEN BATCH & START" if is_en else "ВІДКРИТИ ПАРТІЮ ТА ПОЧАТИ"
            btn_bad.text = "🛑 PATHOLOGY" if is_en else "🛑 ПАТОЛОГІЯ"
            btn_close.text = "🔒 FINISH BATCH" if is_en else "🔒 ФІНАЛЬНИЙ ОГЛЯД ПАРТІЇ"
            btn_doc_vet.text = "📄 Vet Cert" if is_en else "📄 Вет. Свідоцтво"
            btn_doc_waybill.text = "🚚 Waybill" if is_en else "🚚 Відомість"
            btn_doc_chain.text = "🔗 Food Chain" if is_en else "🔗 Ланцюг"
            btn_doc_thermal.text = "🌡️ Thermal" if is_en else "🌡️ Тепловізор"
            lbl_ai_title.value = "🤖 AI Consultant" if is_en else "🤖 ШІ-Консультант"
            chat_input.hint_text = "Question or describe image..." if is_en else "Питання або опис фото..."
            update_ui(); page.update()
            
        switch_lang.on_change = change_language

        def load_active_shift():
            c = sqlite3.connect(DB_NAME)
            r = c.execute("SELECT id, farm, count FROM shifts WHERE status='OPEN' ORDER BY id DESC LIMIT 1").fetchone()
            if r:
                active_shift.update({"id": r[0], "batch": r[1], "total": r[2]})
                ins = c.execute("SELECT COUNT(id) FROM inspections WHERE shift_id=?", (r[0],)).fetchone()
                active_shift["current"] = (ins[0] + 1) if ins[0] else 1
            else: active_shift["id"] = None
            c.close()
        load_active_shift()

        # --- ЛОГІКА ВИДАЛЕННЯ ---
        item_to_delete = [None]
        
        def close_delete(e=None):
            dlg_delete_confirm.open = False
            page.update()

        def execute_delete(e):
            if item_to_delete[0]:
                c = sqlite3.connect(DB_NAME)
                c.execute("DELETE FROM inspections WHERE id=?", (item_to_delete[0],))
                for i, row in enumerate(c.execute("SELECT id FROM inspections WHERE shift_id=? ORDER BY num, id", (active_shift["id"],)).fetchall()):
                    c.execute("UPDATE inspections SET num=? WHERE id=?", (i+1, row[0]))
                c.commit(); c.close(); load_active_shift(); update_ui()
                show_snack("🗑️ Запис видалено.", "red")
            close_delete()

        dlg_delete_confirm = ft.AlertDialog(
            title=ft.Text("Підтвердження"), 
            content=ft.Text("Видалити огляд?"), 
            actions=[
                ft.TextButton("Скасувати", on_click=close_delete), 
                ft.ElevatedButton("ВИДАЛИТИ", on_click=execute_delete, bgcolor="red", color="white")
            ]
        )
        
        def trigger_delete(item_id):
            item_to_delete[0] = item_id
            page.dialog = dlg_delete_confirm
            dlg_delete_confirm.open = True
            page.update()

        def update_ui():
            if active_shift["id"]:
                if active_shift["current"] > active_shift["total"]:
                    btn_norm.visible, btn_bad.visible, btn_close.visible = False, False, True
                    lbl_status.value, lbl_status.color = ("🛑 Inspection Complete!", "red") if CURRENT_LANG[0]=="EN" else ("🛑 Огляд завершено!", "red")
                else:
                    s_text = f"Batch: {active_shift['batch']} | Done: {active_shift['current']-1}/{active_shift['total']}" if CURRENT_LANG[0]=="EN" else f"Партія: {active_shift['batch']} | Огляд: {active_shift['current']} з {active_shift['total']}"
                    lbl_status.value, lbl_status.color = s_text, "green"
                    btn_norm.visible, btn_bad.visible, btn_close.visible = True, True, False
                    btn_norm.text = f"✅ CARCASS #{active_shift['current']} (NORMAL)" if CURRENT_LANG[0]=="EN" else f"✅ ТУША №{active_shift['current']} (НОРМА)"
                
                lv_hist.controls.clear()
                c = sqlite3.connect(DB_NAME)
                for r in c.execute("SELECT id, num, organ, status, diagnosis, photo FROM inspections WHERE shift_id=? ORDER BY num DESC", (active_shift["id"],)).fetchall():
                    icon = ft.icons.CHECK_CIRCLE if "НОРМА" in r[3] or "NORMAL" in r[3] else ft.icons.WARNING
                    icon_color = "green" if "НОРМА" in r[3] or "NORMAL" in r[3] else "red"
                    photo_badge = f" 📸" if r[5] else ""
                    
                    def make_edit_click(item_id):
                        return lambda e: open_pathology(item_id)
                    def make_delete_click(item_id):
                        return lambda e: trigger_delete(item_id)

                    lv_hist.controls.append(ft.Card(content=ft.ListTile(
                        leading=ft.Icon(icon, color=icon_color), 
                        title=ft.Text(f"#{r[1]} | {r[2]}{photo_badge}", weight="bold"), subtitle=ft.Text(r[4] or r[3], size=12),
                        trailing=ft.Row([
                            ft.IconButton(icon=ft.icons.EDIT, icon_color="blue", on_click=make_edit_click(r[0])),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color="red", on_click=make_delete_click(r[0]))
                        ], alignment=ft.MainAxisAlignment.END, width=100)
                    )))
                c.close()
            else:
                lbl_status.value, lbl_status.color = ("No active batch", "red") if CURRENT_LANG[0]=="EN" else ("Немає активної партії", "red")
                btn_norm.visible, btn_bad.visible, btn_close.visible = False, False, False
                lv_hist.controls.clear()
            page.update()

        def create_sh(e):
            c = sqlite3.connect(DB_NAME)
            c.execute("UPDATE shifts SET status='CLOSED'")
            c.execute("INSERT INTO shifts (date, enterprise, farm, type, count, vet, temp, doc_vet, doc_waybill, doc_chain, doc_thermal, animal_ids) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (datetime.now().strftime("%d.%m.%Y %H:%M"), tf_ent.value, tf_farm.value, tf_type.value, int(tf_count.value), tf_vet.value, tf_temp.value, doc_paths["vet"], doc_paths["waybill"], doc_paths["chain"], doc_paths["thermal"], tf_animal_ids.value))
            c.commit(); c.close(); load_active_shift(); update_ui(); change_tab("work")

        btn_open_sh.on_click = create_sh

        def save_norm():
            n = active_shift["current"]
            st = "NORMAL" if CURRENT_LANG[0] == "EN" else "НОРМА"
            diag = "Healthy" if CURRENT_LANG[0] == "EN" else "Здорова"
            c = sqlite3.connect(DB_NAME)
            c.execute("INSERT INTO inspections (shift_id, batch, num, organ, status, time, diagnosis, orders_action) VALUES (?,?,?,?,?,?,?,?)", 
                      (active_shift["id"], active_shift["batch"], n, "Туша", st, datetime.now().strftime("%H:%M"), diag, "Release"))
            c.commit(); c.close(); load_active_shift(); update_ui()

        # --- ЕКСПЕРТИЗА (ПАТОЛОГІЯ) ---
        cur_photo_paths = []
        edit_mode_id = [None]
        row_photos = ft.Row(wrap=True, scroll=ft.ScrollMode.AUTO)
        lbl_photo = ft.Text("0", color="grey")
        
        def on_photo(e): 
            if e.files:
                for f in e.files:
                    new_path = os.path.join(PHOTOS_DIR, f"IMG_{datetime.now().strftime('%H%M%S_%f')}.jpg") 
                    shutil.copy(f.path, new_path)
                    cur_photo_paths.append(new_path)
                    row_photos.controls.append(ft.Image(src=new_path, width=50, height=50, fit="cover"))
                lbl_photo.value = f"✅ Фото ({len(cur_photo_paths)})"
                page.update()
                
        fp_photo.on_result = on_photo

        def trigger_pathology_photo(e):
            fp_photo.pick_files(allow_multiple=True)

        dlg_organ = ft.Dropdown(options=[ft.dropdown.Option(x) for x in ["Внутрішні органи", "Туша", "Голова"]], value="Внутрішні органи", width=200)
        dlg_notes = ft.TextField(label="Опис (Description)", multiline=True, min_lines=2, max_lines=4, width=220)
        dlg_diagnosis = ft.TextField(label="Діагноз (Diagnosis)", color="red")
        dlg_ai = ft.TextField(label="Аналіз (Analysis)", multiline=True) 
        dlg_orders = ft.TextField(label="Дії за Наказом (Actions)", multiline=True, color="blue")

        def ask_ai_click(e):
            if cur_photo_paths:
                dlg_diagnosis.value, dlg_ai.value = "🤖...", "🤖..."
                page.update()
                ai_data = ask_ai_opinion(cur_photo_paths, dlg_notes.value, dlg_organ.value)
                dlg_diagnosis.value, dlg_ai.value, dlg_orders.value = ai_data.get("diagnosis", ""), ai_data.get("analysis", ""), ai_data.get("orders", "")
            page.update()

        def ask_offline_orders_click(e):
            diag_text = dlg_diagnosis.value.strip().lower()
            dlg_orders.value = "Шукаю (Searching)..."
            for key, inst in NAKAZ_28_DB.items():
                if key in diag_text: dlg_orders.value = inst; break
            page.update()

        def close_inspection(e=None):
            dlg_inspection.open = False
            page.update()

        def save_inspection_click(e):
            c = sqlite3.connect(DB_NAME)
            photo_str = "|".join(cur_photo_paths)
            st = "PATHOLOGY" if CURRENT_LANG[0] == "EN" else "ПАТОЛОГІЯ"
            if edit_mode_id[0]:
                c.execute("UPDATE inspections SET organ=?, status=?, notes=?, photo=?, diagnosis=?, ai_result=?, orders_action=? WHERE id=?", 
                          (dlg_organ.value, st, dlg_notes.value, photo_str, dlg_diagnosis.value, dlg_ai.value, dlg_orders.value, edit_mode_id[0]))
            else:
                c.execute("INSERT INTO inspections (shift_id, batch, num, organ, status, time, photo, diagnosis, ai_result, orders_action, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                    (active_shift["id"], active_shift["batch"], active_shift["current"], dlg_organ.value, st, datetime.now().strftime("%H:%M"), photo_str, dlg_diagnosis.value, dlg_ai.value, dlg_orders.value, dlg_notes.value))
            c.commit(); c.close()
            close_inspection()
            load_active_shift(); update_ui()

        dlg_inspection = ft.AlertDialog(
            title=ft.Text("Огляд / Inspection", weight="bold"),
            inset_padding=ft.padding.all(10), 
            content=ft.Container(
                width=360, 
                content=ft.Column([
                    dlg_organ,
                    ft.Row([ft.ElevatedButton("📷 ФОТО", on_click=trigger_pathology_photo), lbl_photo]),
                    row_photos,
                    ft.Row([dlg_notes, ft.IconButton(icon=ft.icons.MIC, icon_size=35, icon_color="blue", tooltip="Мікрофон", on_click=lambda e: dlg_notes.focus())]),
                    ft.Row([ft.ElevatedButton("🤖 ШІ", on_click=ask_ai_click, bgcolor="purple", color="white"), ft.ElevatedButton("⚡ ОФЛАЙН", on_click=ask_offline_orders_click, bgcolor="orange", color="black")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    dlg_diagnosis, dlg_ai, dlg_orders
                ], scroll=ft.ScrollMode.AUTO, spacing=10)
            ),
            actions=[
                ft.TextButton("Скасувати", on_click=close_inspection),
                ft.ElevatedButton("ЗБЕРЕГТИ", on_click=save_inspection_click, bgcolor="blue", color="white")
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        def open_pathology(edit_id=None):
            edit_mode_id[0] = edit_id
            cur_photo_paths.clear(); row_photos.controls.clear()
            if edit_id:
                c = sqlite3.connect(DB_NAME)
                r = c.execute("SELECT organ, status, notes, photo, diagnosis, ai_result, orders_action FROM inspections WHERE id=?", (edit_id,)).fetchone()
                c.close()
                dlg_organ.value, dlg_notes.value, dlg_diagnosis.value, dlg_ai.value, dlg_orders.value = r[0], (r[2] or ""), (r[4] or ""), (r[5] or ""), (r[6] or "")
                if r[3]: 
                    for p in r[3].split("|"):
                        if p and os.path.exists(p):
                            cur_photo_paths.append(p)
                            row_photos.controls.append(ft.Image(src=p, width=50, height=50, fit="cover"))
                lbl_photo.value = f"✅ Фото ({len(cur_photo_paths)})"
            else:
                lbl_photo.value = "0"
                dlg_notes.value = ""; dlg_diagnosis.value = ""; dlg_ai.value = ""; dlg_orders.value = ""
                dlg_organ.value = "Внутрішні органи"
            
            page.dialog = dlg_inspection
            dlg_inspection.open = True
            page.update()
            
        def trigger_open_pathology(e): open_pathology()
        btn_bad.on_click = trigger_open_pathology

        # --- ФІНАЛЬНИЙ ЗВІТ ---
        txt_final_notes = ft.TextField(label="Порушення (Violations)", multiline=True)
        tf_culled = ft.TextField(label="Вибраковка кг (Culled kg)", value="0")
        
        cur_final_photos = []
        row_final_photos = ft.Row(wrap=True, scroll=ft.ScrollMode.AUTO)
        lbl_final_photo = ft.Text("0", color="grey")
        
        def on_final_photo(e): 
            if e.files:
                for f in e.files:
                    new_path = os.path.join(PHOTOS_DIR, f"FINAL_{datetime.now().strftime('%H%M%S_%f')}.jpg") 
                    shutil.copy(f.path, new_path)
                    cur_final_photos.append(new_path)
                    row_final_photos.controls.append(ft.Image(src=new_path, width=50, height=50, fit="cover"))
                lbl_final_photo.value = f"✅ Фото ({len(cur_final_photos)})"
                page.update()
                
        fp_final.on_result = on_final_photo

        def trigger_final_photo(e): fp_final.pick_files(allow_multiple=True)
        
        def close_final(e=None):
            dlg_final.open = False
            page.update()

        def generate_and_close_shift(e):
            c = sqlite3.connect(DB_NAME)
            c.execute("UPDATE shifts SET status='CLOSED', final_notes=?, culled_kg=?, final_photo=? WHERE id=?", (txt_final_notes.value, tf_culled.value, "|".join(cur_final_photos), active_shift["id"]))
            shift_info = c.execute("SELECT type, count, vet, farm, date, final_notes, enterprise, temp, culled_kg, animal_ids, doc_vet, doc_waybill, doc_chain, doc_thermal, final_photo FROM shifts WHERE id=?", (active_shift["id"],)).fetchone()
            rows = c.execute("SELECT num, organ, status, diagnosis, notes, orders_action, photo FROM inspections WHERE shift_id=? ORDER BY num", (active_shift["id"],)).fetchall()
            c.close()
            
            is_en = (CURRENT_LANG[0] == "EN")
            h_title = "Veterinary-Sanitary Conclusion" if is_en else "Державний Ветеринарно-Санітарний Висновок"
            h_batch = "Batch Info:" if is_en else "Інформація про партію:"
            
            h_humane = "Pre-slaughter & Humane Slaughter:" if is_en else "Передзабійне утримання та гуманний забій:"
            h_humane_text = "Animals rested after transportation, fully calmed down, and were provided with unhindered access to drinking water. Kept on a starvation diet for 6 hours. The slaughter was carried out without the use of stress factors, in compliance with the requirements of humane treatment in accordance with the Law of Ukraine 'On the Protection of Animals from Cruelty' and current veterinary and sanitary rules." if is_en else "Тварини відпочили після транспортування, повністю заспокоїлися та були забезпечені безперешкодним доступом до питної води. Витримані на голодній дієті протягом 6 годин. Забій проведено без застосування стресових факторів, з дотриманням вимог гуманного поводження відповідно до Закону України «Про захист тварин від жорстокого поводження» та чинних ветеринарно-санітарних правил."
            
            h_cooling_title = "Movement of products:" if is_en else "Рух продукції:"
            h_cooling_text = "All suitable carcasses and offal are directed to the cooling chamber (temperature regime from 0 °C to +4 °C). Sale is allowed after complete cooling." if is_en else "Усі придатні туші та субпродукти направляються в камеру остигання (температурний режим від 0 °C до +4 °C). Реалізація дозволяється після повного охолодження."
            
            h_table = "Inspection Results:" if is_en else "Результати експертизи:"
            h_cull = f"Culled meat: {shift_info[8]} kg" if is_en else f"Вибракувано: {shift_info[8]} kg"
            
            html = f"<html><head><meta charset='utf-8'></head><body style='font-family: Arial; padding: 20px;'>"
            html += f"<h1 style='text-align: center;'>{h_title}</h1><hr><h3>{h_batch}</h3>"
            html += f"<p><b>Enterprise:</b> {shift_info[6]}<br><b>Date:</b> {shift_info[4]}<br><b>Farm:</b> {shift_info[3]}<br><b>Animals:</b> {shift_info[1]} heads ({shift_info[0]})<br><b>Vet:</b> {shift_info[2]}</p>"
            html += f"<div style='border: 1px solid #28a745; background-color: #f8fff8; padding: 10px; margin-bottom: 10px; border-radius: 5px;'><h4 style='margin: 0 0 5px 0; color: #28a745;'>{h_humane}</h4><p style='margin: 0; font-size: 13px;'>{h_humane_text}</p></div>"
            
            html += f"<h3>{h_table}</h3><table border='1' width='100%' style='border-collapse: collapse;' cellpadding='5'><tr><th>№</th><th>Status</th><th>Diagnosis</th><th>Description</th><th>Photo</th></tr>"
            for r in rows:
                bg = "#ffe6e6" if "ПАТОЛ" in r[2] or "PATH" in r[2] else "#e6ffe6"
                photos_html = ""
                if r[6]:
                    for p in str(r[6]).split("|"):
                        b64 = get_img_base64(p)
                        if b64: photos_html += f"<img src='{b64}' width='100' style='margin:2px;'>"
                html += f"<tr bgcolor='{bg}'><td>{r[0]}</td><td><b>{r[2]}</b></td><td>{r[3]}</td><td>{r[4]}<br><i>{r[5]}</i></td><td>{photos_html}</td></tr>"
            html += f"</table>"
            
            # --- НОВИЙ БЛОК: ТРИХІНЕЛОСКОПІЯ ---
            h_trich = "Trichinelloscopy performed: Result NEGATIVE." if is_en else "В результаті експертизи: трихінелоскопія проведена, результат НЕГАТИВНО."
            html += f"<p style='font-size: 16px; font-weight: bold; color: #28a745; border-left: 4px solid #28a745; padding-left: 10px; margin-top: 15px;'>{h_trich}</p>"
            
            html += f"<h3>{h_cooling_title}</h3><p style='border-left: 4px solid #007bff; padding-left: 10px; font-size: 14px;'>{h_cooling_text}</p>"
            html += f"<p style='font-size: 14px; border-left: 4px solid red; padding-left: 10px;'><b>Додаткові порушення:</b> {shift_info[5] or '-'}</p>"
            html += f"<h3>{h_cull}</h3>"
            
            if shift_info[14]:
                html += "<p>"
                for p in str(shift_info[14]).split("|"):
                    b64 = get_img_base64(p)
                    if b64: html += f"<img src='{b64}' width='250' style='margin: 5px; border: 1px solid #ccc;'>"
                html += "</p>"
            
            # --- НОВИЙ БЛОК: ДОКУМЕНТИ (КОМПАКТНО НА ОДИН ЛИСТ) ---
            html += "<div style='page-break-before: always;'><h2 style='text-align: center; background: #eee; padding: 10px;'>ДОДАТКИ (Супровідні документи)</h2>"
            html += "<table width='100%' style='border-collapse: collapse; text-align: center; border: none;'>"
            
            docs_to_print = []
            doc_names = ["Вет. Свідоцтво", "Відомість", "Харчовий Ланцюг", "Термометрія"]
            for name, idx in zip(doc_names, [10, 11, 12, 13]):
                if len(shift_info) > idx and shift_info[idx]:
                    b64 = get_img_base64(shift_info[idx])
                    if b64: docs_to_print.append((name, b64))
                    
            # Формуємо таблицю 2х2 для документів
            for i in range(0, len(docs_to_print), 2):
                html += "<tr>"
                for j in range(2):
                    if i + j < len(docs_to_print):
                        name, b64 = docs_to_print[i+j]
                        html += f"<td style='width: 50%; padding: 5px; vertical-align: top;'>"
                        html += f"<h4 style='margin: 5px 0; color: #333;'>{name}</h4>"
                        html += f"<img src='{b64}' style='width: 95%; max-height: 480px; object-fit: contain; border: 1px solid #ccc; padding: 2px;'>"
                        html += "</td>"
                    else:
                        html += "<td style='width: 50%;'></td>"
                html += "</tr>"
            
            html += "</table></div></body></html>"
            
            rep_path = os.path.join(DOWNLOADS_DIR, f"Report_{active_shift['batch']}_{datetime.now().strftime('%H%M')}.html")
            with open(rep_path, "w", encoding="utf-8") as f: f.write(html)
            
            close_final()
            load_active_shift(); update_ui()
            show_snack("✅ Saved / Збережено!", "green")

        dlg_final = ft.AlertDialog(
            title=ft.Text("Фінал / Final"), 
            content=ft.Column([
                txt_final_notes, tf_culled,
                ft.Text("Фото порушень (Violations photos):", color="blue"),
                ft.Row([ft.ElevatedButton("📷 ФОТО", on_click=trigger_final_photo), lbl_final_photo]),
                row_final_photos
            ], height=300, scroll=ft.ScrollMode.AUTO), 
            actions=[ft.ElevatedButton("ЗБЕРЕГТИ ЗВІТ", on_click=generate_and_close_shift, bgcolor="blue", color="white")]
        )
        
        def open_final_dialog():
            txt_final_notes.value = ""; tf_culled.value = "0"
            cur_final_photos.clear(); row_final_photos.controls.clear(); lbl_final_photo.value = "0"
            page.dialog = dlg_final
            dlg_final.open = True
            page.update()
            
        def trigger_open_final(e): open_final_dialog()
        btn_close.on_click = trigger_open_final

        # ==========================================
        # 🧠 ШІ-КОНСУЛЬТАНТ + ЗБЕРЕЖЕННЯ/ОЧИЩЕННЯ ЧАТУ
        # ==========================================
        chat_list = ft.ListView(height=400, spacing=10, auto_scroll=True) 
        chat_input = ft.TextField(hint_text="Питання або опис фото...", multiline=True, min_lines=1, max_lines=3, width=220)
        
        cur_chat_image_path = [None]
        img_chat_preview = ft.Image(src="", width=50, height=50, visible=False, fit="cover")
        
        # Пам'ять чату
        chat_history_data = []
        
        def on_chat_image_picked(e):
            if e.files:
                original_path = e.files[0].path
                new_path = os.path.join(safe_dir, f"TEMP_CHAT_{datetime.now().strftime('%H%M%S')}.jpg")
                shutil.copy(original_path, new_path)
                cur_chat_image_path[0] = new_path
                img_chat_preview.src = new_path
                img_chat_preview.visible = True
                btn_clear_chat_img.visible = True
                page.update()
                
        fp_chat_image.on_result = on_chat_image_picked
        
        def clear_chat_image(e):
            cur_chat_image_path[0] = None
            img_chat_preview.visible = False
            btn_clear_chat_img.visible = False
            page.update()
            
        def trigger_chat_picker(e):
            fp_chat_image.pick_files()

        btn_chat_add_photo = ft.IconButton(icon=ft.icons.ADD_A_PHOTO, icon_color="purple", icon_size=30, on_click=trigger_chat_picker)
        btn_clear_chat_img = ft.IconButton(icon=ft.icons.CANCEL, icon_color="red", visible=False, on_click=clear_chat_image)

        def send_chat(e):
            user_msg = chat_input.value
            chat_img = cur_chat_image_path[0]
            
            if not user_msg and not chat_img: return
            
            # Зберігаємо повідомлення лікаря в пам'ять
            chat_history_data.append({
                "role": "Лікар",
                "text": user_msg,
                "image": chat_img,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            
            chat_input.value = ""
            user_msg_ctrl = ft.Text(user_msg, color="white")
            user_content_items = [user_msg_ctrl]
            
            if chat_img:
                user_content_items.insert(0, ft.Image(src=chat_img, width=150, border_radius=5))
                
            chat_list.controls.append(ft.Container(
                content=ft.Column(user_content_items, spacing=5), 
                bgcolor="blue", 
                padding=10, 
                border_radius=10, 
                alignment=ft.alignment.center_right
            ))
            
            thinking_indicator = ft.Text("🤖 Думаю...", color="grey", italic=True)
            chat_list.controls.append(thinking_indicator)
            page.update()
            
            ai_reply = ask_ai_consultant_multimodal(user_msg, chat_img)
            
            # Зберігаємо відповідь ШІ в пам'ять
            chat_history_data.append({
                "role": "ШІ-Консультант",
                "text": ai_reply,
                "image": None,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            
            chat_list.controls.remove(thinking_indicator)
            chat_list.controls.append(ft.Container(
                content=ft.Text(ai_reply), 
                bgcolor="#e0e0e0", 
                padding=10, 
                border_radius=10, 
                alignment=ft.alignment.center_left
            ))
            
            clear_chat_image(None)
            page.update()

        # ФУНКЦІЯ ОЧИЩЕННЯ ЧАТУ
        def clear_chat_history(e):
            chat_history_data.clear()
            chat_list.controls.clear()
            page.update()
            show_snack("🧹 Чат повністю очищено", "blue")

        # ФУНКЦІЯ ЗБЕРЕЖЕННЯ ЧАТУ
        def export_chat_to_html(e):
            if not chat_history_data:
                show_snack("Чат порожній, немає чого зберігати!", "red")
                return

            html = "<html><head><meta charset='utf-8'><style>"
            html += "body {font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: auto;}"
            html += ".msg {padding: 10px; margin-bottom: 10px; border-radius: 8px;}"
            html += ".user {background-color: #e3f2fd; border-left: 5px solid #2196f3;}"
            html += ".ai {background-color: #f5f5f5; border-left: 5px solid #9c27b0;}"
            html += "img {max-width: 300px; border-radius: 5px; margin-bottom: 10px;}"
            html += "</style></head><body>"
            html += f"<h2 style='text-align:center;'>Консультація зі Штучним Інтелектом (VetAI)</h2>"
            html += f"<p style='text-align:center; color:grey;'>Дата експорту: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p><hr>"

            for msg in chat_history_data:
                cls = "user" if msg["role"] == "Лікар" else "ai"
                html += f"<div class='msg {cls}'>"
                html += f"<b>{msg['role']}</b> <span style='font-size:12px;color:grey;'>({msg['time']})</span><br><br>"
                if msg["image"]:
                    b64 = get_img_base64(msg["image"])
                    if b64: html += f"<img src='{b64}'><br>"
                text_html = msg["text"].replace('\n', '<br>')
                html += f"<div>{text_html}</div>"
                html += "</div>"

            html += "</body></html>"

            export_path = os.path.join(DOWNLOADS_DIR, f"VetAI_Chat_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(html)

            show_snack(f"✅ Чат збережено: {os.path.basename(export_path)}", "green")

        lbl_ai_title = ft.Text("🤖 ШІ-Консультант", weight="bold", color="purple")
        btn_clear_chat = ft.IconButton(icon=ft.icons.DELETE_SWEEP, icon_color="red", tooltip="Очистити чат", on_click=clear_chat_history)
        btn_export_chat = ft.IconButton(icon=ft.icons.SAVE_ALT, icon_color="blue", tooltip="Зберегти діалог у файл", on_click=export_chat_to_html)
        
        # Групуємо кнопки збереження і очищення разом
        row_chat_header = ft.Row([lbl_ai_title, ft.Row([btn_clear_chat, btn_export_chat])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # ==========================================
        # ВКЛАДКИ І ФІНАЛЬНЕ ДОДАВАННЯ НА ЕКРАН
        # ==========================================
        content_reg = ft.Column([
            switch_lang, tf_ent, tf_farm, tf_type, tf_count, tf_animal_ids, tf_vet, tf_temp, ft.Divider(),
            ft.Text("Документи:"), 
            ft.Row([btn_doc_vet, lbl_doc_vet]), ft.Row([btn_doc_waybill, lbl_doc_waybill]), 
            ft.Row([btn_doc_chain, lbl_doc_chain]), ft.Row([btn_doc_thermal, lbl_doc_thermal]),
            ft.Container(height=10), btn_open_sh
        ], visible=False)
        
        content_work = ft.Column([lbl_status, ft.Divider(), btn_norm, btn_bad, btn_close, ft.Divider(), lv_hist], visible=True)
        
        content_chat = ft.Column([
            row_chat_header,
            chat_list, 
            ft.Row([img_chat_preview, btn_clear_chat_img], alignment=ft.MainAxisAlignment.START),
            ft.Row([
                btn_chat_add_photo,
                chat_input, 
                ft.IconButton(icon=ft.icons.MIC, icon_size=30, icon_color="blue", tooltip="Голос", on_click=lambda e: chat_input.focus()), 
                ft.IconButton(icon=ft.icons.SEND, icon_color="green", icon_size=30, on_click=send_chat)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], visible=False)
        
        def change_tab(name): 
            content_reg.visible, content_work.visible, content_chat.visible = (name == "reg"), (name == "work"), (name == "chat")
            page.update()
            
        def trig_tab_reg(e): change_tab("reg")
        def trig_tab_work(e): change_tab("work")
        def trig_tab_chat(e): change_tab("chat")

        btn_tab_reg.on_click = trig_tab_reg
        btn_tab_work.on_click = trig_tab_work
        btn_tab_chat.on_click = trig_tab_chat

        page.add(
            ft.Row([btn_tab_reg, btn_tab_work, btn_tab_chat, btn_settings], alignment=ft.MainAxisAlignment.CENTER, wrap=True), 
            ft.Divider(), 
            content_reg, 
            content_work, 
            content_chat
        )
        
        update_ui()

    ft.app(target=main)

except Exception as e:
    err = traceback.format_exc()
    import flet as ft
    def error_main(page: ft.Page):
        page.scroll = ft.ScrollMode.ADAPTIVE
        page.add(
            ft.Text("❌ КРИТИЧНА ПОМИЛКА ПРИ СТАРТІ", color="red", size=22, weight="bold"),
            ft.Text("Зробіть скріншот цього тексту і надішліть його мені:", color="blue", size=16),
            ft.Text(err, selectable=True, size=12, color="black")
        )
    ft.app(target=error_main)
