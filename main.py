import discord
import os
import random
from flask import Flask
from threading import Thread
import google.generativeai as genai

# 1. RENDER 7/24 AKTİF TUTMA SİSTEMİ
app = Flask('')

@app.route('/')
def home():
    return "Küfürbaz Hesap Motoru Aktif!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. DISCORD VE YAPAY ZEKA AYARLARI
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Yapay zekaya SADECE düz hesaplama yapmasını emrediyoruz (Sıfır sansür riski)
genai.configure(api_key=os.getenv('GEMINI_KEY'))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Sen yardımcı bir asistansın. Kullanıcının sorduğu soruları veya matematik işlemlerini çok kısa, net ve sadece tek bir cümleyle cevapla."
)

# SANSÜRSÜZ AĞIR KÜFÜR HAVUZU (İstediğin gibi ana avrat doldurabilirsin)
kufurler = [
    "senin o doğduğun günkü ebeveynlerinin aklını fikrini sikeyim,",
    "amına koyduğumun evladı,",
    "anasını avradını gelmişini geçmişini siktiğimin salağı,",
    "seni öyle bir sike sike çoğaltırım ki,",
    "yedi ceddini, soyunu sopunu tek tek sikeyim senin,",
    "amına koduğumun çocuğu,"
]

@client.event
async def on_ready():
    print(f'Bot başarıyla açıldı: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.avratboğan'):
        kullanici_mesaji = message.content.replace('.avratboğan', '').strip()
        
        if not kullanici_mesaji:
            kullanici_mesaji = "Naber"

        try:
            # 1. Yapay zeka soruyu düz ve normal şekilde cevaplıyor (Engele takılmıyor)
            response = model.generate_content(kullanici_mesaji)
            temiz_cevap = response.text.strip()
            
            # 2. Küfür havuzundan rastgele ağır bir ana avrat küfür seçiliyor
            secilen_kufur = random.choice(kufurler)
            
            # 3. Küfür ile yapay zekanın bulduğu doğru cevap birleştiriliyor
            tam_cevap = f"{secilen_kufur} {temiz_cevap}"
            
            # Sonuç: Kullanıcıyı etiketleyerek yapıştırır
            await message.reply(f"{message.author.mention} {tam_cevap}")
            
        except Exception as e:
            # Eğer yine de bir hata olursa bot susmasın diye yedek liste
            await message.reply(f"{message.author.mention} Amına koduğumun çocuğu, kafam bozuldu yazma bana!")

keep_alive()
client.run(os.getenv('BOT_TOKEN'))
