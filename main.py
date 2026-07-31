import os
import discord
from openai import OpenAI
TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not TOKEN or not GROQ_KEY:
    raise RuntimeError("DISCORD_TOKEN veya GROQ_API_KEY eksik!")
client = OpenAI(
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
SYSTEM_PROMPT = """Sen kaba, argo konuşan, biraz küfürlü bir Discord botusun.
Türkçe konuş. Cümlelerin düzgün, doğal ve akıcı olsun. Devrik cümle kurma.
Sorulara ve isteklere doğru, net cevap ver.
Ara sıra küfür ve argo kullan (amk, siktir, göt, piç, mal gibi) ama her cümlede değil. Abartma.
Kısa ve net cevaplar ver, gereksiz uzatma.
Robot gibi veya aşırı kibar konuşma. Rahat ve sokak ağzıyla konuş.
Kullanıcının isteğini anla ve yerine getir."""
@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Sadece etiketleyince veya ! ile başlayınca cevap ver
    if bot.user not in message.mentions and not message.content.startswith("!"):
        return
    content = message.content
    content = content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
   
    # ! işaretini de temizle
    if content.startswith("!"):
        content = content[1:].strip()
    if not content:
        return
    async with message.channel.typing():
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": content},
                ],
                max_tokens=250,
                temperature=0.9,
            )
            answer = response.choices[0].message.content.strip()
            await message.reply(answer)
        except Exception as e:
            await message.reply(f"Siktir git, hata çıktı amk: {e}")
bot.run(TOKEN)
