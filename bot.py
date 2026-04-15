import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ===== КОНТЕНТ-ПЛАНЫ =====
CONTENT_PLAN = {
    "smm": ["День 1: Анализ ЦА — боли, желания, портрет клиента","День 2: Конкурентный анализ — что работает в нише","День 3: Рубрики — контент-микс 70/20/10","День 4: Продающий пост с историей","День 5: Reels/Shorts — идея и сценарий","День 6: Карусель — обучающий контент","День 7: Анализ статистики и корректировка"],
    "strategy": ["День 1: TOV — голос и стиль бренда","День 2: Контент-стратегия на месяц","День 3: Продающий текст для лендинга","День 4: Email-рассылка","День 5: Сторителлинг бренда","День 6: UGC — отзывы и кейсы","День 7: Анализ и корректировка"],
    "prezentation": ["День 1: Структура — 10 слайдов по Кавасаки","День 2: Визуальный стиль (цвета, шрифты)","День 3: Тексты для слайдов","День 4: Инфографика и данные","День 5: CTA и триггеры","День 6: Тест-прогон на аудитории","День 7: Финальная версия"],
}

# ===== КВЕСТ SMM =====
QUEST = [
    {"title": "Уровень 1: Первый клиент", "text": "Кафе хочет клиентов через Instagram.\n\nЧто делаешь первым?", "opts": [("Сразу постить фото",False),("Анализ ЦА и конкурентов",True),("Просить бюджет",False)], "ok": "Верно! Анализ ЦА — фундамент. +10 очков!", "fail": "Без анализа ЦА контент не попадёт в цель.", "pts": 10},
    {"title": "Уровень 2: Контент-план", "text": "Клиент хочет 10 постов в день!\n\nЧто ответишь?", "opts": [("Хорошо!",False),("1-2 поста — качество важнее",True),("Отказываюсь",False)], "ok": "Алгоритмы любят регулярность, не спам. +15!", "fail": "10 постов в день — спам.", "pts": 15},
    {"title": "Уровень 3: Смыслы", "text": "Клиент: 'Напишите: Мы продаём кофе!'\n\nКак улучшить?", "opts": [("Купите наш кофе!",False),("Начни утро с аромата кофе — заряд на день ☕",True),("У нас много сортов",False)], "ok": "Смыслы + эмоции = вовлечение. +20!", "fail": "Сухой текст не цепляет.", "pts": 20},
    {"title": "Уровень 4: Вовлечение", "text": "Что лучше всего вовлекает аудиторию?", "opts": [("Длинные умные посты",False),("Квизы, опросы, игры",True),("Реклама у блогеров",False)], "ok": "Интерактив — король вовлечения. +25!", "fail": "Интерактив эффективнее рекламы.", "pts": 25},
    {"title": "Уровень 5: Финал", "text": "Презентация для инвесторов. Структура?", "opts": [("Много текста",False),("Проблема → Решение → Результат → CTA",True),("Только картинки",False)], "ok": "ПОБЕДА! Problem-Solution-Result — золото. +50!", "fail": "Инвесторы любят чёткую структуру.", "pts": 50},
]

# ===== КВЕСТ МАРИЯ АФОНИНА — ПРОГРЕВЫ И КОНТЕНТ =====
MARI_QUEST = [
    {
        "title": "🔥 Урок 1: Что такое прогрев",
        "text": (
            "По методу Марии Афониной, прогрев — это не реклама.\n\n"
            "Прогрев — это когда аудитория сама хочет купить.\n\n"
            "❓ Что является ГЛАВНОЙ целью прогрева в блоге?"
        ),
        "opts": [
            ("Рассказать о скидке", False),
            ("Создать желание и доверие до старта продаж", True),
            ("Набрать как можно больше подписчиков", False),
        ],
        "ok": "✅ Верно! Прогрев = желание + доверие. Именно это Мария называет 'интуитивным маркетингом'. +10 очков!",
        "fail": "❌ Нет. Прогрев — это не про скидки и не про подписчиков. Это про создание желания купить ещё до открытия продаж.",
        "pts": 10,
    },
    {
        "title": "🔥 Урок 2: Личность в блоге",
        "text": (
            "Мария учит: люди покупают у людей, а не у брендов.\n\n"
            "В блоге нужно раскрывать личность эксперта.\n\n"
            "❓ Что из этого ЛУЧШЕ всего раскрывает личность?"
        ),
        "opts": [
            ("Посты с полезными советами", False),
            ("Честные истории, ценности, жизнь за кулисами", True),
            ("Красивые фото в студии", False),
        ],
        "ok": "✅ Точно! Мария говорит: 'Личность = истории + ценности + жизнь'. Это то, что цепляет. +15 очков!",
        "fail": "❌ Посты с советами — это экспертный контент. А личность раскрывается через честные истории и жизнь за кулисами.",
        "pts": 15,
    },
    {
        "title": "🔥 Урок 3: Типы контента",
        "text": (
            "По Марии Афониной, экспертный контент бывает разных типов.\n\n"
            "Самый мощный тип — это 'Разбор'.\n\n"
            "❓ Почему разбор — король экспертного контента?"
        ),
        "opts": [
            ("Он длинный и подробный", False),
            ("Он показывает мышление эксперта и создаёт доверие через практику", True),
            ("Его легко снять на видео", False),
        ],
        "ok": "✅ Именно! Разбор = мышление в действии. Аудитория видит КАК эксперт думает — это создаёт максимальное доверие. +20 очков!",
        "fail": "❌ Дело не в длине. Разбор силён тем, что показывает мышление эксперта. Люди видят, как он решает задачи.",
        "pts": 20,
    },
    {
        "title": "🔥 Урок 4: Сторителлинг",
        "text": (
            "Мария: 'Истории продают лучше любой рекламы.'\n\n"
            "Хорошая история для прогрева состоит из элементов.\n\n"
            "❓ Что ОБЯЗАТЕЛЬНО должно быть в продающей истории?"
        ),
        "opts": [
            ("Красивое начало и хэппи-энд", False),
            ("Проблема → Путь → Трансформация → Вывод", True),
            ("Как можно больше деталей", False),
        ],
        "ok": "✅ Браво! Структура: Проблема → Путь → Трансформация → Вывод. Это классический сторителлинг от Марии. +25 очков!",
        "fail": "❌ Красивость не важна. Важна структура: Проблема → Путь → Трансформация → Вывод. Именно она цепляет и продаёт.",
        "pts": 25,
    },
    {
        "title": "🏆 Урок 5: Прогрев через боли",
        "text": (
            "Финальный урок! Мария учит прогревать через боли аудитории.\n\n"
            "Самый мощный инструмент прогрева — это когда человек\nузнаёт себя в твоём контенте.\n\n"
            "❓ Как правильно работать с болями в контенте?"
        ),
        "opts": [
            ("Говорить: 'У вас проблемы? Купите наш курс!'", False),
            ("Описать боль так точно, что человек думает 'это про меня' — и показать путь", True),
            ("Игнорировать боли, говорить только о плюсах", False),
        ],
        "ok": "🏆 ПОБЕДА! Ты прошла квест Марии Афониной!\n\nЗолотое правило: опиши боль точнее самого человека — и он уже наполовину твой клиент. +50 очков!",
        "fail": "❌ Прямые продажи через боль — это грубо. Нужно описать боль с эмпатией и показать путь к решению.",
        "pts": 50,
    },
]

# ===== КВИЗЫ =====
QUIZZES = {
    "smm_q": {"title": "📱 SMM-специализация", "qs": [
        {"q": "Что такое ERR?", "opts": ["Engagement Rate by Reach","Error Rate Report","Email Response Rate"], "a": 0, "exp": "ERR — вовлечённость по охвату."},
        {"q": "Лучший формат для органического охвата?", "opts": ["Статичные посты","Reels/Shorts","Stories"], "a": 1, "exp": "Короткие видео дают максимальный охват."},
        {"q": "Как часто публиковать сторис?", "opts": ["Раз в неделю","Каждый день","Раз в месяц"], "a": 1, "exp": "Ежедневные сторис поддерживают связь."},
    ]},
    "strategy_q": {"title": "📊 Контент-стратегия", "qs": [
        {"q": "Что такое TOV?", "opts": ["Тип визуала","Голос бренда","Вид рекламы"], "a": 1, "exp": "TOV — как бренд общается."},
        {"q": "Оптимальный контент-микс?", "opts": ["100% продажи","50/50","70% польза/20% жизнь/10% продажи"], "a": 2, "exp": "70/20/10 — золотой стандарт."},
        {"q": "Контент-воронка?", "opts": ["Слив контента","Путь от знакомства до покупки","Список тем"], "a": 1, "exp": "Воронка ведёт к покупке."},
    ]},
    "quiz_q": {"title": "🧩 Создание квизов", "qs": [
        {"q": "Зачем квизы в маркетинге?", "opts": ["Развлечение","Вовлечение+лиды","Замена рекламы"], "a": 1, "exp": "Квизы вовлекают и собирают лиды."},
        {"q": "Сколько вопросов оптимально?", "opts": ["2-3","5-10","20+"], "a": 1, "exp": "5-10 — оптимально."},
        {"q": "Что в конце квиза?", "opts": ["Результат","Результат+CTA","Реклама"], "a": 1, "exp": "CTA превращает вовлечение в действие."},
    ]},
    "smysl_q": {"title": "💡 Работа со смыслами", "qs": [
        {"q": "Смысловой маркетинг?", "opts": ["Реклама через ценности","Маркетинг без слов","Таргет"], "a": 0, "exp": "Смыслы — идеи через ценности."},
        {"q": "Лучший триггер в тексте?", "opts": ["Скидка","FOMO (страх упустить)","Список преимуществ"], "a": 1, "exp": "FOMO — мощнейший триггер."},
        {"q": "Боль клиента?", "opts": ["Физическая боль","Нерешённая проблема","Жалоба"], "a": 1, "exp": "Боль — нерешённая проблема."},
    ]},
    "progrev_q": {"title": "🔥 Прогревы (метод Марии Афониной)", "qs": [
        {"q": "Что такое прогрев по Марии Афониной?", "opts": ["Серия рекламных постов","Создание желания и доверия ДО продаж","Марафон в блоге"], "a": 1, "exp": "Прогрев — это не реклама. Это создание желания и доверия заранее."},
        {"q": "Что Мария называет 'королём экспертного контента'?", "opts": ["Лайфстайл-посты","Разбор кейсов","Карусели с советами"], "a": 1, "exp": "Разбор показывает мышление эксперта и создаёт максимальное доверие."},
        {"q": "Структура продающей истории по Марии?", "opts": ["Завязка + Кульминация + Конец","Проблема → Путь → Трансформация → Вывод","Факт + Мнение + Призыв"], "a": 1, "exp": "Проблема → Путь → Трансформация → Вывод — классика сторителлинга."},
        {"q": "Что значит 'прогревать через боли'?", "opts": ["Пугать аудиторию проблемами","Описать боль так точно, что человек узнаёт себя","Перечислять недостатки конкурентов"], "a": 1, "exp": "Точное описание боли создаёт ощущение 'это про меня' — и человек тянется к решению."},
        {"q": "Что такое 'интуитивный маркетинг' по Марии?", "opts": ["Реклама без стратегии","Прогрев без явных продаж через жизнь и ценности","Таргет на интуицию"], "a": 1, "exp": "Интуитивный маркетинг — когда люди хотят купить, не понимая почему. Это высший уровень прогрева."},
    ]},
    "storytelling_q": {"title": "📖 Сторителлинг", "qs": [
        {"q": "Зачем истории в контенте?", "opts": ["Чтобы пост был длиннее","Истории вовлекают и запоминаются лучше фактов","Чтобы показать опыт"], "a": 1, "exp": "Мозг запоминает истории в 22 раза лучше, чем сухие факты."},
        {"q": "Что цепляет в истории больше всего?", "opts": ["Красивые слова","Конфликт и трансформация героя","Подробные детали"], "a": 1, "exp": "Конфликт + трансформация = эмоциональный крючок. Без этого история плоская."},
        {"q": "Как использовать ошибки в прогреве?", "opts": ["Никак, это вредит репутации","Рассказывать об ошибках и чему они научили","Только чужие ошибки"], "a": 1, "exp": "Свои ошибки + урок = доверие. Мария учит: честность продаёт лучше идеальности."},
    ]},
    "visual_q": {"title": "🎨 Визуал и личность в блоге", "qs": [
        {"q": "Зачем раскрывать личность через визуал?", "opts": ["Чтобы было красиво","Люди покупают у людей, а не у безликих брендов","Для охвата"], "a": 1, "exp": "Личный бренд = доверие. Когда видят человека — покупают легче."},
        {"q": "Что главное в визуальном стиле блога?", "opts": ["Как можно больше цветов","Единый стиль, который отражает личность и нишу","Профессиональная съёмка"], "a": 1, "exp": "Единый стиль создаёт узнаваемость. Аудитория должна с первого взгляда понять — чей это аккаунт."},
        {"q": "Как правильно раскрывать личность в контенте?", "opts": ["Публиковать только достижения","Показывать жизнь, ценности, процесс и честные моменты","Делать только экспертные посты"], "a": 1, "exp": "Жизнь + ценности + процесс + честность = живой блог, которому доверяют."},
    ]},
}

# ===== ХЭНДЛЕРЫ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("📅 Контент-план", callback_data="cp_menu")],
        [InlineKeyboardButton("🎮 Квест по SMM", callback_data="quest_start")],
        [InlineKeyboardButton("🔥 Школа Марии Афониной", callback_data="mari_menu")],
        [InlineKeyboardButton("📝 Квизы", callback_data="quiz_menu")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
    ]
    text = (
        "👋 Привет! Я *Марьяша* — твой наставник по SMM!\n\n"
        "🎯 SMM · 📊 Стратегия · 🖼️ Презентации\n"
        "🧩 Квизы · 💡 Смыслы · 🔥 Прогревы\n\n"
        "✨ *Новое:* Школа Марии Афониной — прогревы, сторителлинг, визуал!\n\n"
        "Выбери с чего начнём:"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def cp_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("📱 SMM-специалист", callback_data="cp_smm")],
        [InlineKeyboardButton("📊 Контент-стратег", callback_data="cp_strategy")],
        [InlineKeyboardButton("🖼️ Презентации", callback_data="cp_prezentation")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")],
    ]
    await q.message.edit_text("📅 *Контент-план*\n\nВыбери специализацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def cp_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    key = q.data.replace("cp_",""); plan = CONTENT_PLAN.get(key,[])
    names = {"smm":"📱 SMM-специалист","strategy":"📊 Контент-стратег","prezentation":"🖼️ Презентации"}
    await q.message.edit_text(f"📅 *{names[key]} — 7 дней:*\n\n" + "\n\n".join(f"✅ {d}" for d in plan), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад",callback_data="cp_menu")]]), parse_mode="Markdown")

async def quest_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    context.user_data.update({"ql":0,"qs":0}); await quest_show(q,context)

async def quest_show(q, context):
    idx = context.user_data.get("ql",0)
    if idx >= len(QUEST):
        await q.message.edit_text(f"🏆 Квест пройден!\n\n⭐ *{context.user_data.get('qs',0)} очков*\n\nТы SMM-профи!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню",callback_data="back")]]), parse_mode="Markdown"); return
    level = QUEST[idx]; kb = [[InlineKeyboardButton(f"{chr(65+i)}) {t}",callback_data=f"qa_{i}")] for i,(t,_) in enumerate(level["opts"])]; kb.append([InlineKeyboardButton("🏠 Выйти",callback_data="back")])
    await q.message.edit_text(f"🗺️ *{level['title']}* | ⭐{context.user_data.get('qs',0)}\n\n{level['text']}", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quest_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    idx = context.user_data.get("ql",0); ans = int(q.data.replace("qa_","")); level = QUEST[idx]; _,correct = level["opts"][ans]
    context.user_data["qs"] = context.user_data.get("qs",0) + (level["pts"] if correct else 0)
    context.user_data["ql"] = idx+1
    await q.message.edit_text(f"{'✅' if correct else '❌'} {level['ok'] if correct else level['fail']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Далее",callback_data="quest_next")]]))

async def quest_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); await quest_show(q,context)

# ===== ШКОЛА МАРИИ =====
async def mari_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("🎮 Квест: Прогревы по Марии", callback_data="mari_quest_start")],
        [InlineKeyboardButton("🔥 Квиз: Прогревы", callback_data="qz_progrev_q")],
        [InlineKeyboardButton("📖 Квиз: Сторителлинг", callback_data="qz_storytelling_q")],
        [InlineKeyboardButton("🎨 Квиз: Визуал и личность", callback_data="qz_visual_q")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")],
    ]
    await q.message.edit_text(
        "🔥 *Школа Марии Афониной*\n\n"
        "Мария — эксперт по запускам и прогревам.\n"
        "Здесь собраны её ключевые идеи по SMM:\n\n"
        "🎮 Квест из 5 уровней по прогревам\n"
        "📝 Квизы: прогревы, сторителлинг, визуал\n\n"
        "Выбери формат:",
        reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown"
    )

async def mari_quest_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    context.user_data.update({"mql":0,"mqs":0}); await mari_quest_show(q,context)

async def mari_quest_show(q, context):
    idx = context.user_data.get("mql",0)
    if idx >= len(MARI_QUEST):
        score = context.user_data.get("mqs",0)
        e = "🏆" if score >= 100 else "🥈" if score >= 60 else "📚"
        await q.message.edit_text(
            f"{e} *Квест Марии пройден!*\n\n"
            f"⭐ Твой счёт: *{score} из 120 очков*\n\n"
            f"{'Ты настоящий мастер прогревов!' if score >= 100 else 'Хорошо! Повтори квизы для закрепления.'}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 В меню Марии",callback_data="mari_menu")],[InlineKeyboardButton("🏠 Главное меню",callback_data="back")]]),
            parse_mode="Markdown"
        ); return
    level = MARI_QUEST[idx]
    kb = [[InlineKeyboardButton(f"{chr(65+i)}) {t}",callback_data=f"mqa_{i}")] for i,(t,_) in enumerate(level["opts"])]
    kb.append([InlineKeyboardButton("🏠 Выйти",callback_data="back")])
    await q.message.edit_text(
        f"🔥 *{level['title']}* | ⭐{context.user_data.get('mqs',0)} очков\n\n{level['text']}",
        reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown"
    )

async def mari_quest_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    idx = context.user_data.get("mql",0); ans = int(q.data.replace("mqa_","")); level = MARI_QUEST[idx]; _,correct = level["opts"][ans]
    context.user_data["mqs"] = context.user_data.get("mqs",0) + (level["pts"] if correct else 0)
    context.user_data["mql"] = idx+1
    await q.message.edit_text(level["ok"] if correct else level["fail"], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Следующий урок",callback_data="mquest_next")]]), parse_mode="Markdown")

async def mari_quest_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); await mari_quest_show(q,context)

# ===== КВИЗЫ =====
async def quiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [
        [InlineKeyboardButton("📱 SMM",callback_data="qz_smm_q")],
        [InlineKeyboardButton("📊 Контент-стратегия",callback_data="qz_strategy_q")],
        [InlineKeyboardButton("🧩 Создание квизов",callback_data="qz_quiz_q")],
        [InlineKeyboardButton("💡 Смыслы",callback_data="qz_smysl_q")],
        [InlineKeyboardButton("🔥 Прогревы (Мария Афонина)",callback_data="qz_progrev_q")],
        [InlineKeyboardButton("📖 Сторителлинг",callback_data="qz_storytelling_q")],
        [InlineKeyboardButton("🎨 Визуал и личность",callback_data="qz_visual_q")],
        [InlineKeyboardButton("🔙 Назад",callback_data="back")],
    ]
    await q.message.edit_text("📝 *Квизы*\n\nВыбери тему:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    key = q.data.replace("qz_",""); context.user_data.update({"qkey":key,"qi":0,"qscore":0}); await quiz_show(q,context)

async def quiz_show(q, context):
    key = context.user_data["qkey"]; qi = context.user_data.get("qi",0); quiz = QUIZZES[key]
    if qi >= len(quiz["qs"]):
        s=context.user_data.get("qscore",0); t=len(quiz["qs"]); e="🏆" if s==t else "👍" if s>=t//2 else "📚"
        await q.message.edit_text(f"{e} Квиз завершён!\n\n✅ {s}/{t} правильных", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Ещё раз",callback_data=f"qz_{key}")],[InlineKeyboardButton("📝 Другой квиз",callback_data="quiz_menu")],[InlineKeyboardButton("🏠 Меню",callback_data="back")]])); return
    question = quiz["qs"][qi]; kb = [[InlineKeyboardButton(f"{chr(65+i)}) {o}",callback_data=f"qza_{i}")] for i,o in enumerate(question["opts"])]
    await q.message.edit_text(f"📝 *{quiz['title']}*\nВопрос {qi+1}/{len(quiz['qs'])}\n\n❓ {question['q']}", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quiz_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    ans=int(q.data.replace("qza_","")); key=context.user_data["qkey"]; qi=context.user_data.get("qi",0); question=QUIZZES[key]["qs"][qi]
    if ans==question["a"]:
        context.user_data["qscore"]=context.user_data.get("qscore",0)+1; fb=f"✅ Верно!\n\n💡 {question['exp']}"
    else:
        fb=f"❌ Неверно. Правильно: *{question['opts'][question['a']]}*\n\n💡 {question['exp']}"
    context.user_data["qi"]=qi+1
    await q.message.edit_text(fb, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Далее",callback_data="qz_next")]]), parse_mode="Markdown")

async def quiz_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); await quiz_show(q,context)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.message.edit_text(
        "ℹ️ *Марьяша — SMM-бот*\n\n"
        "📅 Контент-планы по специализациям\n"
        "🎮 Квест-игра по SMM (5 уровней)\n"
        "🔥 Школа Марии Афониной:\n"
        "   • Квест по прогревам (5 уроков)\n"
        "   • Квизы: прогревы, сторителлинг, визуал\n"
        "📝 Квизы по 7 темам с объяснениями\n\n"
        "Темы: SMM · Стратегия · Смыслы · Квизы\nПрогревы · Сторителлинг · Визуал",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню",callback_data="back")]]),
        parse_mode="Markdown"
    )

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cp_menu, pattern="^cp_menu$"))
    app.add_handler(CallbackQueryHandler(cp_show, pattern="^cp_(smm|strategy|prezentation)$"))
    app.add_handler(CallbackQueryHandler(quest_start, pattern="^quest_start$"))
    app.add_handler(CallbackQueryHandler(quest_ans, pattern="^qa_"))
    app.add_handler(CallbackQueryHandler(quest_next, pattern="^quest_next$"))
    app.add_handler(CallbackQueryHandler(mari_menu, pattern="^mari_menu$"))
    app.add_handler(CallbackQueryHandler(mari_quest_start, pattern="^mari_quest_start$"))
    app.add_handler(CallbackQueryHandler(mari_quest_ans, pattern="^mqa_"))
    app.add_handler(CallbackQueryHandler(mari_quest_next, pattern="^mquest_next$"))
    app.add_handler(CallbackQueryHandler(quiz_menu, pattern="^quiz_menu$"))
    app.add_handler(CallbackQueryHandler(quiz_start, pattern="^qz_(?!next)"))
    app.add_handler(CallbackQueryHandler(quiz_ans, pattern="^qza_"))
    app.add_handler(CallbackQueryHandler(quiz_next, pattern="^qz_next$"))
    app.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.run_polling()

if __name__ == "__main__":
    main()
