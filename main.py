import telebot
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "ቦቱ በሰላም እየሰራ ነው!"

def run():
    app.run(host='0.0.0.0', port=8080)

API_TOKEN = '8985196897:AAHId61d1nfnzaYF761k1SNpJon1ybhkdCY'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "እንኳን ወደ MELBET በደህና መጡ! 🎰")

@bot.message_handler(commands=['check_balance'])
def check_balance(message):
    bot.reply_to(message, "💸 የእርስዎ የአሁኑ ቀሪ ሂሳብ: 0.00 ብር ነው።")

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("ቦቱ መስራት ጀምሯል...")
    bot.polling(none_stop=True)
