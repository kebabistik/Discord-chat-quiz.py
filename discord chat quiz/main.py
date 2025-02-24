import discord
import random
import asyncio
from discord.ext import commands
from discord import Embed

# Sorular ve cevaplar listesi
questions = {
    "Dünyanın en büyük okyanusu hangisidir?": "Pasifik Okyanusu",
    "Einstein'ın ünlü formülü nedir?": "E=mc^2",
    "Python'un yaratıcısı kimdir?": "Guido van Rossum",
    "Ay hangi gezegenin uydusudur?": "Dünya",
    "Hangi gezegen kırmızı renkli görünür?": "Mars",
    "Hangi ülkenin başkenti Paris'tir?": "Fransa",
    "Hangi elementin sembolü 'O'dur?": "Oksijen",
    "Hangi gezegen Güneş Sistemi'ndeki en büyük gezegendir?": "Jüpiter",
    "Hangi yıl Apollo 11 Ay'a iniş yaptı?": "1969",
    "Hangi ülke Eiffel Kulesi'ne ev sahipliği yapar?": "Fransa"
}

TOKEN = "Bura Token giriniz"  # Bot tokeninizi buraya ekleyin
intents = discord.Intents.default()
intents.message_content = True  # Mesaj içeriğini okumak için gerekli
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")
    bot.loop.create_task(ask_question_periodically())

async def ask_question_periodically():
    await bot.wait_until_ready()
    channel_id = kanal_id_girin  # Mesajın gönderileceği kanal ID'si
    channel = bot.get_channel(channel_id)
    while not bot.is_closed():
        question, correct_answer = random.choice(list(questions.items()))
        
        # Soruyu Embed ile gönder
        embed = Embed(
            title="🎯 **Yeni Soru** 🎯",
            description=f"**{question}**",
            color=discord.Color.blue()  # Mavi renk
        )
        if channel:
            await channel.send(embed=embed)
        
        def check(m):
            return m.content.lower() == correct_answer.lower() and m.channel == channel
        
        try:
            msg = await bot.wait_for("message", timeout=10.0, check=check)
            # Doğru cevap veren kullanıcıyı etiketle ve fotoğraf gönder
            success_embed = Embed(
                title="🎉 **Tebrikler!** 🎉",
                description=f"Helal {msg.author.mention}, doğru cevabı bildin!",
                color=discord.Color.green()  # Yeşil renk
            )
            await channel.send(embed=success_embed)
            
            # Fotoğrafı ekle (örnek olarak bir dosya yolu belirtin)
            with open("indir.jpg", "rb") as f:
                picture = discord.File(f)
                await channel.send(file=picture)
        except asyncio.TimeoutError:
            timeout_embed = Embed(
                title="⏳ **Zaman Doldu!** ⏳",
                description=f"Kimse doğru cevabı bilemedi. Doğru cevap: **{correct_answer}**",
                color=discord.Color.red()  # Kırmızı renk
            )
            await channel.send(embed=timeout_embed)
        
        await asyncio.sleep(600)  # 10 dakika bekle

bot.run(TOKEN)