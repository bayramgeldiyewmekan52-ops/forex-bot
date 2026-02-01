import telebot

TOKEN = "8335425232:AAHZyKgxdt5Oo6sZ3ptBjCFQ_-CYLKuPupo"
MYFXBOOK_ID = "11910629"
SAHIP_ID = 7304286516 

bot = telebot.TeleBot(TOKEN)

# Sadece 'kar' yazıldığında tetiklenir (büyük/küçük harf duyarsız)
@bot.message_handler(func=lambda message: message.text.lower() == 'kar')
def get_profit(message):
    if message.chat.id == SAHIP_ID:
        rapor = (f"📊 *Hesap Özeti (Demo)*\n\n"
                 f"💰 Güncel Bakiye: 3,000.00 USD\n"
                 f"📈 Toplam Kâr: +0.00%\n"
                 f"🆔 Sistem ID: {MYFXBOOK_ID}\n\n"
                 f"🔗 [Detaylı Rapor İçin Tıkla](https://www.myfxbook.com/members/sistem/{MYFXBOOK_ID})")
        bot.reply_to(message, rapor, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ Bot hazır! Artık sadece 'kar' yazarak rapor alabilirsin.")

print("Bot aktif... Telegram'dan 'kar' yazabilirsin.")
bot.polling()

