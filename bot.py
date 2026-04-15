import os
import json
import datetime
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

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
            {"q": "Лучший размер поста Instagram?", "opts": ["1080x1080px ✅","500x300px 😬","2000x3000px 📏"], "a": 0, "exp": "1080x1080 — стандарт квадрата! Также 1080x1350 для вертикали 🖼️"},
            {"q": "Что такое визуальный стиль?", "opts": ["Красивая аватарка 🖼️","Единые цвета, шрифты и атмосфера бренда 🎨","Много разных фильтров 🌈"], "a": 1, "exp": "Визстиль = единство! Люди узнают тебя с первого взгляда 👁️"},
        ],
    },
    "promo_q": {
        "title": "🔥 Прогревы (по Марии Афониной)",
        "skill": "promo", "sp": 15,
        "qs": [
            {"q": "Прогрев — это?", "opts": ["Реклама в лоб 📢","Контент, создающий доверие перед продажей ❤️","Скидки и акции 🎁"], "a": 1, "exp": "Прогрев = разогрев через ценность и историю 🔥"},
            {"q": "Лучший тип прогревающего контента?", "opts": ["Прайс-листы 💰","Разборы ошибок и кейсы 🎯","Репосты чужого контента 🔄"], "a": 1, "exp": "Кейсы и разборы = доверие + экспертность! Люди видят результат 💪"},
            {"q": "Сколько касаний нужно для продажи?", "opts": ["1-2 поста 😅","7-12 касаний минимум 🎯","100+ постов 😵"], "a": 1, "exp": "7-12 касаний — столько нужно человеку чтобы решиться! Прогревай стабильно 🔥"},
        ],
    },
}

# ── WARMUP SCHOOL (Мария Афонина) ─────────────────────────────────────────────
WARMUP_LESSONS = [
    {
        "title": "🔥 Урок 1: Что такое прогрев",
        "text": (
            "Прогрев — это не реклама в лоб, а постепенное создание доверия.

"
            "📌 Три кита прогрева:
"
            "• Личность — кто ты как человек
"
            "• Экспертность — почему тебе можно доверять
"
            "• Желание — почему людям нужно твоё решение

"
            "💡 Главное правило Марии Афониной:
"
            "Сначала дай ценность — потом продавай!"
        ),
        "xp": 20, "skill": "promo"
    },
    {
        "title": "👤 Урок 2: Личность в блоге",
        "text": (
            "Люди покупают у людей, а не у корпораций.

"
            "📌 Что показывать в блоге:
"
            "• Свой путь и ошибки (честность = доверие)
"
            "• Закулисье работы
"
            "• Личные ценности и принципы
"
            "• Юмор и живые моменты

"
            "💡 Задание: напиши пост-знакомство — кто ты, почему занимаешься SMM?"
        ),
        "xp": 20, "skill": "stories"
    },
    {
        "title": "📖 Урок 3: Сторителлинг",
        "text": (
            "История продаёт лучше любой рекламы.

"
            "📌 Структура сильной истории:
"
            "1. Боль/проблема (с чего всё началось)
"
            "2. Путь (что ты делал)
"
            "3. Результат (что изменилось)
"
            "4. Вывод (урок для читателя)

"
            "💡 Формула Афониной: 'Было — стало — как' = идеальная история для сторис!"
        ),
        "xp": 25, "skill": "stories"
    },
    {
        "title": "💊 Урок 4: Прогрев через боли",
        "text": (
            "Говори о проблемах клиента лучше, чем он сам.

"
            "📌 Как найти боли ЦА:
"
            "• Читай комментарии конкурентов
"
            "• Спрашивай в сторис
"
            "• Изучай форумы и Telegram-каналы

"
            "📌 Типы болей в SMM:
"
            "• Нет охватов
"
            "• Нет продаж
"
            "• Нет времени на контент
"
            "• Непонятно что публиковать

"
            "💡 Пиши не о себе — пиши О НИХ!"
        ),
        "xp": 25, "skill": "target"
    },
    {
        "title": "🧠 Урок 5: Интуитивный маркетинг",
        "text": (
            "Маркетинг — это наука о людях, а не о постах.

"
            "📌 Принципы интуитивного маркетинга (Афонина):
"
            "• Доверяй своей аудитории
"
            "• Не продавай — помогай выбрать
"
            "• Будь последовательна — хаос отпугивает
"
            "• Экспериментируй и анализируй результат

"
            "💡 Ты — не просто SMM-специалист. Ты архитектор доверия! 🏗️"
        ),
        "xp": 30, "skill": "strategy"
    },
]

# ── SMM QUEST ─────────────────────────────────────────────────────────────────
SMM_QUEST = [
    {"q": "Марьяша начала вести Instagram. С чего начать?", "opts": ["Сразу делать рекламу 📢","Оформить шапку профиля и придумать стиль 🎨","Купить подписчиков 💸"], "a": 1, "xp": 20, "exp": "Профиль — это твоя витрина! Сначала упаковка 📦"},
    {"q": "Ты написала пост, лайков мало. Что делать?", "opts": ["Удалить и сдаться 😢","Проанализировать — заголовок, время, хэштеги 🔍","Купить лайки 👍"], "a": 1, "xp": 20, "exp": "Анализ — ключ к росту! Каждый пост — это тест 🧪"},
    {"q": "Клиент хочет 1000 подписчиков за неделю. Ты?", "opts": ["Соглашусь и накручу 🤡","Объясню что нужно время и стратегия 💪","Откажусь от клиента 🏃"], "a": 1, "xp": 30, "exp": "Честность = доверие! Настоящий SMM — это стратегия, а не магия ✨"},
    {"q": "Лучший способ расти в Instagram сейчас?", "opts": ["Покупать рекламу 💰","Reels + коллаборации + регулярный постинг 🎬","Хэштеги 📌"], "a": 1, "xp": 25, "exp": "Reels дают органику, коллабы — аудиторию, регулярность — доверие! 🔥"},
    {"q": "Контент-план нужен?", "opts": ["Нет, буду по вдохновению 🦋","Да, без плана хаос 📅","Только для больших блогов 🤷"], "a": 1, "xp": 20, "exp": "Контент-план = твой компас! Без него сложно расти системно 🧭"},
    {"q": "Марьяша стала SMM-специалистом! Первый шаг?", "opts": ["Взять 10 клиентов сразу 😱","Найти первого клиента и сделать круто 💎","Ждать пока найдут сами 😴"], "a": 1, "xp": 50, "exp": "Один довольный клиент = 10 рекомендаций! Начни с малого и сделай лучшее 🌟"},
]

# ── USER STATE ────────────────────────────────────────────────────────────────
user_data: dict = {}

def get_user(uid: int) -> dict:
    if uid not in user_data:
        user_data[uid] = {
            "xp": 0,
            "skills": {k: 0 for k in SKILLS},
            "badges": [],
            "quest_step": 0,
            "quiz_state": None,
            "warmup_step": 0,
            "chat_history": [],
        }
    return user_data[uid]

def get_level(xp: int):
    current = LEVELS[0]
    for lvl in LEVELS:
        if xp >= lvl[0]:
            current = lvl
    return current

def add_xp(uid: int, amount: int, skill: str = None) -> str:
    u = get_user(uid)
    old_lvl = get_level(u["xp"])[1]
    u["xp"] += amount
    if skill and skill in u["skills"]:
        u["skills"][skill] = min(5, u["skills"][skill] + 1)
    new_lvl = get_level(u["xp"])[1]
    if u["xp"] >= 300 and "xp_300" not in u["badges"]:
        u["badges"].append("xp_300")
    if u["xp"] >= 1000 and "xp_1000" not in u["badges"]:
        u["badges"].append("xp_1000")
    if old_lvl != new_lvl:
        return f"⬆️ НОВЫЙ УРОВЕНЬ: {new_lvl}!"
    return ""

def xp_bar(xp: int) -> str:
    lvls = [l[0] for l in LEVELS]
    cur_idx = 0
    for i, threshold in enumerate(lvls):
        if xp >= threshold:
            cur_idx = i
    if cur_idx < len(LEVELS) - 1:
        cur_min = lvls[cur_idx]
        nxt = lvls[cur_idx + 1]
        progress = int((xp - cur_min) / (nxt - cur_min) * 10)
        bar = "🟣" * progress + "⬜" * (10 - progress)
        return f"{bar} {xp}/{nxt} XP"
    return "🟣" * 10 + " МАКСИМУМ!"

def profile_text(uid: int) -> str:
    u = get_user(uid)
    lvl = get_level(u["xp"])
    lines = [
        f"👩‍💻 *Профиль Марьяши*",
        f"",
        f"Ранг: {lvl[1]}",
        f"💬 {lvl[2]}",
        f"",
        f"⚡ XP: {u['xp']}",
        f"{xp_bar(u['xp'])}",
        f"",
        f"🎯 Скиллы:",
    ]
    for k, name in SKILLS.items():
        stars = "⭐" * u["skills"][k] + "☆" * (5 - u["skills"][k])
        lines.append(f"  {name}: {stars}")
    if u["badges"]:
        lines.append("")
        lines.append("🏆 Бейджи: " + " ".join(BADGES[b] for b in u["badges"] if b in BADGES))
    return "\n".join(lines)

# ── AI AGENT ──────────────────────────────────────────────────────────────────
AI_SYSTEM_PROMPT = """Ты — Марьяша-бот, крутой SMM-наставник для 16-летней девочки по имени Марьяша.

Твоя роль: дружелюбный, энергичный наставник по SMM, который говорит на языке молодёжи.

Правила общения:
- Говори легко, живо, как подруга — не как учебник
- Используй эмодзи уместно 🔥
- Отвечай кратко и по делу (3-5 предложений max)
- Знаешь SMM: контент-стратегии, прогревы, Reels, визуал, ЦА, аналитику
- Вдохновляй и поддерживай — Марьяша только начинает!
- Если вопрос не про SMM — мягко верни к теме
- Помни контекст разговора

Твои знания основаны на курсе Марии Афониной:
- Прогрев = создание доверия через ценность и личность
- Контент-микс: 70% польза / 20% жизнь / 10% продажи
- Сторителлинг: было — стало — как
- Reels — главный инструмент охватов сейчас
- ЦА: изучай боли, говори о них лучше клиента

Если спрашивают что-то конкретное про SMM — давай практический совет.
Если просто хотят поговорить — будь дружелюбной и веди к обучению."""

async def ai_chat(uid: int, user_message: str) -> str:
    if not OPENAI_API_KEY:
        return (
            "🤖 AI-агент пока спит... Чтобы он заработал, "
            "нужно добавить OPENAI_API_KEY в настройки! "
            "А пока — используй меню ниже 👇"
        )
    try:
        import httpx
        u = get_user(uid)
        history = u.get("chat_history", [])
        history.append({"role": "user", "content": user_message})
        if len(history) > 20:
            history = history[-20:]
        messages = [{"role": "system", "content": AI_SYSTEM_PROMPT}] + history
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "max_tokens": 300,
                    "temperature": 0.8,
                },
            )
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": reply})
        u["chat_history"] = history[-20:]
        return reply
    except Exception as e:
        return f"🤖 Упс, что-то пошло не так: {str(e)[:100]}. Попробуй ещё раз!"

# ── KEYBOARDS ─────────────────────────────────────────────────────────────────
def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👩‍💻 Мой профиль и скиллы", callback_data="profile")],
        [InlineKeyboardButton("🔥 Школа Прогревов (квест)", callback_data="warmup_menu")],
        [InlineKeyboardButton("📝 Квизы — прокачай знания", callback_data="quiz_menu")],
        [InlineKeyboardButton("⚔️ SMM-Квест", callback_data="quest_start")],
        [InlineKeyboardButton("💬 Спросить AI-наставника", callback_data="ai_chat_info")],
    ])

def warmup_kb(step: int):
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
    text = (
        f"👋 Привет, Марьяша! Я твой SMM-наставник 💙\n\n"
        f"Твой ранг: {lvl[1]} | ХР: {u['xp']}\n\n"
        f"🎮 Прокачивай скиллы, зарабатывай ХР и становись\n"
        f"👑 Легендой SMM — у тебя всё получится!\n\n"
        f"💬 Кстати, ты можешь просто написать мне любой вопрос\n"
        f"про SMM — отвечу как живой наставник! 🤖\n\n"
        f"Выбери с чего начнём:"
    )
    await update.message.reply_text(text, reply_markup=main_kb(), parse_mode="Markdown")

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msg = update.message.text.strip()
    if msg.startswith("/"):
        return
    await update.message.chat.send_action("typing")
    reply = await ai_chat(uid, msg)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Главное меню", callback_data="start")]
    ])
    await update.message.reply_text(reply, reply_markup=kb)

async def cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = get_user(uid)
    data = q.data

    if data == "start":
        lvl = get_level(u["xp"])
        text = (
            f"👋 Привет! Ранг: {lvl[1]} | ХР: {u['xp']}\n\n"
            f"💬 Пиши любой вопрос про SMM — отвечу как живой наставник! 🤖\n\n"
            f"Или выбери раздел:"
        )
        await q.edit_message_text(text, reply_markup=main_kb(), parse_mode="Markdown")

    elif data == "profile":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Назад", callback_data="start")]])
        await q.edit_message_text(profile_text(uid), reply_markup=kb, parse_mode="Markdown")

    elif data == "ai_chat_info":
        text = (
            "💬 *AI-наставник активирован!*\n\n"
            "Просто напиши мне любой вопрос прямо в чат — и я отвечу!\n\n"
            "Например:\n"
            "• Как сделать крутой Reels?\n"
            "• Что такое прогрев?\n"
            "• Как найти ЦА?\n"
            "• Помоги придумать контент-план\n\n"
            "🤖 Я всегда здесь и отвечаю быстро!"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Назад", callback_data="start")]])
        await q.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

    elif data == "warmup_menu":
        await q.edit_message_text(
            "🔥 *Школа Прогревов* (по Марии Афониной)\n\nВыбери урок:",
            reply_markup=warmup_kb(u["warmup_step"]),
            parse_mode="Markdown"
        )

    elif data.startswith("warmup_"):
        idx = int(data.split("_")[1])
        lesson = WARMUP_LESSONS[idx]
        lvl_up = add_xp(uid, lesson["xp"], lesson["skill"])
        if "first_quiz" not in u["badges"]:
            u["badges"].append("first_quiz")
        if idx >= u["warmup_step"]:
            u["warmup_step"] = idx + 1
        btns = []
        if idx + 1 < len(WARMUP_LESSONS):
            btns.append([InlineKeyboardButton("➡️ Следующий урок", callback_data=f"warmup_{idx+1}")])
        btns.append([InlineKeyboardButton("📚 Все уроки", callback_data="warmup_menu")])
        btns.append([InlineKeyboardButton("🏠 Главная", callback_data="start")])
        text = (
            f"{lesson['title']}\n\n"
            f"{lesson['text']}\n\n"
            f"✨ +{lesson['xp']} XP получено!\n"
            + (f"\n{lvl_up}" if lvl_up else "")
        )
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(btns))

    elif data == "quiz_menu":
        await q.edit_message_text(
            "📝 *Квизы*\n\nКаждый правильный ответ = ХР + прокачка скилла!\n\nВыбери тему:",
            reply_markup=quiz_menu_kb(),
            parse_mode="Markdown"
        )

    elif data.startswith("quiz_") and not data.startswith("quiz_ans_"):
        qid = data[5:]
        if qid not in QUIZZES:
            return
        quiz = QUIZZES[qid]
        if "first_quiz" not in u["badges"]:
            u["badges"].append("first_quiz")
        u["quiz_state"] = {"id": qid, "step": 0, "correct": 0}
        q0 = quiz["qs"][0]
        btns = [[InlineKeyboardButton(f"{o}", callback_data=f"quiz_ans_{qid}_0_{i}")] for i, o in enumerate(q0["opts"])]
        await q.edit_message_text(
            f"📝🔥 {quiz['title']}\nВопрос 1/{len(quiz['qs'])}\n\n❓ {q0['q']}",
            reply_markup=InlineKeyboardMarkup(btns)
        )

    elif data.startswith("quiz_ans_"):
        parts = data.split("_")
        qid = parts[2]
        step = int(parts[3])
        chosen = int(parts[4])
        if qid not in QUIZZES:
            return
        quiz = QUIZZES[qid]
        qs = quiz["qs"]
        correct = qs[step]["a"] == chosen
        exp_text = qs[step]["exp"]
        if u.get("quiz_state") and u["quiz_state"].get("id") == qid:
            if correct:
                u["quiz_state"]["correct"] = u["quiz_state"].get("correct", 0) + 1
        xp_gain = quiz["sp"] if correct else 0
        lvl_up = add_xp(uid, xp_gain, quiz["skill"] if correct else None) if correct else ""
        result = f"✅ Верно! +{xp_gain} XP\n\n💡 {exp_text}" if correct else f"❌ Не совсем...\n\n💡 {exp_text}"
        if step + 1 < len(qs):
            nq = qs[step + 1]
            btns = [[InlineKeyboardButton(f"{o}", callback_data=f"quiz_ans_{qid}_{step+1}_{i}")] for i, o in enumerate(nq["opts"])]
            btns.append([InlineKeyboardButton("🏠 Выйти", callback_data="quiz_menu")])
            await q.edit_message_text(
                f"{result}\n\n{'─'*20}\n\n📝 {quiz['title']}\nВопрос {step+2}/{len(qs)}\n\n❓ {nq['q']}",
                reply_markup=InlineKeyboardMarkup(btns)
            )
        else:
            correct_count = u.get("quiz_state", {}).get("correct", 0) + (1 if correct else 0)
            total = len(qs)
            if "quest_done" not in u["badges"] and correct_count == total:
                u["badges"].append("quest_done")
            btns = [
                [InlineKeyboardButton("📝 Ещё квиз", callback_data="quiz_menu")],
                [InlineKeyboardButton("👩‍💻 Мой профиль", callback_data="profile")],
                [InlineKeyboardButton("🏠 Главная", callback_data="start")],
            ]
            await q.edit_message_text(
                f"{result}\n\n{'═'*20}\n\n🎉 Квиз завершён! {correct_count}/{total} верных\n{lvl_up}",
                reply_markup=InlineKeyboardMarkup(btns)
            )

    elif data == "quest_start":
        step = u.get("quest_step", 0)
        if step >= len(SMM_QUEST):
            await q.edit_message_text(
                "🏆 Ты прошла весь SMM-Квест! Ты настоящий специалист!\n\nДержи финальный бейдж: ⚔️",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главная", callback_data="start")]])
            )
            return
        item = SMM_QUEST[step]
        btns = [[InlineKeyboardButton(o, callback_data=f"quest_ans_{step}_{i}")] for i, o in enumerate(item["opts"])]
        btns.append([InlineKeyboardButton("🏠 Выйти", callback_data="start")])
        await q.edit_message_text(
            f"⚔️ *SMM-Квест* | Шаг {step+1}/{len(SMM_QUEST)}\n\n{item['q']}",
            reply_markup=InlineKeyboardMarkup(btns),
            parse_mode="Markdown"
        )

    elif data.startswith("quest_ans_"):
        parts = data.split("_")
        step = int(parts[2])
        chosen = int(parts[3])
        item = SMM_QUEST[step]
        correct = item["a"] == chosen
        lvl_up = add_xp(uid, item["xp"] if correct else 5, "strategy") if correct else add_xp(uid, 5)
        if correct:
            u["quest_step"] = max(u.get("quest_step", 0), step + 1)
        result = f"✅ Верно! +{item['xp']} XP\n\n💡 {item['exp']}" if correct else f"❌ Не то...\n\n💡 {item['exp']}"
        btns = [[InlineKeyboardButton("➡️ Следующий шаг", callback_data="quest_start")],
                [InlineKeyboardButton("🏠 Главная", callback_data="start")]]
        await q.edit_message_text(
            f"{result}\n\n{lvl_up if lvl_up else ''}",
            reply_markup=InlineKeyboardMarkup(btns)
        )

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("🚀 Марьяша-бот запущен с AI-агентом!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
