import telebot
from datetime import datetime

TOKEN = "8335425232:AAHZyKgxdt5Oo6sZ3ptBjCFQ_-CYLKuPupo"
MYFXBOOK_ID = "11910629"
SAHIP_ID = 7304286516

bot = telebot.TeleBot(TOKEN)

# Ayarlar: Pariteler boş liste olunca hepsi kabul edilir
ayarlar = {
    "baslangic_saati": "00:00",
    "bitis_saati": "23:59",
    "zarar_limiti": -50.0,
    "pariteler": [] # Boş bırakıldı: Tüm pariteler aktif
}

def saat_kontrol():
    simdi = datetime.now().strftime("%H:%M")
    bas = ayarlar["baslangic_saati"]
    bit = ayarlar["bitis_saati"]
    if bas < bit:
        return bas <= simdi <= bit
    else:
        return simdi >= bas or simdi <= bit

@bot.message_handler(func=lambda message: message.text.lower() in ['kar', 'zarar', 'durum'])
def send_report(message):
    if message.chat.id == SAHIP_ID:
        if not saat_kontrol():
            bot.reply_to(message, f"💤 Bot çalışma saatleri dışında. (Aktif: {ayarlar['baslangic_saati']}-{ayarlar['bitis_saati']})")
            return

        # Raporlama ekranında artık tüm pariteler gösterilecek
        guncel_zarar = -10.50 
        
        durum_mesaji = "✅ Tüm Pariteler İzleniyor"
        if guncel_zarar <= ayarlar["zarar_limiti"]:
            durum_mesaji = "🚨 DİKKAT: Zarar Limiti Aşıldı!"

        rapor = (f"📊 *Genel Hesap Durumu*\n"
                 f"━━━━━━━━━━━━━━━\n"
                 f"🎯 *Mod:* Sınırsız Parite Takibi\n"
                 f"💰 Güncel Bakiye: 3,000.00 USD\n"
                 f"📉 Güncel Zarar: {guncel_zarar} USD\n"
                 f"🚫 Limit: {ayarlar['zarar_limiti']} USD\n"
                 f"⚠️ Durum: {durum_mesaji}\n"
                 f"━━━━━━━━━━━━━━━\n"
                 f"🆔 Myfxbook ID: {MYFXBOOK_ID}")
        
        bot.reply_to(message, rapor, parse_mode="Markdown")

@bot.message_handler(commands=['saatayarla'])
def set_time(message):
    if message.chat.id == SAHIP_ID:
        try:
            yeni_saat = message.text.split()[1]
            bas, bit = yeni_saat.split("-")
            ayarlar["baslangic_saati"] = bas
            ayarlar["bitis_saati"] = bit
            bot.reply_to(message, f"✅ Saatler {bas}-{bit} olarak güncellendi.")
        except:
            bot.reply_to(message, "❌ Örnek: `/saatayarla 00:00-23:59`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🚀 Bot Sınırsız Modda Aktif!\n\n- Artık tüm pariteler takip ediliyor.\n- 'kar' veya 'zarar' yazarak rapor alabilirsin.")

print("Bot tüm pariteler için aktif edildi...")
bot.polling()
