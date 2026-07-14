import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading
from utils import check_ban

app = Flask(__name__)

load_dotenv()
APPLICATION_ID = os.getenv("APPLICATION_ID")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

DEFAULT_LANG = "en"
user_languages = {}

BANCHECK_CHANNEL_ID = 1526554000823156860

ROASTS = [
    "Bhai padhna likhna seekh le, ye wala channel nahi hai 💀 Ja <#{channel}> me.",
    "Itna bada server, phir bhi galat channel dhundh liya. Talent hai bhai 👏 Sahi jagah: <#{channel}>",
    "UID check karne aaya tha, khud ka dimag check kara le pehle 🧠❌ Command <#{channel}> me chalti hai.",
    "Bhai tu Free Fire me bhi aise hi random jagah land karta hai kya? 🪂 <#{channel}> me aa.",
    "Ye channel teri command ke liye nahi bana hai, samjha kar 💅 <#{channel}> me try kar.",
    "Headshot to door ki baat hai, tu channel pe hi miss kar gaya 🎯 <#{channel}> me ja.",
    "GPS kharab hai kya bhai? Destination: <#{channel}> 🗺️",
    "Rank push baad me, pehle sahi channel push kar le 📉 <#{channel}> me chal.",
    "Booyah to tab milega jab command sahi channel me hogi 🏆 <#{channel}> me aa ja.",
    "Bhai lobby me ghusne se pehle map dekh liya kar 🤦 Command yaha nahi, <#{channel}> me.",
    "Grandmaster banne chala hai, channel to pehle dhundh le 🥴 <#{channel}> me aa.",
    "Teri aim aur teri channel choice, dono ka same haal hai 😭 <#{channel}> me ja bhai.",
    "Bhai ye Factory roof nahi hai jahan kahin bhi kood jaye 🏭 Command <#{channel}> me chalegi.",
    "Wrong number bhai, yahan nahi 📞 Sahi line: <#{channel}>",
    "Tu wahi banda hai na jo Bermuda me Peak jaake lootta kuch nahi 💀 <#{channel}> me aa.",
    "Command dalne se pehle chashma pehen le bhai 🤓 Channel ye raha: <#{channel}>",
    "Gloo wall bhi teri tarah galat jagah lagti hogi 🧱 <#{channel}> me try kar.",
    "Bhai server me ghum ne nahi, command chalane aaya hai to <#{channel}> me chal 🚶",
    "Itni mehnat galat channel dhundhne me lagayi, utni rank me lagata to Heroic hota 📈 <#{channel}> me ja.",
    "Ye channel dekh ke lagta hai tujhe minimap band karke khelna pasand hai 🗺️❌ <#{channel}> me aa.",
    "Teri UID se pehle teri channel-sense check honi chahiye 🩺 <#{channel}> me chal.",
    "Bhai revive to milta hai, par galat channel ka koi ilaaj nahi 💊 <#{channel}> me ja.",
    "Zone ke bahar khada hai bhai tu, damage kha raha hai 🔥 Safe zone: <#{channel}>",
    "Bot bhi soch raha hai ki isko channel kaun samjhaye 🤖💔 <#{channel}> me aa ja.",
    "Solo vs Squad khelta hoga tu, par channel vs channel me haar gaya 😔 <#{channel}> me chal.",
    "Bhai keyboard sahi hai, bas dimag ka aim off hai 🎮 Command <#{channel}> me daal.",
    "Airdrop bhi sahi jagah girta hai, ek tu hi hai jo nahi girta 📦 <#{channel}> me aa.",
    "Ye channel scan kiya, teri command allowed nahi mili 🔍❌ <#{channel}> me try kar.",
    "Bhai practice mode me ja ke channel dhundhna seekh le pehle 🏋️ Sahi jagah: <#{channel}>",
    "Clutch to door, tu to channel hi nahi dhundh paya 1v1 me kya karega 💀 <#{channel}> me chal.",
]

nomBot = "None"

@app.route('/')
def home():
    global nomBot
    return f"Bot {nomBot} is working"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask).start()

@bot.event
async def on_ready():
    global nomBot
    nomBot = f"{bot.user}"
    print(f"Le bot est connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == BANCHECK_CHANNEL_ID:
        ctx = await bot.get_context(message)
        if not ctx.valid:
            try:
                await message.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
            else:
                await message.channel.send(
                    f"{message.author.mention} ⚠️ Ye channel sirf commands ke liye hai! (`!bancheck <UID>`)",
                    delete_after=5
                )
            return

    await bot.process_commands(message)

@bot.command(name="guilds")
async def show_guilds(ctx):
    guild_names = [f"{i+1}. {guild.name}" for i, guild in enumerate(bot.guilds)]
    guild_list = "\n".join(guild_names)
    await ctx.send(f"Le bot est dans les guilds suivantes :\n{guild_list}")

@bot.command(name="lang")
async def change_language(ctx, lang_code: str):
    lang_code = lang_code.lower()
    if lang_code not in ["en", "fr"]:
        await ctx.send("❌ Invalid language. Available: `en`, `fr`")
        return

    user_languages[ctx.author.id] = lang_code
    message = "✅ Language set to English." if lang_code == 'en' else "✅ Langue définie sur le français."
    await ctx.send(f"{ctx.author.mention} {message}")

@bot.command(name="bancheck", aliases=["ID"])
async def check_ban_command(ctx, user_id: str = ""):
    if ctx.channel.id != BANCHECK_CHANNEL_ID:
        roast = random.choice(ROASTS).format(channel=BANCHECK_CHANNEL_ID)
        await ctx.send(f"{ctx.author.mention} {roast}")
        return

    user_id = user_id.strip()
    lang = user_languages.get(ctx.author.id, "en")

    print(f"Commande fait par {ctx.author} (lang={lang})")

    if not user_id.isdigit():
        message = {
            "en": f"{ctx.author.mention} ❌ **Invalid UID!**\n➡️ Please use: `!bancheck 123456789`",
            "fr": f"{ctx.author.mention} ❌ **UID invalide !**\n➡️ Veuillez fournir un UID valide sous la forme : `!bancheck 123456789`"
        }
        await ctx.send(message[lang])
        return

    async with ctx.typing():
        try:
            ban_status = await check_ban(user_id)
        except Exception as e:
            await ctx.send(f"{ctx.author.mention} ⚠️ Error:\n```{str(e)}```")
            return

        if ban_status is None:
            message = {
                "en": f"{ctx.author.mention} ❌ **Could not get information. Please try again later.**",
                "fr": f"{ctx.author.mention} ❌ **Impossible d'obtenir les informations.**\nVeuillez réessayer plus tard."
            }
            await ctx.send(message[lang])
            return

        is_banned = int(ban_status.get("is_banned", 0))
        period = ban_status.get("period", "N/A")
        nickname = ban_status.get("nickname", "NA")
        region = ban_status.get("region", "N/A")
        id_str = f"`{user_id}`"

        if isinstance(period, int):
            period_str = f"more than {period} months" if lang == "en" else f"plus de {period} mois"
        else:
            period_str = "unavailable" if lang == "en" else "indisponible"

        embed = discord.Embed(
            color=0xFF0000 if is_banned else 0x00FF00,
            timestamp=ctx.message.created_at
        )

        if is_banned:
            embed.title = "**▌ Banned Account 🛑 **" if lang == "en" else "**▌ Compte banni 🛑 **"
            embed.description = (
                f"**• {'Reason' if lang == 'en' else 'Raison'} :** "
                f"{'This account was confirmed for using cheats.' if lang == 'en' else 'Ce compte a été confirmé comme utilisant des hacks.'}\n"
                f"**• {'Suspension duration' if lang == 'en' else 'Durée de la suspension'} :** {period_str}\n"
                f"**• {'Nickname' if lang == 'en' else 'Pseudo'} :** `{nickname}`\n"
                f"**• {'Player ID' if lang == 'en' else 'ID du joueur'} :** `{id_str}`\n"
                f"**• {'Region' if lang == 'en' else 'Région'} :** `{region}`"
            )
            # embed.set_image(url="https://i.ibb.co/wFxTy8TZ/banned.gif")
            file = discord.File("assets/banned.gif", filename="banned.gif")
            embed.set_image(url="attachment://banned.gif")
        else:
            embed.title = "**▌ Clean Account ✅ **" if lang == "en" else "**▌ Compte non banni ✅ **"
            embed.description = (
                f"**• {'Status' if lang == 'en' else 'Statut'} :** "
                f"{'No sufficient evidence of cheat usage on this account.' if lang == 'en' else 'Aucune preuve suffisante pour confirmer l’utilisation de hacks sur ce compte.'}\n"
                f"**• {'Nickname' if lang == 'en' else 'Pseudo'} :** `{nickname}`\n"
                f"**• {'Player ID' if lang == 'en' else 'ID du joueur'} :** `{id_str}`\n"
                f"**• {'Region' if lang == 'en' else 'Région'} :** `{region}`"
            )
            # embed.set_image(url="https://i.ibb.co/Kx1RYVKZ/notbanned.gif")
            file = discord.File("assets/notbanned.gif", filename="notbanned.gif")
            embed.set_image(url="attachment://notbanned.gif")

        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.set_footer(text="Developed by Ashutosh Shandilay")
        await ctx.send(f"{ctx.author.mention}", embed=embed ,file=file)

bot.run(TOKEN)
