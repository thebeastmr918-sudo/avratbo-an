import discord
import random
import os
from flask import Flask
from threading import Thread

# 1. RENDER 7/24 AKTİF TUTMA SİSTEMİ
app = Flask('')

@app.route('/')
def home():
    return "Küfür Makinesi Aktif!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. DISCORD SÖVGÜ BOTU SİSTEMİ
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# SANSÜRSÜZ KÜFÜR LİSTESİ (Burayı istediğin gibi ana avrat doldurabilirsin)
sozler = [
    "Senin o doğduğun günkü ebeveynlerinin aklını fikrini sikeyim, tipini siktiğimin fırlatması!",
    "Ulan amına koyduğumun evladı, sen konuşunca benim buradaki sigortalarım atıyor, uza şuradan!",
    "Anasını avradını gelmişini geçmişini siktiğimin salağı, ne yazıp duruyorsun buraya?!",
    "Seni öyle bir sike sike çoğaltırım ki sülalen darmadağın olur amcık hoşafı!",
    "Yedi ceddini, soyunu sopunu, gelmişini geçmişini tek tek sikeyim senin!",
    "Boş yapma anasını avradını siktiğimin iti, git iki dakika ötede havla!",
    "Ulan amına koduğumun çocuğu, sen bu zekayla bu yaşa kadar nasıl hayatta kaldın lan?"
]

@client.event
async def on_ready():
    print(f'Sövgü Botu Başarıyla Açıldı: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.avratboğan'):
        # Listeden en ağır küfürlerden birini rastgele seçer
        rastgele_sovgü = random.choice(sozler)
        # Karşıdaki kişiyi etiketleyerek küfrü yüzüne vurur
        await message.reply(f"{message.author.mention} {rastgele_sovgü}")

# Sistemi çalıştır
keep_alive()
client.run(os.getenv('BOT_TOKEN'))
