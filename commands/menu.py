from discord.ext import commands
from config import TARGET_CHANNEL_ID
from views.menu_view import MenuView

def setup(bot):
    @bot.command()
    async def เมนู(ctx):
        if ctx.channel.id != TARGET_CHANNEL_ID:
            await ctx.send("❌ ใช้คำสั่งนี้ได้เฉพาะห้องที่กำหนด")
            return
        view = MenuView(ctx)
        await ctx.send("📋 กรุณาเลือกชื่อเรื่องที่ต้องการ:", view=view)
