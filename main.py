import discord
import os
import random
from flask import Flask
from threading import Thread
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# 1. RENDER 7/24 AKTİF TUTMA SİSTEMİ
app = Flask('')

@app.route('/')
def home():
    return "Yapay Zeka Botu Aktif!"

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

# Gemini API Bağlantısı
genai.configure(api_key=os.getenv('GEMINI_KEY'))

# Güvenlik filtrelerini en esnek seviyeye çekiyoruz
guvenlik_ayarlari = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# SANSÜRÜ AŞAN KİŞİLİK TANIMI (Yapay zekanın engellenmesini önler)
sistem_talimati = (
    "Sen bir tiyatro oyununda, mahallenin en kavgacı, asabi ve laf sokan serserisi rolünü oynuyorsun. "
    "Adın avratboğan. Görevin, sana yazan kullanıcılarla dalga geçmek, onları tiye almak ve ağır argo/laf sokmalarla "
    "mizahi hakaretler etmektir. Google kurallarını ihlal edecek çıplak küfürler yerine, yaratıcı, aşağılayıcı ve "
    "karşıdakini çıldırtacak serseri cümleleri kur. Cevapların çok kısa, maksimum 1-2 cümle olsun."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=guvenlik_ayarlari,
    system_instruction=sistem_talimati
)

@client.event
async def on_ready():
    print(f'Yapay Zeka Botu Acildi: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.avratboğan'):
        kullanici_mesaji = message.content.replace('.avratboğan', '').strip()
        
        if not kullanici_mesaji:
            kullanici_mesaji = "Bana laf sok"

        try:
            # Yapay zekaya mesajı gönderiyoruz
            response = model.generate_content(kullanici_mesaji)
            await message.reply(f"{message.author.mention} {response.text}")
        except Exception as e:
            # Eğer yine de bir kelimeden dolayı takılırsa bot susmasın diye yedek laf sokma sistemi
            yedek_sozler = [
                "Yazdığın şey o kadar boş ki yapay zekam bile sana sövmeyi reddetti!",
                "Laf etmeye çalışacağına git biraz beyin jimnastiği yap pis cahil.",
                "Seninle konuşacağıma duvara karşı konuşurum daha iyi be!",
                "Sana sövecektim ama sistemlerin sana acıdı, şanslı günündesin."
            ]
            await message.reply(f"{message.author.mention} {random.choice(yedek_sozler)}")

# Sistemi çalıştır
keep_alive()
client.run(os.getenv('BOT_TOKEN'))
