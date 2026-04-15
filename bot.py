import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

CONTENT_PLAN = {
    "smm": ["День 1: Анализ ЦА", "День 2: Конкурентный анализ", "День 3: Рубрики 70/20/10", "День 4: Продающий пост", "День 5: Reels-сценарий", "День 6: Карусель", "День 7: Анализ статистики"],
    "strategy": ["День 1: TOV бренда", "День 2: Стратегия на месяц", "День 3: Лендинг-текст", "День 4: Email-рассылка", "День 5: Сторителлинг", "День 6: UGC-контент", "День 7: Анализ"],
    "prezentation": ["День 1: Структура по Кавасаки", "День 2: Визуал (цвета, шрифты)", "День 3: Тексты слайдов", "День 4: Инфографика", "День 5: CTA и триггеры", "День 6: Тест-прогон", "День 7: Финальная версия"],
}
QUEST = [
    {"title": "Уровень 1", "text": "Кафе хочет клиентов. Что первым?", "opts": [("Постить фото",False),("Анализ ЦА",True),("Больше бюджета",False)], "ok": "Верно! +10", "fail": "Нет, анализ ЦА первичен.", "pts": 10},
    {"title": "Уровень 2", "text": "Клиент хочет 10 постов/день!", "opts": [("Ок!",False),("1-2 поста — качество важнее",True),("Отказываюсь",False)], "ok": "Правильно! +15", "fail": "10 постов — спам.", "pts": 15},
    {"title": "Уровень 3", "text": "Улучши: 'Мы продаём кофе!'", "opts": [("Купите кофе!",False),("Начни утро с аромата кофе ☕",True),("Много сортов",False)], "ok": "Смыслы+эмоции! +20", "fail": "Сухой текст не цепляет.", "pts": 20},
    {"title": "Уровень 4", "text": "Что лучше вовлекает?", "opts": [("Длинные посты",False),("Квизы и опросы",True),("Блогеры",False)], "ok": "Интерактив — король! +25", "fail": "Интерактив эффективнее.", "pts": 25},
    {"title": "Уровень 5", "text": "Структура презентации для инвесторов?", "opts": [("Много текста",False),("Проблема→Решение→Результат→CTA",True),("Картинки",False)], "ok": "ПОБЕДА! +50", "fail": "Инвесторы любят чёткую структуру.", "pts": 50},
]
QUIZZES = {
    "smm_q": {"title": "SMM", "qs": [
        {"q": "Что такое ERR?", "opts": ["Engagement Rate by Reach","Error Rate Report","Email Response Rate"], "a": 0, "exp": "ERR — вовлечённость по охвату."},
        {"q": "Лучший формат для охвата?", "opts": ["Посты","Reels/Shorts","Stories"], "a": 1, "exp": "Короткие видео дают максимальный охват."},
        {"q": "Как часто сторис?", "opts": ["Раз в неделю","Каждый день","Раз в месяц"], "a": 1, "exp": "Ежедневные сторис поддерживают связь."},
    ]},
    "strategy_q": {"title": "Контент-стратегия", "qs": [
        {"q": "Что такое TOV?", "opts": ["Тип визуала","Голос бренда","Вид рекламы"], "a": 1, "exp": "TOV — как бренд общается."},
        {"q": "Контент-микс?", "opts": ["100% продажи","50/50","70% польза/20% жизнь/10% продажи"], "a": 2, "exp": "70/20/10 — золотой стандарт."},
        {"q": "Контент-воронка?", "opts": ["Слив контента","Путь от знакомства до покупки","Список тем"], "a": 1, "exp": "Воронка ведёт к покупке."},
    ]},
    "quiz_q": {"title": "Квизы", "qs": [
        {"q": "Зачем квизы?", "opts": ["Развлечение","Вовлечение+лиды","Замена рекламы"], "a": 1, "exp": "Квизы вовлекают и собирают лиды."},
        {"q": "Сколько вопросов?", "opts": ["2-3","5-10","20+"], "a": 1, "exp": "5-10 — оптимально."},
        {"q": "Что в конце?", "opts": ["Результат","Результат+CTA","Реклама"], "a": 1, "exp": "CTA превращает вовлечение в действие."},
    ]},
    "smysl_q": {"title": "Смыслы", "qs": [
        {"q": "Смысловой маркетинг?", "opts": ["Реклама через ценности","Маркетинг без слов","Таргет"], "a": 0, "exp": "Смыслы — идеи через ценности."},
        {"q": "Лучший триггер?", "opts": ["Скидка","FOMO","Список преимуществ"], "a": 1, "exp": "FOMO — мощнейший триггер."},
        {"q": "Боль клиента?", "opts": ["Физическая боль","Нерешённая проблема","Жалоба"], "a": 1, "exp": "Боль — нерешённая проблема."},
    ]},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📅 Контент-план", callback_data="cp_menu")],[InlineKeyboardButton("🎮 Квест по SMM", callback_data="quest_start")],[InlineKeyboardButton("📝 Квизы", callback_data="quiz_menu")],[InlineKeyboardButton("ℹ️ О боте", callback_data="about")]]
    text = "👋 Привет! Я *Марьяша* — наставник по SMM!\n\n🎯 SMM · 📊 Стратегия · 🖼️ Презентации · 🧩 Квизы · 💡 Смыслы\n\nВыбери:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def cp_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [[InlineKeyboardButton("📱 SMM",callback_data="cp_smm")],[InlineKeyboardButton("📊 Стратегия",callback_data="cp_strategy")],[InlineKeyboardButton("🖼️ Презентации",callback_data="cp_prezentation")],[InlineKeyboardButton("🔙 Назад",callback_data="back")]]
    await q.message.edit_text("📅 *Контент-план*\n\nВыбери специализацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def cp_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    key = q.data.replace("cp_",""); plan = CONTENT_PLAN.get(key,[])
    names = {"smm":"SMM-специалист","strategy":"Контент-стратег","prezentation":"Презентации"}
    await q.message.edit_text(f"📅 *{names[key]} — 7 дней:*\n\n" + "\n\n".join(f"✅ {d}" for d in plan), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад",callback_data="cp_menu")]]), parse_mode="Markdown")

async def quest_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    context.user_data.update({"ql":0,"qs":0}); await quest_show(q,context)

async def quest_show(q, context):
    idx = context.user_data.get("ql",0)
    if idx >= len(QUEST):
        await q.message.edit_text(f"🏆 Квест пройден! ⭐ *{context.user_data.get('qs',0)} очков*\n\nТы SMM-профи!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню",callback_data="back")]]), parse_mode="Markdown"); return
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

async def quiz_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    kb = [[InlineKeyboardButton("📱 SMM",callback_data="qz_smm_q")],[InlineKeyboardButton("📊 Стратегия",callback_data="qz_strategy_q")],[InlineKeyboardButton("🧩 Квизы",callback_data="qz_quiz_q")],[InlineKeyboardButton("💡 Смыслы",callback_data="qz_smysl_q")],[InlineKeyboardButton("🔙 Назад",callback_data="back")]]
    await q.message.edit_text("📝 *Квизы*\n\nВыбери тему:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    key = q.data.replace("qz_",""); context.user_data.update({"qkey":key,"qi":0,"qscore":0}); await quiz_show(q,context)

async def quiz_show(q, context):
    key = context.user_data["qkey"]; qi = context.user_data.get("qi",0); quiz = QUIZZES[key]
    if qi >= len(quiz["qs"]):
        s=context.user_data.get("qscore",0); t=len(quiz["qs"]); e="🏆" if s==t else "👍" if s>=t//2 else "📚"
        await q.message.edit_text(f"{e} Квиз завершён! ✅ {s}/{t}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Ещё раз",callback_data=f"qz_{key}")],[InlineKeyboardButton("📝 Другой",callback_data="quiz_menu")],[InlineKeyboardButton("🏠 Меню",callback_data="back")]])); return
    question = quiz["qs"][qi]; kb = [[InlineKeyboardButton(f"{chr(65+i)}) {o}",callback_data=f"qza_{i}")] for i,o in enumerate(question["opts"])]
    await q.message.edit_text(f"📝 *{quiz['title']}* — {qi+1}/{len(quiz['qs'])}\n\n❓ {question['q']}", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def quiz_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    ans=int(q.data.replace("qza_","")); key=context.user_data["qkey"]; qi=context.user_data.get("qi",0); question=QUIZZES[key]["qs"][qi]
    if ans==question["a"]:
        context.user_data["qscore"]=context.user_data.get("qscore",0)+1; fb=f"✅ Верно! 💡 {question['exp']}"
    else:
        fb=f"❌ Правильно: *{question['opts'][question['a']]}* 💡 {question['exp']}"
    context.user_data["qi"]=qi+1
    await q.message.edit_text(fb, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Далее",callback_data="qz_next")]]), parse_mode="Markdown")

async def quiz_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); await quiz_show(q,context)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.message.edit_text("ℹ️ *Марьяша — SMM-бот*\n\n📅 Контент-планы\n🎮 Квест-игра\n📝 Квизы: SMM, Стратегия, Квизы, Смыслы", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню",callback_data="back")]]), parse_mode="Markdown")

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
    app.add_handler(CallbackQueryHandler(quiz_menu, pattern="^quiz_menu$"))
    app.add_handler(CallbackQueryHandler(quiz_start, pattern="^qz_(?!next)"))
    app.add_handler(CallbackQueryHandler(quiz_ans, pattern="^qza_"))
    app.add_handler(CallbackQueryHandler(quiz_next, pattern="^qz_next$"))
    app.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.run_polling()

if __name__ == "__main__":
    main()
