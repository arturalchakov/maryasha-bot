import os
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# ── RPG LEVELS ───────────────────────────────────────────────────────────────
LEVELS = [
    (0,    "🥚 Яйцо",        "Только начинаешь — и это уже круто!"),
    (100,  "🐣 Новичок",     "Первые шаги сделаны, продолжай!"),
    (300,  "⚡ Практик",     "Уже что-то умеешь, огонь!"),
    (600,  "🔥 Специалист",  "Растёшь на глазах!"),
    (1000, "💎 Профи",       "Красавица! Топ-уровень!"),
    (1500, "🌟 Эксперт",     "Люди учатся у тебя!"),
    (2000, "👑 ЛЕГЕНДА",     "Ты легенда! Гордимся тобой!"),
]

SKILLS = {
    "content":  "✍️ Контент",
    "promo":    "🔥 Прогревы",
    "visual":   "🎨 Визуал",
    "stories":  "📖 Сторителлинг",
    "target":   "🎯 ЦА",
    "strategy": "📊 Стратегия",
}

BADGES = {
    "first_quiz": "🏅 Первый квиз",
    "quest_done": "⚔️ Квестер",
    "xp_300":     "🚀 300 XP",
    "xp_1000":    "💎 1000 XP",
}

# ── QUIZ DATA ─────────────────────────────────────────────────────────────────
QUIZZES = {
    "smm_q": {
        "title": "📱 SMM — базовые знания",
        "skill": "content", "sp": 10,
        "qs": [
            {"q": "Что такое SMM?", "opts": ["Продажи в магазине 🏪","Маркетинг в соцсетях 📱","Email-рассылка 📧"], "a": 1, "exp": "SMM = Social Media Marketing — продвижение в соцсетях! 🎯"},
            {"q": "Лучший формат для охватов?", "opts": ["Статичные посты 🖼️","Reels/Shorts 🎬","Длинные видео 🎥"], "a": 1, "exp": "Reels и Shorts рвут охваты — алгоритмы их обожают! 🚀"},
            {"q": "Как часто постить сторис?", "opts": ["Раз в неделю 😴","Каждый день ✅","Раз в месяц 🗓️"], "a": 1, "exp": "Ежедневные сторис = живая связь с аудиторией! ❤️"},
        ],
    },
    "content_q": {
        "title": "📊 Контент-стратегия",
        "skill": "content", "sp": 10,
        "qs": [
            {"q": "Что такое TOV?", "opts": ["Тип визуала 🎨","Голос и стиль бренда 🗣️","Вид рекламы 📢"], "a": 1, "exp": "TOV (Tone of Voice) — как твой бренд разговаривает! 💬"},
            {"q": "Лучший контент-микс?", "opts": ["100% продажи 💰","50% польза / 50% продажи ⚖️","70% польза / 20% жизнь / 10% продажи 🎯"], "a": 2, "exp": "70/20/10 — золотой стандарт! Сначала давай ценность 💛"},
            {"q": "Контент-воронка — это?", "opts": ["Слив контента 🚽","Путь от знакомства до покупки 🎯","Список тем для постов 📝"], "a": 1, "exp": "Воронка ведёт человека от 'кто ты?' до 'хочу купить!' 🔥"},
        ],
    },
    "visual_q": {
        "title": "🎨 Визуал и дизайн",
        "skill": "visual", "sp": 10,
        "qs": [
            {"q": "Сколько шрифтов в посте?", "opts": ["5+ разных 🤪","1-2 максимум ✅","Чем больше, тем лучше 🎭"], "a": 1, "exp": "Минимализм рулит! 1-2 шрифта — чисто и стильно 💎"},
            {"q": "Лучший размер поста Instagram?", "opts": ["1080x1080px ✅","500x300px 😬","2000x3000px 📏"], "a": 0, "exp": "1080x1080 — стандарт квадрата! 🖼️"},
            {"q": "Что такое визуальный стиль?", "opts": ["Красивая аватарка 🖼️","Единые цвета, шрифты и атмосфера бренда 🎨","Много разных фильтров 🌈"], "a": 1, "exp": "Визстиль = единство! Люди узнают тебя с первого взгляда 👁️"},
        ],
    },
    "promo_q": {
        "title": "🔥 Прогревы (по Марии Афониной)",
        "skill": "promo", "sp": 15,
        "qs": [
            {"q": "Прогрев — это?", "opts": ["Реклама в лоб 📢","Контент, создающий доверие перед продажей ❤️","Скидки и акции 🎁"], "a": 1, "exp": "Прогрев = разогрев через ценность и историю 🔥"},
            {"q": "Лучший тип прогревающего контента?", "opts": ["Прайс-листы 💰","Разборы ошибок и кейсы 🎯","Репосты чужого контента 🔄"], "a": 1, "exp": "Кейсы и разборы = доверие + экспертность! 💪"},
            {"q": "Сколько касаний нужно для продажи?", "opts": ["1-2 поста 😅","7-12 касаний минимум 🎯","100+ постов 😵"], "a": 1, "exp": "7-12 касаний — столько нужно человеку чтобы решиться! 🔥"},
        ],
    },
}

# ── WARMUP SCHOOL ─────────────────────────────────────────────────────────────
WARMUP_LESSONS = [
    {"title": "🔥 Урок 1: Что такое прогрев", "text": "Прогрев — это не реклама в лоб, а постепенное создание доверия.\n\n📌 Три кита прогрева:\n• Личность — кто ты как человек\n• Экспертность — почему тебе можно доверять\n• Желание — почему людям нужно твоё решение\n\n💡 Главное правило Марии Афониной:\nСначала дай ценность — потом продавай!", "xp": 20, "skill": "promo"},
    {"title": "👤 Урок 2: Личность в блоге", "text": "Люди покупают у людей, а не у корпораций.\n\n📌 Что показывать в блоге:\n• Свой путь и ошибки (честность = доверие)\n• Закулисье работы\n• Личные ценности и принципы\n• Юмор и живые моменты\n\n💡 Задание: напиши пост-знакомство!", "xp": 20, "skill": "stories"},
    {"title": "📖 Урок 3: Сторителлинг", "text": "История продаёт лучше любой рекламы.\n\n📌 Структура сильной истории:\n1. Боль/проблема (с чего всё началось)\n2. Путь (что ты делал)\n3. Результат (что изменилось)\n4. Вывод (урок для читателя)\n\n💡 Формула Афониной: 'Было — стало — как' = идеальная история!", "xp": 25, "skill": "stories"},
    {"title": "💊 Урок 4: Прогрев через боли", "text": "Говори о проблемах клиента лучше, чем он сам.\n\n📌 Как найти боли ЦА:\n• Читай комментарии конкурентов\n• Спрашивай в сторис\n• Изучай форумы и Telegram-каналы\n\n💡 Пиши не о себе — пиши О НИХ!", "xp": 25, "skill": "target"},
    {"title": "🧠 Урок 5: Интуитивный маркетинг", "text": "Маркетинг — это наука о людях, а не о постах.\n\n📌 Принципы (Афонина):\n• Доверяй своей аудитории\n• Не продавай — помогай выбрать\n• Будь последовательна — хаос отпугивает\n• Экспериментируй и анализируй результат\n\n💡 Ты — архитектор доверия! 🏗️", "xp": 30, "skill": "strategy"},
]

# ── SMM QUEST ─────────────────────────────────────────────────────────────────
SMM_QUEST = [
    {"q": "Марьяша начала вести Instagram. С чего начать?", "opts": ["Сразу делать рекламу 📢","Оформить шапку профиля и придумать стиль 🎨","Купить подписчиков 💸"], "a": 1, "xp": 20, "exp": "Профиль — это твоя витрина! Сначала упаковка 📦"},
    {"q": "Ты написала пост, лайков мало. Что делать?", "opts": ["Удалить и сдаться 😢","Проанализировать — заголовок, время, хэштеги 🔍","Купить лайки 👍"], "a": 1, "xp": 20, "exp": "Анализ — ключ к росту! Каждый пост — это тест 🧪"},
    {"q": "Клиент хочет 1000 подписчиков за неделю. Ты?", "opts": ["Соглашусь и накручу 🤡","Объясню что нужно время и стратегия 💪","Откажусь от клиента 🏃"], "a": 1, "xp": 30, "exp": "Честность = доверие! Настоящий SMM — это стратегия ✨"},
    {"q": "Лучший способ расти в Instagram сейчас?", "opts": ["Покупать рекламу 💰","Reels + коллаборации + регулярный постинг 🎬","Только хэштеги 📌"], "a": 1, "xp": 25, "exp": "Reels дают органику, коллабы — аудиторию, регулярность — доверие! 🔥"},
    {"q": "Контент-план нужен?", "opts": ["Нет, буду по вдохновению 🦋","Да, без плана хаос 📅","Только для больших блогов 🤷"], "a": 1, "xp": 20, "exp": "Контент-план = твой компас! 🧭"},
    {"q": "Марьяша стала SMM-специалистом! Первый шаг?", "opts": ["Взять 10 клиентов сразу 😱","Найти первого клиента и сделать круто 💎","Ждать пока найдут сами 😴"], "a": 1, "xp": 50, "exp": "Один довольный клиент = 10 рекомендаций! 🌟"},
]

# ── USER STATE ────────────────────────────────────────────────────────────────
user_data: dict = {}

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {"xp": 0, "skills": {k: 0 for k in SKILLS}, "badges": [], "quest_step": 0, "quiz_state": None, "warmup_step": 0, "chat_history": []}
    return user_data[uid]

def get_level(xp):
    cur = LEVELS[0]
    for lvl in LEVELS:
        if xp >= lvl[0]: cur = lvl
    return cur

def add_xp(uid, amount, skill=None):
    u = get_user(uid)
    old = get_level(u["xp"])[1]
    u["xp"] += amount
    if skill and skill in u["skills"]: u["skills"][skill] = min(5, u["skills"][skill] + 1)
    new = get_level(u["xp"])[1]
    if u["xp"] >= 300 and "xp_300" not in u["badges"]: u["badges"].append("xp_300")
    if u["xp"] >= 1000 and "xp_1000" not in u["badges"]: u["badges"].append("xp_1000")
    return f"⬆️ НОВЫЙ УРОВЕНЬ: {new}!" if old != new else ""

def xp_bar(xp):
    lvls = [l[0] for l in LEVELS]
    ci = 0
    for i, t in enumerate(lvls):
        if xp >= t: ci = i
    if ci < len(LEVELS) - 1:
        p = int((xp - lvls[ci]) / (lvls[ci+1] - lvls[ci]) * 10)
        return "🟣" * p + "⬜" * (10-p) + f" {xp}/{lvls[ci+1]} XP"
    return "🟣" * 10 + " МАКСИМУМ!"

def profile_text(uid):
    u = get_user(uid)
    lvl = get_level(u["xp"])
    lines = [f"👩‍💻 *Профиль Марьяши*", f"", f"Ранг: {lvl[1]}", f"💬 {lvl[2]}", f"", f"⚡ XP: {u['xp']}", xp_bar(u["xp"]), f"", f"🎯 Скиллы:"]
    for k, name in SKILLS.items():
        lines.append(f"  {name}: " + "⭐" * u["skills"][k] + "☆" * (5 - u["skills"][k]))
    if u["badges"]:
        lines.append("")
        lines.append("🏆 Бейджи: " + " ".join(BADGES[b] for b in u["badges"] if b in BADGES))
    return "\n".join(lines)

# ── AI AGENT (Gemini) ─────────────────────────────────────────────────────────
AI_SYSTEM = """Ты — Марьяша-бот, крутой SMM-наставник для 16-летней девочки Марьяши.

Говори легко и живо, как подруга — не как учебник. Используй эмодзи уместно 🔥
Отвечай кратко (3-5 предложений). Знаешь SMM: контент, прогревы, Reels, визуал, ЦА.
Вдохновляй и поддерживай! Основа знаний — курс Марии Афониной:
- Прогрев = доверие через ценность и личность
- Контент-микс: 70% польза / 20% жизнь / 10% продажи
- Сторителлинг: было — стало — как
- Reels — главный инструмент охватов
Если вопрос не про SMM — мягко верни к теме."""

async def ai_chat(uid, message):
    if not DEEPSEEK_API_KEY:
        return "🤖 AI-агент пока спит... Нужно добавить DEEPSEEK_API_KEY в секреты GitHub!"
    try:
        import httpx
        u = get_user(uid)
        history = u.get("chat_history", [])

        # Build messages for DeepSeek API (OpenAI-compatible format)
        messages = [{"role": "system", "content": AI_SYSTEM}]
        for msg in history[-10:]:
            role = "assistant" if msg["role"] == "model" else msg["role"]
            messages.append({"role": role, "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "max_tokens": 512,
                    "temperature": 0.8
                }
            )
        data = resp.json()

        if "error" in data:
            return f"🤖 Ошибка DeepSeek: {data['error'].get('message', 'unknown')}. Попробуй ещё раз!"

        choices = data.get("choices", [])
        if not choices:
            return "🤖 Не смогла ответить. Попробуй переформулировать вопрос!"

        reply = choices[0]["message"]["content"].strip()

        history.append({"role": "user", "content": message})
        history.append({"role": "model", "content": reply})
        u["chat_history"] = history[-20:]
        return reply
    except httpx.TimeoutException:
        return "🤖 DeepSeek не ответил вовремя. Попробуй ещё раз!"
    except Exception as e:
        return f"🤖 Упс, что-то пошло не так: {str(e)[:150]}. Попробуй ещё раз!"
# ── KEYBOARDS ─────────────────────────────────────────────────────────────────
def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👩‍💻 Мой профиль и скиллы", callback_data="profile")],
        [InlineKeyboardButton("🔥 Школа Прогревов (квест)", callback_data="warmup_menu")],
        [InlineKeyboardButton("📝 Квизы — прокачай знания", callback_data="quiz_menu")],
        [InlineKeyboardButton("⚔️ SMM-Квест", callback_data="quest_start")],
        [InlineKeyboardButton("💬 Спросить AI-наставника", callback_data="ai_chat_info")],
    ])

def warmup_kb(step):
    btns = []
    for i, l in enumerate(WARMUP_LESSONS):
        mark = "✅ " if i < step else ""
        btns.append([InlineKeyboardButton(f"{mark}{l['title']}", callback_data=f"warmup_{i}")])
    btns.append([InlineKeyboardButton("🏠 Назад", callback_data="start")])
    return InlineKeyboardMarkup(btns)

def quiz_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 SMM — базовые знания", callback_data="quiz_smm_q")],
        [InlineKeyboardButton("📊 Контент-стратегия", callback_data="quiz_content_q")],
        [InlineKeyboardButton("🎨 Визуал и дизайн", callback_data="quiz_visual_q")],
        [InlineKeyboardButton("🔥 Прогревы по Марии", callback_data="quiz_promo_q")],
        [InlineKeyboardButton("🏠 Назад", callback_data="start")],
    ])

# ── HANDLERS ──────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    u = get_user(uid)
    lvl = get_level(u["xp"])
    text = (f"👋 Привет, Марьяша! Я твой SMM-наставник 💙\n\n"
            f"Твой ранг: {lvl[1]} | ХР: {u['xp']}\n\n"
            f"🎮 Прокачивай скиллы, зарабатывай ХР и становись\n"
            f"👑 Легендой SMM!\n\n"
            f"💬 Просто напиши мне любой вопрос про SMM —\n"
            f"отвечу как живой AI-наставник! 🤖\n\nВыбери с чего начнём:")
    await update.message.reply_text(text, reply_markup=main_kb(), parse_mode="Markdown")

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msg = update.message.text.strip()
    if msg.startswith("/"): return
    await update.message.chat.send_action("typing")
    reply = await ai_chat(uid, msg)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("📋 Главное меню", callback_data="start")]])
    await update.message.reply_text(reply, reply_markup=kb)

async def cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = get_user(uid)
    data = q.data

    if data == "start":
        lvl = get_level(u["xp"])
        text = (f"👋 Ранг: {lvl[1]} | ХР: {u['xp']}\n\n"
                f"💬 Пиши любой вопрос про SMM — отвечу как AI-наставник! 🤖\n\nВыбери раздел:")
        await q.edit_message_text(text, reply_markup=main_kb(), parse_mode="Markdown")

    elif data == "profile":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Назад", callback_data="start")]])
        await q.edit_message_text(profile_text(uid), reply_markup=kb, parse_mode="Markdown")

    elif data == "ai_chat_info":
        text = ("💬 *AI-наставник активирован!*\n\n"
                "Просто напиши мне любой вопрос прямо в чат — и я отвечу!\n\n"
                "Например:\n• Как сделать крутой Reels?\n• Что такое прогрев?\n"
                "• Как найти ЦА?\n• Помоги придумать контент-план\n\n"
                "🤖 Я всегда здесь и отвечаю быстро!")
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Назад", callback_data="start")]])
        await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    elif data == "warmup_menu":
        await q.edit_message_text("🔥 *Школа Прогревов* (по Марии Афониной)\n\nВыбери урок:",
                                   reply_markup=warmup_kb(u["warmup_step"]), parse_mode="Markdown")

    elif data.startswith("warmup_"):
        idx = int(data.split("_")[1])
        lesson = WARMUP_LESSONS[idx]
        lvl_up = add_xp(uid, lesson["xp"], lesson["skill"])
        if "first_quiz" not in u["badges"]: u["badges"].append("first_quiz")
        if idx >= u["warmup_step"]: u["warmup_step"] = idx + 1
        btns = []
        if idx + 1 < len(WARMUP_LESSONS):
            btns.append([InlineKeyboardButton("➡️ Следующий урок", callback_data=f"warmup_{idx+1}")])
        btns.append([InlineKeyboardButton("📚 Все уроки", callback_data="warmup_menu")])
        btns.append([InlineKeyboardButton("🏠 Главная", callback_data="start")])
        text = f"{lesson['title']}\n\n{lesson['text']}\n\n✨ +{lesson['xp']} XP получено!" + (f"\n\n{lvl_up}" if lvl_up else "")
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(btns))

    elif data == "quiz_menu":
        await q.edit_message_text("📝 *Квизы*\n\nКаждый правильный ответ = ХР + прокачка скилла!\n\nВыбери тему:",
                                   reply_markup=quiz_menu_kb(), parse_mode="Markdown")

    elif data.startswith("quiz_") and not data.startswith("quiz_ans_"):
        qid = data[5:]
        if qid not in QUIZZES: return
        quiz = QUIZZES[qid]
        if "first_quiz" not in u["badges"]: u["badges"].append("first_quiz")
        u["quiz_state"] = {"id": qid, "step": 0, "correct": 0}
        q0 = quiz["qs"][0]
        btns = [[InlineKeyboardButton(o, callback_data=f"quiz_ans_{qid}_0_{i}")] for i, o in enumerate(q0["opts"])]
        await q.edit_message_text(f"📝 {quiz['title']}\nВопрос 1/{len(quiz['qs'])}\n\n❓ {q0['q']}",
                                   reply_markup=InlineKeyboardMarkup(btns))

    elif data.startswith("quiz_ans_"):
        parts = data.split("_")
        chosen = int(parts[-1]); step = int(parts[-2]); qid = "_".join(parts[2:-2])
        if qid not in QUIZZES: return
        quiz = QUIZZES[qid]
        qs = quiz["qs"]
        correct = qs[step]["a"] == chosen
        if u.get("quiz_state") and u["quiz_state"].get("id") == qid and correct:
            u["quiz_state"]["correct"] = u["quiz_state"].get("correct", 0) + 1
        xp_gain = quiz["sp"] if correct else 0
        lvl_up = add_xp(uid, xp_gain, quiz["skill"]) if correct else ""
        result = f"✅ Верно! +{xp_gain} XP\n\n💡 {qs[step]['exp']}" if correct else f"❌ Не совсем...\n\n💡 {qs[step]['exp']}"
        if step + 1 < len(qs):
            nq = qs[step + 1]
            btns = [[InlineKeyboardButton(o, callback_data=f"quiz_ans_{qid}_{step+1}_{i}")] for i, o in enumerate(nq["opts"])]
            btns.append([InlineKeyboardButton("🏠 Выйти", callback_data="quiz_menu")])
            await q.edit_message_text(f"{result}\n\n{'─'*20}\n\n📝 Вопрос {step+2}/{len(qs)}\n\n❓ {nq['q']}",
                                       reply_markup=InlineKeyboardMarkup(btns))
        else:
            cc = u.get("quiz_state", {}).get("correct", 0) + (1 if correct else 0)
            if "quest_done" not in u["badges"] and cc == len(qs): u["badges"].append("quest_done")
            btns = [[InlineKeyboardButton("📝 Ещё квиз", callback_data="quiz_menu")],
                    [InlineKeyboardButton("👩‍💻 Мой профиль", callback_data="profile")],
                    [InlineKeyboardButton("🏠 Главная", callback_data="start")]]
            await q.edit_message_text(f"{result}\n\n{'═'*20}\n\n🎉 Квиз завершён! {cc}/{len(qs)} верных\n{lvl_up}",
                                       reply_markup=InlineKeyboardMarkup(btns))

    elif data == "quest_start":
        step = u.get("quest_step", 0)
        if step >= len(SMM_QUEST):
            await q.edit_message_text("🏆 Ты прошла весь SMM-Квест! Ты настоящий специалист! ⚔️",
                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главная", callback_data="start")]]))
            return
        item = SMM_QUEST[step]
        btns = [[InlineKeyboardButton(o, callback_data=f"quest_ans_{step}_{i}")] for i, o in enumerate(item["opts"])]
        btns.append([InlineKeyboardButton("🏠 Выйти", callback_data="start")])
        await q.edit_message_text(f"⚔️ *SMM-Квест* | Шаг {step+1}/{len(SMM_QUEST)}\n\n{item['q']}",
                                   reply_markup=InlineKeyboardMarkup(btns), parse_mode="Markdown")

    elif data.startswith("quest_ans_"):
        parts = data.split("_")
        step, chosen = int(parts[2]), int(parts[3])
        item = SMM_QUEST[step]
        correct = item["a"] == chosen
        lvl_up = add_xp(uid, item["xp"] if correct else 5, "strategy")
        if correct: u["quest_step"] = max(u.get("quest_step", 0), step + 1)
        result = f"✅ Верно! +{item['xp']} XP\n\n💡 {item['exp']}" if correct else f"❌ Не то...\n\n💡 {item['exp']}"
        btns = [[InlineKeyboardButton("➡️ Следующий шаг", callback_data="quest_start")],
                [InlineKeyboardButton("🏠 Главная", callback_data="start")]]
        await q.edit_message_text(f"{result}" + (f"\n\n{lvl_up}" if lvl_up else ""),
                                   reply_markup=InlineKeyboardMarkup(btns))

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("🚀 Марьяша-бот запущен с Gemini AI-агентом!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
