import discord
from discord.ext import commands
import os

from config import TOKEN, TARGET_CHANNEL_ID
from keep_alive import server_on
from features.send_clip import send_clip_cmd
from features.menu_command import menu_cmd
from features.show_menu_button import show_menu_button_cmd

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

server_on()

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์: {bot.user}")

# โหลดคำสั่งย่อย
bot.command(name="ส่งคลิป")(send_clip_cmd(bot))
bot.command(name="เมนู")(menu_cmd(bot))
bot.command(name="แสดงปุ่มเมนู")(show_menu_button_cmd(bot))

bot.run(TOKEN)
