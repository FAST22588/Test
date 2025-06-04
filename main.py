import discord
from discord.ext import commands
from keep_alive import server_on

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

server_on()

@bot.event
async def on_ready():
    print(f"✅ Bot พร้อมใช้งาน: {bot.user}")

# โหลดคำสั่ง
from commands.send_clip import setup as setup_clip
from commands.menu import setup as setup_menu
from commands.show_menu_button import setup as setup_button

setup_clip(bot)
setup_menu(bot)
setup_button(bot)

bot.run(__import__('config').TOKEN)
