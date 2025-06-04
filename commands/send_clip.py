import discord, asyncio, time, gdown, os
from discord.ext import commands
from config import VIDEOS, COUNTDOWN_TIME
from views.delivery_view import DeliveryChoice

user_processing = set()

def setup(bot):
    @bot.command()
    async def ส่งคลิป(ctx, *, title: str = None):
        if ctx.author.id in user_processing:
            await ctx.send("⏳ โปรดรอคำสั่งก่อนหน้าสำเร็จ")
            return

        user_processing.add(ctx.author.id)
        try:
            if not title:
                await ctx.send(f"❗ กรุณาระบุชื่อเรื่อง เช่น `!ส่งคลิป กังฟูแพนด้า`\n📽 มีให้: {' | '.join(VIDEOS)}")
                return

            title = title.strip()
            if title not in VIDEOS:
                await ctx.send(f"❌ ไม่พบชื่อเรื่อง: **{title}**\n📽 เลือกจาก: {' | '.join(VIDEOS)}")
                return

            msg = await ctx.send(f"⏳ เตรียมส่ง **{title}**...")
            url = f"https://drive.google.com/uc?id={VIDEOS[title]}"
            FILE_NAME = "video.mp4"
            gdown.download(url, FILE_NAME, quiet=False)

            elapsed = time.time() - time.time()
            remaining = max(0, int(COUNTDOWN_TIME - elapsed))
            for i in range(remaining, 0, -1):
                await msg.edit(content=f"⏳ ส่งใน {i} วิ...")
                await asyncio.sleep(1)
            await msg.delete()

            await ctx.send(f"📌 ส่งคลิป **{title}** ทางไหน?", view=DeliveryChoice(FILE_NAME, title, ctx))
        finally:
            user_processing.discard(ctx.author.id)
