import telebot
from datetime import datetime

TOKEN = "8335425232:AAHZyKgxdt5Oo6sZ3ptBjCFQ_-CYLKuPupo"
MYFXBOOK_ID = "11910629"
SAHIP_ID = 7304286516

bot = telebot.TeleBot(TOKEN)

# Varsayılan ayarlar
ayarlar = {
    "baslangic_saati": "22:00",
    "bitis_saati": "09:00",
    "zarar_limiti": -50.0,
    "pariteler": ["XAUUSD", "XAGUSD", "EURUSD"]
}

def saat_kontrol():
    simdi = datetime.now().strftime("%H:%M")
    bas = ayarlar["baslangic_saati"]
    bit = ayarlar["bitis_saati"]
    if bas < bit:
        return bas <= simdi <= bit
    else: # Gece yarısını geçen saatler için (Örn: 22:00 - 09:00)
        return simdi >= bas or simdi <= bit

@bot.message_handler(func=lambda message: message.text.lower() in ['kar', 'zarar'])
def send_report(message):
    if message.chat.id == SAHIP_ID:
        if not saat_kontrol():
            bot.reply_to(message, f"💤 Bot şu an çalışma saatleri dışında. (Aktif: {ayarlar['baslangic_saati']}-{ayarlar['bitis_saati']})")
            return

        # Demo veriler (Gerçek veriler için Myfxbook API bağlanmalıdır)
        guncel_zarar = -10.50 # Örnek zarar
        
        durum_mesaji = "✅ Sistem Normal"
        if guncel_zarar <= ayarlar["zarar_limiti"]:
            durum_mesaji = "🚨 DİKKAT: Günlük Zarar Limiti Aşıldı!"

        rapor = (f"📊 *Hesap Özeti (Demo)*\n"
                 f"━━━━━━━━━━━━━━━\n"
                 f"🎯 *İzlenen:* {', '.join(ayarlar['pariteler'])}\n"
                 f"💰 Bakiye: 3,000.00 USD\n"
                 f"📉 Güncel Zarar: {guncel_zarar} USD\n"
                 f"🚫 Limit: {ayarlar['zarar_limiti']} USD\n"
                 f"⚠️ Durum: {durum_mesaji}\n"
                 f"━━━━━━━━━━━━━━━\n"
                 f"🆔 ID: {MYFXBOOK_ID}")
        
        bot.reply_to(message, rapor, parse_mode="Markdown")

@bot.message_handler(commands=['saatayarla'])
def set_time(message):
    if message.chat.id == SAHIP_ID:
        try:
            # Örnek kullanım: /saatayarla 22:00-09:00
            yeni_saat = message.text.split()[1]
            bas, bit = yeni_saat.split("-")
            ayarlar["baslangic_saati"] = bas
            ayarlar["bitis_saati"] = bit
            bot.reply_to(message, f"✅ Çalışma saatleri {bas} ile {bit} arası olarak güncellendi.")
        except:
            bot.reply_to(message, "❌ Hata! Lütfen şu formatta yazın: `/saatayarla 22:00-09:00`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ Bot güncellendi!\n\n- 'kar' veya 'zarar' yazarak rapor alabilirsin.\n- /saatayarla komutuyla saatleri değiştirebilirsin.\n- Sadece XAUUSD, XAGUSD, EURUSD izleniyor.")

print("Bot yeni özelliklerle aktif...")
bot.polling()
        
