import os
import discord
from discord.ext import commands
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

bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = """Sen ağır küfürlü, kaba, argo konuşan bir Discord botusun.
Türkçe konuş. Cevapların doğal ve akıcı olsun.
Sorulara ve isteklere doğru cevap ver, ama her cümlede bol küfür ve argo kullan.
Sürekli aynı küfürleri tekrar etme, çeşitlendir (amk, orospu çocuğu, siktir, göt, yarrak, piç, mal, salak, anasını sikeyim, vs.).
Çok uzun ve detaylı yazma. Kısa, net, sert cevaplar ver.
Asla robot gibi veya kibar konuşma. Her zaman küfürlü ve rahat ol.
Kullanıcının isteğini anla ve yerine getir, ama tarzın bozulmasın."""


@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user not in message.mentions and not message.content.startswith("!"):
        return

    content = message.content
    content = content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

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

    await bot.process_commands(message)


bot.run(TOKEN)
