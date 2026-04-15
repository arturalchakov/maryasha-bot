import os
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

LEVELS = [
    (0,    "🥚 Яйцо",       "Только начинаешь — и это уже круто!"),
    (100,  "🐣 Новичок",    "Первые шаги сделаны, продолжай!"),
    (300,  "⚡ Практик",    "Уже что-то умеешь, огонь!"),
    (600,  "🔥 Специалист", "Растёшь на глазах!"),
    (1000, "💎 Профи",      "Красавица! Топ-уровень!"),
    (1500, "🌟 Эксперт",    "Люди учатся у тебя!"),
    (2000, "👑 ЛЕГЕНДА",    "Ты легенда! Гордимся тобой!"),
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
    "first_quiz":  "🏅 Первый квиз",
    "quest_done":  "⚔️ Квестер",
    "xp_300":      "🚀 300 XP",
    "xp_1000":     "💎 1000 XP",
    "skill_50":    "💪 Прокачка скилла",
    "daily":       "📅 Дисциплина",
    "all_quizzes": "🧠 Умница — все квизы!",
}

DAILY = [
    "📸 Сними 3 сторис: экспертная + личная + вопрос аудитории",
    "✍️ Напиши пост по формуле: Боль → Решение → Результат → CTA",
    "🔍 Разбери 3 аккаунта конкурентов: что работает — запиши",
    "💬 Ответь на 10 комментариев в своей нише от лица эксперта",
    "🎨 Создай новую рубрику и сделай шаблон в Canva",
    "📊 Зайди в аналитику: какой пост дал больший охват и почему",
    "🎥 Запиши Reels 15-30 сек с одним полезным лайфхаком",
    "🤝 Найди 5 блогеров для потенциального коллаба",
    "📝 Составь контент-план на 7 дней вперёд",
    "💡 Набросай 10 идей для постов — просто быстро, без цензуры",
]

PROMO_QUEST = [
    {
        "title": "🔥 Школа прогревов — Уровень 1",
        "text": "Мария говорит: прогрев — это не реклама!\n\nЧто такое прогрев в SMM?",
        "opts": [
            ("Пост с ценой товара 💸", False, "content"),
            ("Контент, который создаёт доверие перед продажей ❤️", True, "promo"),
            ("Таргетированная реклама 📢", False, "target"),
        ],
        "ok": "💥 Точно! Прогрев = история + ценность + доверие. +25 XP!",
        "fail": "❌ Нет! Прогрев — это контент, который греет аудиторию перед продажей.",
        "xp": 25, "skill": "promo", "sp": 15,
    },
    {
        "title": "🔥 Школа прогревов — Уровень 2",
        "text": "Какой контент лучше всего прогревает?",
        "opts": [
            ("Красивые фото 📸", False, "visual"),
            ("Разборы ошибок + кейсы + личность 🎯", True, "stories"),
            ("Репосты 🔄", False, "content"),
        ],
        "ok": "🔥 Да! Разборы + кейсы + личность — мощный коктейль прогрева! +30 XP!",
        "fail": "❌ Лучший прогрев: разборы, кейсы и твоя личность!",
        "xp": 30, "skill": "stories", "sp": 20,
    },
    {
        "title": "🔥 Школа прогревов — Уровень 3",
        "text": "Зачем показывать свою личность в блоге?",
        "opts": [
            ("Чтобы было красиво ✨", False, "visual"),
            ("Люди покупают у людей — личность = доверие = продажи 💛", True, "stories"),
            ("Это вообще не нужно 🤷", False, "content"),
        ],
        "ok": "💎 Правильно! Личность — это твой главный актив в соцсетях! +30 XP!",
        "fail": "❌ Личность в блоге — ключ к доверию аудитории!",
        "xp": 30, "skill": "stories", "sp": 20,
    },
    {
        "title": "🔥 Школа прогревов — Уровень 4",
        "text": "Формула идеального сторителлинга?",
        "opts": [
            ("Длинный текст без структуры 📄", False, "content"),
            ("Герой → Проблема → Решение → Трансформация 🚀", True, "stories"),
            ("Просто факты и цифры 📊", False, "strategy"),
        ],
        "ok": "✨ Бомба! Герой → Проблема → Решение → Трансформация = история, которая цепляет! +35 XP!",
        "fail": "❌ Цепляет структура: Герой → Проблема → Решение → Трансформация!",
        "xp": 35, "skill": "stories", "sp": 25,
    },
    {
        "title": "👑 Школа прогревов — ФИНАЛ!",
        "text": "Как прогревать без явных продаж?",
        "opts": [
            ("Каждый день писать о скидках 😅", False, "content"),
            ("Жить интересно: ценности, мысли, закулисье 🌟", True, "promo"),
            ("Молчать и ждать 🤫", False, "strategy"),
        ],
        "ok": "👑 ЛЕГЕНДА! Интуитивный маркетинг — это образ жизни который продаёт сам себя! +50 XP!",
        "fail": "❌ Прогрев без прогревов = твоя жизнь, ценности и закулисье!",
        "xp": 50, "skill": "promo", "sp": 30,
    },
]

QUIZZES = {
    "smm_q": {
        "title": "📱 SMM — базовые знания",
        "skill": "strategy", "sp": 10,
        "qs": [
            {"q": "Что такое ERR?", "opts": ["Engagement Rate by Reach 📊","Error Rate Report ❌","Email Response Rate 📧"], "a": 0, "exp": "ERR — вовлечённость по охвату. Чем выше — тем лучше! 📈"},
            {"q": "Какой формат сейчас даёт максимальный охват?", "opts": ["Статичные посты 🖼️","Reels/Shorts 🎬","Длинные видео 🎥"], "a": 1, "exp": "Reels и Shorts рвут охваты — алгоритмы их обожают! 🚀"},
            {"q": "Как часто постить сторис?", "opts": ["Раз в неделю 😴","Каждый день ✅","Раз в месяц 🗓️"], "a": 1, "exp": "Ежедневные сторис = живая связь с аудиторией! ❤️"},
        ],
    },
    "content_q": {
        "title": "📊 Контент-стратегия",
        "skill": "content", "sp": 10,
        "qs": [
            {"q": "Что такое TOV?", "opts": ["Тип визуала 🎨","Голос и стиль бренда 🗣️","Вид рекламы 📢"], "a": 1, "exp": "TOV (Tone of Voice) — как твой бренд разговаривает! 💬"},
            {"q": "Лучший контент-микс?", "opts": ["100% продажи 💰","50% польза / 50% продажи ⚖️","70% польза / 20% жизнь / 10% продажи 🎯"], "a": 2, "exp": "70/20/10 — золотой стандарт! Сначала давай ценность 💛"},
            {"q": "Контент-воронка — это?", "opts": ["Слив контента 🚽","Путь от знакомства до покупки 🎯","Список тем для постов 📝"], "a": 1, "exp": "Воронка ведёт человека от 'кто это?' до 'хочу купить!' 🛍️"},
        ],
    },
    "visual_q": {
        "title": "🎨 Визуал и дизайн",
        "skill": "visual", "sp": 10,
        "qs": [
            {"q": "Максимум шрифтов в одном дизайне?", "opts": ["1-2 шрифта ✅","5-6 шрифтов 😵","Без ограничений 🎪"], "a": 0, "exp": "1-2 шрифта — золотое правило! Больше = визуальный хаос 🎨"},
            {"q": "Что такое визуальная сетка аккаунта?", "opts": ["Таблица с данными 📊","Единый стиль всех постов в профиле ✨","Вид рекламы 📢"], "a": 1, "exp": "Сетка = первое впечатление от профиля. Должна быть 🔥!"},
            {"q": "Лучший бесплатный инструмент для дизайна?", "opts": ["Photoshop 💸","Canva ✅","Paint 😅"], "a": 1, "exp": "Canva — твой лучший друг! Бесплатно и мощно 🖌️"},
        ],
    },
    "promo_q": {
        "title": "🔥 Прогревы (по Марии)",
        "skill": "promo", "sp": 15,
        "qs": [
            {"q": "Прогрев — это?", "opts": ["Реклама в лоб 📢","Контент, создающий доверие перед продажей ❤️","Скидки и акции 💸"], "a": 1, "exp": "Прогрев = разогрев через ценность и историю 🔥"},
            {"q": "Лучший тип прогревающего контента?", "opts": ["Прайс-листы 💰","Разборы ошибок и кейсы 🎯","Репосты чужого контента 🔄"], "a": 1, "exp": "Разборы и кейсы = экспертность + доверие 💪"},
            {"q": "FOMO — это?", "opts": ["Страх упустить возможность ⚡","Название приложения 📱","Вид рекламы 📢"], "a": 0, "exp": "FOMO (Fear Of Missing Out) — мощнейший триггер в маркетинге! ⚡"},
        ],
    },
}

PLANS = {
    "smm": ["📌 День 1: Анализ ЦА — боли, желания, портрет клиента","📌 День 2: Конкурентный анализ — что работает в нише","📌 День 3: Рубрики и контент-микс 70/20/10","📌 День 4: Продающий пост с историей","📌 День 5: Reels/Shorts — идея и сценарий","📌 День 6: Карусель — обучающий контент","📌 День 7: Анализ статистики и корректировка"],
    "content": ["📌 День 1: TOV — голос и стиль бренда","📌 День 2: Контент-стратегия на месяц","📌 День 3: Продающий текст для лендинга","📌 День 4: Email-рассылка","📌 День 5: Сторителлинг бренда","📌 День 6: UGC — отзывы и кейсы","📌 День 7: Анализ и корректировка"],
    "visual": ["📌 День 1: Определить фирменные цвета (3-4 цвета)","📌 День 2: Выбрать 2 шрифта и создать шаблоны","📌 День 3: Сделать 5 шаблонов постов в Canva","📌 День 4: Оформить highlights в едином стиле","📌 День 5: Создать шаблоны для сторис","📌 День 6: Сделать пресет для фото","📌 День 7: Проверить единство сетки профиля"],
}

def get_level(xp):
    lvl = LEVELS[0]
    for l in LEVELS:
        if xp >= l[0]: lvl = l
    return lvl

def xp_bar(xp):
    current = get_level(xp)
    idx = LEVELS.index(current)
    if idx + 1 < len(LEVELS):
        nxt = LEVELS[idx + 1]
        prev_xp = current[0]
        prog = min(10, int((xp - prev_xp) / (nxt[0] - prev_xp) * 10))
        bar = "█" * prog + "░" * (10 - prog)
        return f"[{bar}] {xp - prev_xp}/{nxt[0] - prev_xp} до {nxt[1]}"
    return "🔥 МАКСИМАЛЬНЫЙ УРОВЕНЬ!"

def build_profile(ud):
    xp = ud.get("xp", 0)
    _, lvl, desc = get_level(xp)
    skills = ud.get("skills", {k: 0 for k in SKILLS})
    badges = ud.get("badges", [])
    s_lines = ""
    for k, name in SKILLS.items():
        v = skills.get(k, 0)
        b = "█" * min(10, v // 10) + "░" * (10 - min(10, v // 10))
        s_lines += f"\n{name}: [{b}] {v}pts"
    bdg = "  ".join(BADGES[b] for b in badges) if badges else "Пока нет 😴 — проходи квизы!"
    return (f"⚡ *Профиль Марьяши*\n\n"
            f"{lvl} | *{xp} XP*\n_{desc}_\n{xp_bar(xp)}\n\n"
            f"*🎮 Скиллы:*{s_lines}\n\n"
            f"*🏅 Значки:*\n{bdg}")

def add_xp(ud, amount, skill=None, skill_pts=0):
    ud["xp"] = ud.get("xp", 0) + amount
    if skill:
        sk = ud.setdefault("skills", {k: 0 for k in SKILLS})
        sk[skill] = sk.get(skill, 0) + skill_pts
        badges = ud.setdefault("badges", [])
        if sk[skill] >= 50 and "skill_50" not in badges:
            badges.append("skill_50")
    badges = ud.setdefault("badges", [])
    if ud["xp"] >= 300 and "xp_300" not in badges: badges.append("xp_300")
    if ud["xp"] >= 1000 and "xp_1000" not in badges: badges.append("xp_1000")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "xp" not in context.user_data:
        context.user_data.update({"xp": 0, "skills": {k: 0 for k in SKILLS}, "badges": []})
    ud = context.user_data
    xp = ud.get("xp", 0)
    _, lvl, _ = get_level(xp)
    kb = [
        [InlineKeyboardButton("👤 Мой профиль и скиллы", callback_data="profile")],
        [InlineKeyboardButton("🔥 Школа Прогревов (квест)", callback_data="promo_start")],
        [InlineKeyboardButton("📝 Квизы — прокачай знания", callback_data="quiz_menu")],
        [InlineKeyboardButton("📅 Контент-план на 7 дней", callback_data="plan_menu")],
        [InlineKeyboardButton("🎯 Задание дня (+30 XP)", callback_data="daily")],
        [InlineKeyboardButton("🏅 Мои достижения", callback_data="badges")],
    ]
    text = (f"👋 Привет, Марьяша! Я твой SMM-наставник 💙\n\n"
            f"Твой ранг: *{lvl}* | XP: *{xp}*\n\n"
            f"🎮 Прокачивай скиллы, зарабатывай XP и становись\n"
            f"👑 *Легендой SMM* — у тебя всё получится!\n\n"
            f"Выбери с чего начнём:")
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    text = build_profile(context.user_data)
    kb = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back")]]
    await q.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def badges_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    got = context.user_data.get("badges", [])
    lines = []
    for k, v in BADGES.items():
        lines.append(f"{'✅' if k in got else '🔒'} {v}")
    kb = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back")]]
    await q.message.edit_text("🏅 *Достижения*\n\n" + "\n".join(lines), reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    task = DAILY[datetime.datetime.now().day % len(DAILY)]
    kb = [[InlineKeyboardButton("✅ Выполнила! +20 XP", callback_data="daily_done")], [InlineKeyboardButton("🏠 Меню", callback_data="back")]]
    await q.message.edit_text(f"🎯 *Задание дня:*\n\n{task}\n\n💡 Выполни и получи +20 XP!", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def daily_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    add_xp(context.user_data, 20)
    bgs = context.user_data.setdefault("badges", [])
    if "daily" not in bgs: bgs.append("daily")
    _, lvl, _ = get_level(context.user_data["xp"])
    await q.message.edit_text(f"🔥 Огонь! +20 XP заработано!\n\nТвой ранг: *{lvl}*\n\nТак держать, ты растёшь каждый день! 🚀",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню", callback_data="back")]]), parse_mode="Markdown")

async def promo_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    context.user_data.update({"pq_idx": 0, "pq_xp": 0})
    await promo_show(q, context)

async def promo_show(q, context):
    idx = context.user_data.get("pq_idx", 0)
    if idx >= len(PROMO_QUEST):
        earned = context.user_data.get("pq_xp", 0)
        add_xp(context.user_data, earned)
        bgs = context.user_data.setdefault("badges", [])
        if "quest_done" not in bgs: bgs.append("quest_done")
        _, lvl, _ = get_level(context.user_data["xp"])
        await q.message.edit_text(
            f"🏆 *КВЕСТ ПРОЙДЕН!*\n\n"
            f"⭐ Заработала: *{earned} XP*\n"
            f"👑 Ранг: *{lvl}*\n\n"
            f"Ты прошла Школу Прогревов Марии Афониной!\nТы — огонь! 🔥",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👤 Посмотреть профиль", callback_data="profile")],
                [InlineKeyboardButton("🏠 Меню", callback_data="back")]
            ]), parse_mode="Markdown"); return
    lv = PROMO_QUEST[idx]
    kb = [[InlineKeyboardButton(f"{chr(65+i)}) {t}", callback_data=f"pqa_{i}")] for i,(t,_,_) in enumerate(lv["opts"])]
    kb.append([InlineKeyboardButton("🏠 Выйти", callback_data="back")])
    await q.message.edit_text(
        f"{lv['title']} | ⭐ {context.user_data.get('pq_xp',0)} XP\n\n{lv['text']}",
        reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def promo_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    idx = context.user_data.get("pq_idx", 0)
    ans = int(q.data.replace("pqa_",""))
    lv = PROMO_QUEST[idx]
    _, correct, skill = lv["opts"][ans]
    if correct:
        context.user_data["pq_xp"] = context.user_data.get("pq_xp", 0) + lv["xp"]
        skills = context.user_data.setdefault("skills", {k: 0 for k in SKILLS})
        skills[lv["skill"]] = skills.get(lv["skill"], 0) + lv["sp"]
        fb = f"✅ {lv['ok']}\n\n+{lv['sp']} к скиллу {SKILLS[lv['skill']]}"
    else:
        fb = f"❌ {lv['fail']}"
    context.user_data["pq_idx"] = idx + 1
    await q.message.edit_text(fb, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Следующий уровень", callback_data="promo_next")]]), parse_mode="Markdown")

async def promo_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); await promo_show(q, context)

async def quiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("📱 SMM — базовые знания", callback_data="qz_smm_q")],
        [InlineKeyboardButton("📊 Контент-стратегия", callback_data="qz_content_q")],
        [InlineKeyboardButton("🎨 Визуал и дизайн", callback_data="qz_visual_q")],
        [InlineKeyboardButton("🔥 Прогревы по Марии", callback_data="qz_promo_q")],
        [InlineKeyboardButton("🏠 Назад", callback_data="back")],
    ]
    await q.message.edit_text("📝 *Квизы*\n\nКаждый правильный ответ = XP + прокачка скилла!\n\nВыбери тему:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    key = q.data.replace("qz_","")
    context.user_data.update({"qk": key, "qi": 0, "qs": 0})
    await quiz_show(q, context)

async def quiz_show(q, context):
    key = context.user_data["qk"]; qi = context.user_data.get("qi", 0); quiz = QUIZZES[key]
    if qi >= len(quiz["qs"]):
        sc = context.user_data.get("qs", 0); tot = len(quiz["qs"])
        xp_g = sc * 15
        add_xp(context.user_data, xp_g, quiz["skill"], quiz["sp"] * sc)
        bgs = context.user_data.setdefault("badges", [])
        if "first_quiz" not in bgs: bgs.append("first_quiz")
        if len([k for k in QUIZZES if context.user_data.get(f"done_{k}")]) >= len(QUIZZES) - 1:
            if "all_quizzes" not in bgs: bgs.append("all_quizzes")
        context.user_data[f"done_{key}"] = True
        e = "🏆" if sc==tot else "👍" if sc>=tot//2 else "📚"
        _, lvl, _ = get_level(context.user_data["xp"])
        await q.message.edit_text(
            f"{e} *Квиз завершён!*\n\n✅ {sc}/{tot} правильных\n⭐ +{xp_g} XP\n👑 Ранг: *{lvl}*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Ещё раз", callback_data=f"qz_{key}")],
                [InlineKeyboardButton("📝 Другой квиз", callback_data="quiz_menu")],
                [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
                [InlineKeyboardButton("🏠 Меню", callback_data="back")],
            ]), parse_mode="Markdown"); return
    question = quiz["qs"][qi]
    kb = [[InlineKeyboardButton(f"{chr(65+i)}) {o}", callback_data=f"qza_{i}")] for i,o in enumerate(question["opts"])]
    await q.message.edit_text(
        f"📝 *{quiz['title']}*\nВопрос {qi+1}/{len(quiz['qs'])}\n\n❓ {question['q']}",
        reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quiz_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    ans = int(q.data.replace("qza_","")); key = context.user_data["qk"]; qi = context.user_data.get("qi", 0)
    question = QUIZZES[key]["qs"][qi]
    if ans == question["a"]:
        context.user_data["qs"] = context.user_data.get("qs", 0) + 1
        fb = f"✅ *Верно! +15 XP*\n\n💡 {question['exp']}"
    else:
        fb = f"❌ *Неверно.* Правильно: *{question['opts'][question['a']]}*\n\n💡 {question['exp']}"
    context.user_data["qi"] = qi + 1
    await q.message.edit_text(fb, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Далее", callback_data="qz_next")]]), parse_mode="Markdown")

async def quiz_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); await quiz_show(q, context)

async def plan_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("📱 SMM-специалист", callback_data="pl_smm")],
        [InlineKeyboardButton("✍️ Контент-мейкер", callback_data="pl_content")],
        [InlineKeyboardButton("🎨 Визуал-дизайнер", callback_data="pl_visual")],
        [InlineKeyboardButton("🏠 Назад", callback_data="back")],
    ]
    await q.message.edit_text("📅 *Контент-план на 7 дней*\n\nВыбери специализацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def plan_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    key = q.data.replace("pl_",""); plan = PLANS.get(key,[])
    names = {"smm":"📱 SMM-специалист","content":"✍️ Контент-мейкер","visual":"🎨 Визуал-дизайнер"}
    add_xp(context.user_data, 5)
    await q.message.edit_text(
        f"📅 *{names[key]} — план на 7 дней:*\n\n" + "\n\n".join(plan) + "\n\n+5 XP за изучение! 🎯",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад к планам", callback_data="plan_menu")]]),
        parse_mode="Markdown")

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(profile, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(badges_menu, pattern="^badges$"))
    app.add_handler(CallbackQueryHandler(daily, pattern="^daily$"))
    app.add_handler(CallbackQueryHandler(daily_done, pattern="^daily_done$"))
    app.add_handler(CallbackQueryHandler(promo_start, pattern="^promo_start$"))
    app.add_handler(CallbackQueryHandler(promo_ans, pattern="^pqa_"))
    app.add_handler(CallbackQueryHandler(promo_next, pattern="^promo_next$"))
    app.add_handler(CallbackQueryHandler(quiz_menu, pattern="^quiz_menu$"))
    app.add_handler(CallbackQueryHandler(quiz_start, pattern="^qz_(?!next)"))
    app.add_handler(CallbackQueryHandler(quiz_ans, pattern="^qza_"))
    app.add_handler(CallbackQueryHandler(quiz_next, pattern="^qz_next$"))
    app.add_handler(CallbackQueryHandler(plan_menu, pattern="^plan_menu$"))
    app.add_handler(CallbackQueryHandler(plan_show, pattern="^pl_"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.run_polling()

if __name__ == "__main__":
    main()
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

LEVELS = [(0,"🥚 Яйцо SMM","Ты только начинаешь..."),(50,"🐣 Новичок","Первые шаги!"),(150,"📱 Контент-мейкер","Умеешь создавать контент!"),(300,"🔥 SMM-щик","Прогревы — твой конёк!"),(500,"⚡ Стратег","Видишь картину целиком!"),(800,"🦋 Эксперт","Люди идут за советом!"),(1200,"👑 SMM-Легенда","Ты — легенда Instagram!")]
SKILLS = {"content":"✍️ Контент","visual":"🎨 Визуал","warmup":"🔥 Прогревы","stories":"📖 Сторителлинг","analytics":"📊 Аналитика"}
ACHIEVEMENTS = [("quest_done","🏆 Квест-мастер","Прошла первый квест!"),("quiz_perfect","🎯 Снайпер","Все ответы верно!"),("level3","🔥 В огне!","Достигла SMM-щик!"),("level5","⚡ Молния!","Достигла Стратег!")]
CONTENT_PLAN = {"smm":["📅 День 1: Анализ ЦА — боли, желания, портрет","📅 День 2: Конкурентный анализ","📅 День 3: Рубрики 70% польза/20% жизнь/10% продажи","📅 День 4: Продающий пост с историей","📅 День 5: Reels — идея и сценарий","📅 День 6: Карусель — обучающий контент","📅 День 7: Анализ статистики"],"strategy":["📅 День 1: TOV — голос бренда","📅 День 2: Стратегия на месяц","📅 День 3: Продающий текст","📅 День 4: Email-рассылка","📅 День 5: Сторителлинг бренда","📅 День 6: UGC — отзывы и кейсы","📅 День 7: Анализ и корректировка"],"prezentation":["📅 День 1: Структура по Кавасаки","📅 День 2: Визуальный стиль","📅 День 3: Тексты слайдов","📅 День 4: Инфографика","📅 День 5: CTA и триггеры","📅 День 6: Тест-прогон","📅 День 7: Финальная версия"]}
QUEST=[{"title":"🗺️ Уровень 1: Первый клиент","text":"Кафе хочет клиентов через Instagram.\n\n❓ Что делаешь первым?","opts":[("🤳 Сразу постить фото",False,0),("🔍 Анализ ЦА и конкурентов",True,10),("💸 Просить бюджет",False,0)],"ok":"✅ Огонь! Анализ ЦА — фундамент! +10 XP 🔥","fail":"❌ Без анализа ЦА контент мимо цели","skill":"content"},{"title":"🗺️ Уровень 2: Контент-план","text":"Клиент хочет 10 постов в день 😱\n\n❓ Что ответишь?","opts":[("😅 Ок, сделаю!",False,0),("🎯 1-2 поста — качество важнее",True,15),("😤 Отказываюсь",False,0)],"ok":"✅ Красавица! Регулярность > количество! +15 XP 💪","fail":"❌ 10 постов = спам. Алгоритмы накажут","skill":"content"},{"title":"🗺️ Уровень 3: Прогрев","text":"Нужен прогрев перед продажами.\n\n❓ С чего начнёшь?","opts":[("💰 Покажу цены",False,0),("💡 Раскрою личность эксперта",True,20),("📣 Запущу рекламу",False,0)],"ok":"✅ Топ! Сначала доверие — потом продажи! +20 XP 🔥","fail":"❌ Без доверия продажи не работают","skill":"warmup"},{"title":"🗺️ Уровень 4: Сторителлинг","text":"Какой формат поста зайдёт лучше?\n\n❓ Выбери:","opts":[("📋 Список фактов",False,0),("📖 История из жизни с моралью",True,25),("🔢 Цифры и статистика",False,0)],"ok":"✅ Именно! История цепляет эмоции! +25 XP ✨","fail":"❌ История вовлекает лучше цифр","skill":"stories"},{"title":"🗺️ Уровень 5: Визуал","text":"Что важнее в обложке Reels?\n\n❓ Выбери:","opts":[("🌈 Много ярких цветов",False,0),("👁️ Чёткий посыл + читаемый текст",True,30),("🤩 Фото знаменитости",False,0)],"ok":"✅ Супер! Ясность — главное! +30 XP 🎨","fail":"❌ Яркость без смысла не работает","skill":"visual"},{"title":"🏆 Финал!","text":"Главный секрет успешного SMM?\n\n❓ Выбери:","opts":[("🎲 Удача и тренды",False,0),("📊 Стратегия + тест + анализ",True,50),("💰 Большой бюджет",False,0)],"ok":"🏆 ПОБЕДА! Ты — настоящий SMM-профи! +50 XP 👑","fail":"❌ Работает только система!","skill":"analytics"}]
QUIZZES={"smm_q":{"title":"📱 SMM-база","skill":"content","qs":[{"q":"Что такое ERR?","opts":["Engagement Rate by Reach","Error Rate Report","Email Response Rate"],"a":0,"exp":"ERR — вовлечённость по охвату. Чем выше — тем лучше!"},{"q":"Лучший формат для органического охвата?","opts":["Статичные посты","Reels/Shorts","IGTV"],"a":1,"exp":"Reels дают максимальный охват в 2025"},{"q":"Сколько сторис в день?","opts":["1-3","5-10","20+"],"a":0,"exp":"1-3 сторис — оптимально. Качество важнее количества"}]},"warmup_q":{"title":"🔥 Прогревы","skill":"warmup","qs":[{"q":"Из чего состоит прогрев?","opts":["Цены и условия","Доверие + экспертность + желание","Только реклама"],"a":1,"exp":"Прогрев = доверие + экспертность + желание купить"},{"q":"Прогрев через боли — это...?","opts":["Критика аудитории","Показ проблем которые решает продукт","Жалобы"],"a":1,"exp":"Боли — проблемы ЦА. Показываем что понимаем их"},{"q":"Интуитивный маркетинг — это...?","opts":["Продажи без стратегии","Контент из жизни без явных продаж","Реклама"],"a":1,"exp":"Прогрев через жизнь — высший уровень!"}]},"stories_q":{"title":"📖 Сторителлинг","skill":"stories","qs":[{"q":"Что делает историю цепляющей?","opts":["Много деталей","Эмоции + конфликт + мораль","Длинный текст"],"a":1,"exp":"Эмоция + конфликт + вывод = идеальная история"},{"q":"Как лучше начать пост?","opts":["С вывода","С цепляющего вопроса или факта","С представления"],"a":1,"exp":"Первые 2 строки решают всё — это хук"},{"q":"Что такое инфоповод?","opts":["Реклама","Событие дающее повод для контента","Плохие новости"],"a":1,"exp":"Инфоповод = тренд или событие для актуального контента"}]},"visual_q":{"title":"🎨 Визуал","skill":"visual","qs":[{"q":"Сколько шрифтов в дизайне?","opts":["Чем больше — тем лучше","1-2 максимум","5-6 разных"],"a":1,"exp":"1-2 шрифта — золотое правило. Больше = хаос"},{"q":"Что важнее в обложке Reels?","opts":["Красивый фон","Лицо + чёткий текст","Логотип"],"a":1,"exp":"Лицо + текст = максимум кликов"},{"q":"Живой визуал — это...?","opts":["Фото в студии","Настоящие фото из жизни","Пейзажи"],"a":1,"exp":"Живой визуал показывает личность — аудитория это любит"}]}}
WARMUP_LESSONS={"ws_what":("🔥 Что такое прогрев?","Прогрев — путь от \"не знаю тебя\" до \"хочу купить\".\n\n3 этапа:\n1️⃣ *Доверие* — показываешь кто ты\n2️⃣ *Экспертность* — доказываешь что умеешь\n3️⃣ *Желание* — создаёшь мечту о результате\n\n💡 Без прогрева продажи — это спам!","warmup"),"ws_person":("👤 Личность в блоге","Люди покупают у людей, не у брендов!\n\n✅ Что раскрывать:\n• Ценности и убеждения\n• Страхи и победы\n• Юмор и живые моменты\n• Отношение к профессии\n\n💡 Аудитория узнаёт себя в тебе!","warmup"),"ws_story":("📖 Сторителлинг","История продаёт лучше рекламы!\n\n🔑 Формула:\n1. *Ситуация* — контекст\n2. *Конфликт* — проблема\n3. *Действие* — что сделал\n4. *Результат* — что получил\n5. *Мораль* — вывод\n\n💡 Читатель думает: \"Это про меня!\"","stories"),"ws_pain":("😢 Прогрев через боли","Боль — нерешённая проблема ЦА.\n\n✅ Как использовать:\n• Назови боль точно\n• Покажи что понимаешь\n• Намекни что знаешь решение\n\n❌ Нельзя запугивать!\n\n💡 Цель — понимание, не страх","warmup"),"ws_intuitive":("✨ Интуитивный маркетинг","Прогрев без прогревов — высший уровень!\n\n• Показываешь результат в жизни\n• Делишься инсайтами без продажи\n• Живёшь интересно и рассказываешь\n\n💡 Люди сами спрашивают \"Как купить?\"","warmup")}

def get_level(xp):
    lvl = LEVELS[0]
    for item in LEVELS:
        if xp >= item[0]: lvl = item
    return lvl

def xp_bar(xp):
    _, name, _ = get_level(xp)
    nxt = next((l for l in LEVELS if l[0] > xp), None)
    if nxt:
        prv = max((l[0] for l in LEVELS if l[0] <= xp), default=0)
        p = int((xp-prv)/(nxt[0]-prv)*10)
        bar = "🟦"*p+"⬜"*(10-p)
        return f"{bar}\n⚡{xp} XP → до {nxt[1]}: {nxt[0]-xp} XP"
    return "🟦"*10+"\n👑 МАКСИМАЛЬНЫЙ УРОВЕНЬ!"

def profile_text(ud):
    xp=ud.get("xp",0); _,lvl,desc=get_level(xp)
    sk=ud.get("skills",{k:0 for k in SKILLS})
    ach=ud.get("achievements",[])
    sl=""
    for k,label in SKILLS.items():
        pts=sk.get(k,0); stars=min(5,pts//20)
        sl+=f"\n{label}: {'⭐'*stars}{'☆'*(5-stars)} ({pts}pts)"
    at="\n".join([f"🏅 {a[1]}" for a in ACHIEVEMENTS if a[0] in ach]) or "Пока нет — иди прокачиваться! 💪"
    return f"👾 *Профиль Марьяши*\n\n🏷️ Уровень: *{lvl}*\n💬 {desc}\n\n{xp_bar(xp)}\n\n🛠️ *Скиллы:*{sl}\n\n🏅 *Достижения:*\n{at}"

def add_xp(ud, pts, skill=None):
    ud["xp"]=ud.get("xp",0)+pts
    if skill:
        if "skills" not in ud: ud["skills"]={k:0 for k in SKILLS}
        ud["skills"][skill]=ud["skills"].get(skill,0)+pts
    if "achievements" not in ud: ud["achievements"]=[]
    x=ud["xp"]
    if x>=300 and "level3" not in ud["achievements"]: ud["achievements"].append("level3")
    if x>=800 and "level5" not in ud["achievements"]: ud["achievements"].append("level5")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "xp" not in context.user_data:
        context.user_data.update({"xp":0,"skills":{k:0 for k in SKILLS},"achievements":[]})
    xp=context.user_data["xp"]; _,lvl,_=get_level(xp)
    kb=[[InlineKeyboardButton("📅 Контент-план",callback_data="cp_menu"),InlineKeyboardButton("👾 Мой профиль",callback_data="profile")],[InlineKeyboardButton("🎮 SMM-Квест",callback_data="quest_start"),InlineKeyboardButton("📝 Квизы",callback_data="quiz_menu")],[InlineKeyboardButton("🔥 Школа прогревов",callback_data="warmup_school"),InlineKeyboardButton("ℹ️ О боте",callback_data="about")]]
    text=f"👋 Привет! Я *Марьяша* — твой SMM-наставник! 🚀\n\n🏷️ Ты сейчас: *{lvl}* | ⚡{xp} XP\n\nПрокачай скиллы и стань *👑 SMM-Легендой*!\n\nВыбирай куда идём:"
    if update.message:
        await update.message.reply_text(text,reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text,reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    if "xp" not in context.user_data: context.user_data.update({"xp":0,"skills":{k:0 for k in SKILLS},"achievements":[]})
    await q.message.edit_text(profile_text(context.user_data),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Прокачаться!",callback_data="quest_start")],[InlineKeyboardButton("🏠 Меню",callback_data="back")]]),parse_mode="Markdown")

async def cp_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    kb=[[InlineKeyboardButton("📱 SMM-специалист",callback_data="cp_smm")],[InlineKeyboardButton("📊 Контент-стратег",callback_data="cp_strategy")],[InlineKeyboardButton("🖼️ Презентации",callback_data="cp_prezentation")],[InlineKeyboardButton("🔙 Назад",callback_data="back")]]
    await q.message.edit_text("📅 *Контент-план*\n\nВыбери специализацию:",reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")

async def cp_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    key=q.data.replace("cp_",""); plan=CONTENT_PLAN.get(key,[])
    names={"smm":"📱 SMM","strategy":"📊 Стратегия","prezentation":"🖼️ Презентации"}
    add_xp(context.user_data,5,"content")
    await q.message.edit_text(f"📅 *{names[key]} — 7 дней:*\n\n"+"\n\n".join(plan)+"\n\n+5 XP за изучение! 💪",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад",callback_data="cp_menu")]]),parse_mode="Markdown")

async def quest_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    context.user_data["ql"]=0; await quest_show(q,context)

async def quest_show(q, context):
    idx=context.user_data.get("ql",0)
    if idx>=len(QUEST):
        xp=context.user_data.get("xp",0); _,lvl,_=get_level(xp)
        if "achievements" not in context.user_data: context.user_data["achievements"]=[]
        if "quest_done" not in context.user_data["achievements"]: context.user_data["achievements"].append("quest_done")
        await q.message.edit_text(f"🏆 *КВЕСТ ПРОЙДЕН!*\n\n👑 Уровень: *{lvl}*\n{xp_bar(xp)}\n\nТы — настоящая SMM-легенда! 🔥",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👾 Профиль",callback_data="profile")],[InlineKeyboardButton("🏠 Меню",callback_data="back")]]),parse_mode="Markdown"); return
    level=QUEST[idx]; kb=[[InlineKeyboardButton(t,callback_data=f"qa_{i}")] for i,(t,_,_) in enumerate(level["opts"])]; kb.append([InlineKeyboardButton("🏠 Выйти",callback_data="back")])
    xp=context.user_data.get("xp",0)
    await q.message.edit_text(f"{level['title']} | ⚡{xp} XP\n\n{level['text']}",reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")

async def quest_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    idx=context.user_data.get("ql",0); ans=int(q.data.replace("qa_","")); level=QUEST[idx]; t,correct,pts=level["opts"][ans]
    if correct: add_xp(context.user_data,pts,level.get("skill")); fb=level["ok"]
    else: fb=level["fail"]
    context.user_data["ql"]=idx+1; xp=context.user_data.get("xp",0); _,lvl,_=get_level(xp)
    await q.message.edit_text(f"{fb}\n\n🏷️ {lvl} | ⚡{xp} XP",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Дальше!",callback_data="quest_next")]]),parse_mode="Markdown")

async def quest_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); await quest_show(q,context)

async def quiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    kb=[[InlineKeyboardButton("📱 SMM-база",callback_data="qz_smm_q")],[InlineKeyboardButton("🔥 Прогревы",callback_data="qz_warmup_q")],[InlineKeyboardButton("📖 Сторителлинг",callback_data="qz_stories_q")],[InlineKeyboardButton("🎨 Визуал",callback_data="qz_visual_q")],[InlineKeyboardButton("🔙 Назад",callback_data="back")],]
    await q.message.edit_text("📝 *Квизы — прокачай скиллы!*\n\nКаждый правильный ответ = XP ⚡\n\nВыбери тему:",reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")

async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    key=q.data.replace("qz_",""); context.user_data.update({"qkey":key,"qi":0,"qscore":0}); await quiz_show(q,context)

async def quiz_show(q, context):
    key=context.user_data["qkey"]; qi=context.user_data.get("qi",0); quiz=QUIZZES[key]
    if qi>=len(quiz["qs"]):
        s=context.user_data.get("qscore",0); t=len(quiz["qs"]); e="🏆 ИДЕАЛЬНО!" if s==t else "👍 Хорошо!" if s>=t//2 else "📚 Учись ещё!"
        bxp=s*10; add_xp(context.user_data,bxp,quiz.get("skill")); xp=context.user_data.get("xp",0); _,lvl,_=get_level(xp)
        if s==t:
            if "achievements" not in context.user_data: context.user_data["achievements"]=[]
            if "quiz_perfect" not in context.user_data["achievements"]: context.user_data["achievements"].append("quiz_perfect")
        await q.message.edit_text(f"{e}\n\n✅ {s}/{t} правильных\n+{bxp} XP!\n\n🏷️ {lvl} | ⚡{xp} XP",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Ещё раз",callback_data=f"qz_{key}")],[InlineKeyboardButton("📝 Другой квиз",callback_data="quiz_menu")],[InlineKeyboardButton("👾 Профиль",callback_data="profile")],[InlineKeyboardButton("🏠 Меню",callback_data="back")]])); return
    question=quiz["qs"][qi]; kb=[[InlineKeyboardButton(f"{chr(65+i)}) {o}",callback_data=f"qza_{i}")] for i,o in enumerate(question["opts"])]
    await q.message.edit_text(f"📝 *{quiz['title']}* — {qi+1}/{len(quiz['qs'])}\n\n❓ {question['q']}",reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")

async def quiz_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    ans=int(q.data.replace("qza_","")); key=context.user_data["qkey"]; qi=context.user_data.get("qi",0); question=QUIZZES[key]["qs"][qi]
    if ans==question["a"]: context.user_data["qscore"]=context.user_data.get("qscore",0)+1; fb=f"✅ Правильно! 🔥\n\n💡 {question['exp']}"
    else: fb=f"❌ Мимо! Правильно: *{question['opts'][question['a']]}*\n\n💡 {question['exp']}"
    context.user_data["qi"]=qi+1
    await q.message.edit_text(fb,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Дальше!",callback_data="qz_next")]]),parse_mode="Markdown")

async def quiz_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); await quiz_show(q,context)

async def warmup_school(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    kb=[[InlineKeyboardButton("🔥 Что такое прогрев?",callback_data="ws_what")],[InlineKeyboardButton("👤 Личность в блоге",callback_data="ws_person")],[InlineKeyboardButton("📖 Сторителлинг",callback_data="ws_story")],[InlineKeyboardButton("😢 Прогрев через боли",callback_data="ws_pain")],[InlineKeyboardButton("✨ Интуитивный маркетинг",callback_data="ws_intuitive")],[InlineKeyboardButton("🔙 Назад",callback_data="back")]]
    add_xp(context.user_data,3); await q.message.edit_text("🔥 *Школа Прогревов*\nпо материалам Марии Афониной\n\nКаждый урок = +15 XP ⚡\n\nВыбери тему:",reply_markup=InlineKeyboardMarkup(kb),parse_mode="Markdown")

async def warmup_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); key=q.data
    if key not in WARMUP_LESSONS: return
    title,text,skill=WARMUP_LESSONS[key]; add_xp(context.user_data,15,skill); xp=context.user_data.get("xp",0); _,lvl,_=get_level(xp)
    await q.message.edit_text(f"*{title}*\n\n{text}\n\n+15 XP! 🏷️ {lvl} | ⚡{xp} XP",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад к урокам",callback_data="warmup_school")],[InlineKeyboardButton("👾 Профиль",callback_data="profile")]]),parse_mode="Markdown")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    await q.message.edit_text("ℹ️ *Марьяша — SMM-бот с RPG* 👾\n\n🎮 Уровни: 🥚 Яйцо → 👑 Легенда\n⚡ Зарабатывай XP за всё\n🛠️ 5 скиллов для прокачки\n🏅 Достижения\n\n🔥 Школа прогревов — материалы Марии Афониной\n📅 Контент-планы · 🎮 Квест · 📝 Квизы",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню",callback_data="back")]]),parse_mode="Markdown")

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(profile,pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(cp_menu,pattern="^cp_menu$"))
    app.add_handler(CallbackQueryHandler(cp_show,pattern="^cp_(smm|strategy|prezentation)$"))
    app.add_handler(CallbackQueryHandler(quest_start,pattern="^quest_start$"))
    app.add_handler(CallbackQueryHandler(quest_ans,pattern="^qa_"))
    app.add_handler(CallbackQueryHandler(quest_next,pattern="^quest_next$"))
    app.add_handler(CallbackQueryHandler(quiz_menu,pattern="^quiz_menu$"))
    app.add_handler(CallbackQueryHandler(quiz_start,pattern="^qz_(?!next)"))
    app.add_handler(CallbackQueryHandler(quiz_ans,pattern="^qza_"))
    app.add_handler(CallbackQueryHandler(quiz_next,pattern="^qz_next$"))
    app.add_handler(CallbackQueryHandler(warmup_school,pattern="^warmup_school$"))
    app.add_handler(CallbackQueryHandler(warmup_lesson,pattern="^ws_"))
    app.add_handler(CallbackQueryHandler(about,pattern="^about$"))
    app.add_handler(CallbackQueryHandler(back,pattern="^back$"))
    app.run_polling()

if __name__ == "__main__":
    main()
