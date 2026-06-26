import telebot
from telebot import types
from flask import Flask
from threading import Thread
import psycopg2

app = Flask('')

@app.route('/')
def home():
    return "ቦቱ በሰላም እየሰራ ነው!"

def run():
    app.run(host='0.0.0.0', port=8080)

# የቦት ቶከን
API_TOKEN = '8985196897:AAHId61d1nfnzaYF761k1SNpJon1ybhkdCY'
bot = telebot.TeleBot(API_TOKEN)

# ያመጣኸው የዳታቤዝ ሊንክ
DB_URL = "DB_URL = "postgres://melbet_dp_user:4Y8Oc5WWy9FOB6bh8XrMFVYOFxi6Dmj5@dpg-d8v52jmq1p3s73bfg1cg-a.oregon-postgres.render.com/melbet_dp"
"

# ዳታቤዝ ውስጥ ሰንጠረዥ (Table) መፍጠሪያ
def init_db():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            balance REAl DEFAULT 0.0
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# አዲስ ተጠቃሚ መመዝገቢያ
def register_user(user_id, username):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, username, balance) VALUES (%s, %s, %s)", (user_id, username, 0.0))
        conn.commit()
    cursor.close()
    conn.close()

# የቀሪ ሂሳብ ማያያዣ
def get_balance(user_id):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res[0] if res else 0.0

# የዋናው ማውጫ ቁልፎች (Play ጨምሮ)
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_play = types.InlineKeyboardButton("🎰 አሁኑኑ ይጫወቱ (Play)", callback_data="play_game")
    btn_balance = types.InlineKeyboardButton("💸 ቀሪ ሂሳብ (Balance)", callback_data="check_balance")
    btn_deposit = types.InlineKeyboardButton("📥 ብር ያስገቡ (Deposit)", callback_data="deposit")
    btn_withdraw = types.InlineKeyboardButton("📤 ብር ያውጡ (Withdraw)", callback_data="withdraw")
    
    markup.add(btn_play)
    markup.add(btn_balance, btn_deposit)
    markup.add(btn_withdraw)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "ተጠቃሚ"
    
    # ተጠቃሚውን ዳታቤዝ ውስጥ መመዝገብ
    register_user(user_id, username)
    
    welcome_text = (
        f"እንኳን ወደ  Melbet በደህና መጡ! 🎰\n\n"
        f"👋 ሰላም {username}፣ አካውንትዎ በነፃ ተከፍቷል።\n"
        f"እዚህ በቀላሉ የቢንጎ፣ የሩሌት እና የቁማር ጨዋታዎችን መጫወት ይችላሉ።\n\n"
        f"ለመጀመር ከታች ያለውን 'Play' ወይም የሚፈልጉትን አማራጭ ይጫኑ፦"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# የቁልፎቹ ስራዎች
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    
    if call.data == "play_game":
        bot.answer_callback_query(call.id)
        # እዚህ ጋር ለወደፊቱ የዌብ አፕ (Web App) ሊንክ ወይም የጨዋታ ምርጫዎችን ማውጣት ይቻላል
        bot.send_message(call.message.chat.id, "🎰 የቢንጎ እና የስሎት ጨዋታዎች ማውጫ በመዘጋጀት ላይ ነው... በቅርቡ JILI ጨዋታዎች ይገባሉ!")
        
    elif call.data == "check_balance":
        bot.answer_callback_query(call.id)
        bal = get_balance(user_id)
        bot.send_message(call.message.chat.id, f"💸 የእርስዎ የአሁኑ ቀሪ ሂሳብ: {bal:.2f} ብር ነው።")
        
    elif call.data == "deposit":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📥 ብር ለማስገባት እና አካውንቶን ለመሙላት እባክዎ የባንክ ሂሳብ ወይም የቴሌብር ቁጥር ከአስተዳዳሪው ይጠይቁ።")
        
    elif call.data == "withdraw":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📤 ብር ለማውጣት አነስተኛው መጠን 100 ብር ነው። በአሁኑ ሰዓት በቂ ቀሪ ሂሳብ የሎትም።")

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    init_db() # ዳታቤዙን መጀመሪያ ማስነሳት
    keep_alive()
    print("ቦቱ መስራት ጀምሯል...")
    bot.polling(none_stop=True)
