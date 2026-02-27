import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# API KEYS
BOT_TOKEN  =  os.getenv("BOT_TOKEN")
OPENAI_API_KEY=  os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


# User session storage
user_sessions = {}

# ================= AI FUNCTION =================
def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional IELTS examiner."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🎤 IELTS Speaking"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome!\nChoose an option:",
        reply_markup=reply_markup,
    )


# ================= SPEAKING START =================
async def start_speaking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    user_sessions[user_id] = {
        "part": 1,
        "part1_questions": [],
        "part3_questions": [],
        "index": 0,
        "cue_topic": ""
    }

    prompt = "Generate 6 different IELTS Speaking Part 1 questions. Only questions."
    questions = ask_ai(prompt).split("\n")

    user_sessions[user_id]["part1_questions"] = [
        q for q in questions if q.strip() != ""
    ]

    await update.message.reply_text(
        "🎤 Part 1\n\n" + user_sessions[user_id]["part1_questions"][0]
    )


# ================= MESSAGE HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "🎤 IELTS Speaking":
        await start_speaking(update, context)
        return

    if user_id not in user_sessions:
        return

    session = user_sessions[user_id]

    # -------- PART 1 --------
    if session["part"] == 1:
        session["index"] += 1

        if session["index"] < len(session["part1_questions"]):
            next_q = session["part1_questions"][session["index"]]
            await update.message.reply_text(next_q)
        else:
            session["part"] = 2
            session["index"] = 0

            cue = ask_ai(
                "Generate one IELTS Speaking Part 2 cue card with bullet points."
            )

            session["cue_topic"] = cue

            await update.message.reply_text(
                "🎤 Part 2\n\n" + cue + "\n\nYou have 2 minutes. Start speaking."
            )

    # -------- PART 2 --------
    elif session["part"] == 2:
        session["part"] = 3
        session["index"] = 0

        prompt = f"""
        Based on this Part 2 topic:
        {session['cue_topic']}

        Generate 5 IELTS Speaking Part 3 discussion questions.
        Only questions.
        """

        part3 = ask_ai(prompt).split("\n")

        session["part3_questions"] = [
            q for q in part3 if q.strip() != ""
        ]

        await update.message.reply_text(
            "🎤 Part 3\n\n" + session["part3_questions"][0]
        )

    # -------- PART 3 --------
    elif session["part"] == 3:
        session["index"] += 1

        if session["index"] < len(session["part3_questions"]):
            next_q = session["part3_questions"][session["index"]]
            await update.message.reply_text(next_q)
        else:
            await update.message.reply_text(
                "✅ Speaking test finished! Great job!"
            )
            del user_sessions[user_id]


# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()







