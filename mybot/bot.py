from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import os

TOKEN = os.getenv("BOT_TOKEN")

# Foydalanuvchi tanlagan tilni saqlaymiz
user_language = {}

# Matnlar bazasi
texts = {
    "uz": {
        "welcome": "Tilni tanlang:",
        "menu": "Kerakli bo‘limni tanlang:",
        "speaking": "🗣 Speaking Mock",
        "course": "📚 Mini Course",
        "channel": "📢 Kanal",
        "course_text": "Mini IELTS course tez kunda qo‘shiladi 📚",
        "channel_text": "Bizning kanalga qo‘shiling: @yourchannel"
    },
    "en": {
        "welcome": "Please choose your language:",
        "menu": "Select a section:",
        "speaking": "🗣 Speaking Mock",
        "course": "📚 Mini Course",
        "channel": "📢 Channel",
        "course_text": "Mini IELTS course coming soon 📚",
        "channel_text": "Join our channel: @yourchannel"
    },
    "ru": {
        "welcome": "Выберите язык:",
        "menu": "Выберите раздел:",
        "speaking": "🗣 Speaking Mock",
        "course": "📚 Мини курс",
        "channel": "📢 Канал",
        "course_text": "Мини курс скоро будет 📚",
        "channel_text": "Подписывайтесь на канал: @yourchannel"
    },
    "tr": {
        "welcome": "Lütfen dil seçin:",
        "menu": "Bir bölüm seçin:",
        "speaking": "🗣 Speaking Mock",
        "course": "📚 Mini Kurs",
        "channel": "📢 Kanal",
        "course_text": "Mini IELTS kursu yakında 📚",
        "channel_text": "Kanalımıza katılın: @yourchannel"
    },
    "ar": {
        "welcome": "اختر اللغة:",
        "menu": "اختر القسم:",
        "speaking": "🗣 Speaking Mock",
        "course": "📚 دورة مصغرة",
        "channel": "📢 القناة",
        "course_text": "الدورة قريباً 📚",
        "channel_text": "انضم إلى قناتنا: @yourchannel"
    }
}

speaking_questions = [
    "Describe your hometown.",
    "What do you do in your free time?",
    "Describe a person who inspires you.",
    "Do you like reading books? Why?",
    "What is your favorite subject?"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🇺🇿 Uzbek", "🇬🇧 English"],
        ["🇷🇺 Russian", "🇹🇷 Turkish"],
        ["🇸🇦 Arabic"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🌍 Please choose your language:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "🇺🇿 Uzbek":
        user_language[user_id] = "uz"
    elif text == "🇬🇧 English":
        user_language[user_id] = "en"
    elif text == "🇷🇺 Russian":
        user_language[user_id] = "ru"
    elif text == "🇹🇷 Turkish":
        user_language[user_id] = "tr"
    elif text == "🇸🇦 Arabic":
        user_language[user_id] = "ar"

    if user_id in user_language:
        lang = user_language[user_id]
        keyboard = [
            [texts[lang]["speaking"]],
            [texts[lang]["course"], texts[lang]["channel"]]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        if text in ["🇺🇿 Uzbek","🇬🇧 English","🇷🇺 Russian","🇹🇷 Turkish","🇸🇦 Arabic"]:
            await update.message.reply_text(texts[lang]["menu"], reply_markup=reply_markup)
            return

        if text == texts[lang]["speaking"]:
            question = random.choice(speaking_questions)
            await update.message.reply_text(question)

        elif text == texts[lang]["course"]:
            await update.message.reply_text(texts[lang]["course_text"])

        elif text == texts[lang]["channel"]:
            await update.message.reply_text(texts[lang]["channel_text"])

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
