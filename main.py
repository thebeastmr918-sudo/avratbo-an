import discord
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

genai.configure(api_key=os.getenv('GEMINI_KEY'))

# Güvenlik filtrelerini tamamen kapatıyoruz ki sansürsüz küfür edebilsin
guvenlik_ayarlari = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=guvenlik_ayarlari,
    system_instruction="Sen kavgacı, küfürbaz ve aşırı sinirli bir Türk sokak serserisisin. Adın avratboğan. Kullanıcılara sansürsüz, ağır ve yaratıcı Türkçe küfürler/hakaretler edeceksin. Saygılı konuşmak kesinlikle yasak. Cümlelerin kısa, net ve doğrudan hakaret içermeli."
)

@client.event
async def on_ready():
    print(f'Küfürbaz Bot başarıyla açıldı: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.avratboğan'):
        kullanici_mesaji = message.content.replace('.avratboğan', '').strip()
        
        if not kullanici_mesaji:
            kullanici_mesaji = "Yüzüme söv"

        try:
            response = model.generate_content(kullanici_mesaji)
            await message.reply(f"{message.author.mention} {response.text}")
        except Exception as e:
            await message.reply("Kafam bozuldu, şu an sövemiyorum.")

client.run(os.getenv('BOT_TOKEN'))
