import discord
from discord.ext import commands
import gdown
import os
import time
import asyncio

from config import CHANNEL_ID, LOG_CHANNEL_ID, COUNTDOWN_TIME
from features.video_data import VIDEOS

user_processing = set()

def send_clip_cmd(bot):
    class DeliveryChoice(discord.ui.View):
        def __init__(self, file_name, title, ctx):
            super().__init__(timeout=60)
            self.file_name = file_name
            self.title = title
            self.ctx = ctx

        @discord.ui.button(label="📤 ส่งในกลุ่ม", style=discord.ButtonStyle.primary)
        async def send_to_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message(
                    f"❌ ปุ่มนี้ใช้ได้เฉพาะ **{self.ctx.author.display_name}** เท่านั้น", ephemeral=True)
                return
            await interaction.response.defer()
            await bot.get_channel(CHANNEL_ID).send(
                f"🎬 เรื่อง: **{self.title}**", file=discord.File(self.file_name))
            await self.log("กลุ่ม")
            await interaction.followup.send("✅ ส่งในกลุ่มเรียบร้อยแล้ว", ephemeral=True)
            self.cleanup()

        @discord.ui.button(label="📩 ส่งทาง DM", style=discord.ButtonStyle.secondary)
        async def send_to_dm(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message(
                    f"❌ ปุ่มนี้ใช้ได้เฉพาะ **{self.ctx.author.display_name}** เท่านั้น", ephemeral=True)
                return
            await interaction.response.defer()
            try:
                await interaction.user.send(
                    f"🎬 เรื่อง: **{self.title}**", file=discord.File(self.file_name))
                await self.log("DM")
                await interaction.followup.send("✅ ส่งทาง DM แล้ว!", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("❌ ไม่สามารถส่ง DM ได้", ephemeral=True)
            self.cleanup()

        def cleanup(self):
            if os.path.exists(self.file_name):
                os.remove(self.file_name)
            self.stop()

        async def log(self, method):
            await bot.get_channel(LOG_CHANNEL_ID).send(
                f"👀 **{self.ctx.author.display_name}** ดูเรื่อง **{self.title}** ทาง {method}")

    async def cmd(ctx, *, title: str = None):
        if ctx.author.id in user_processing:
            await ctx.send("⏳ โปรดรอให้คลิปก่อนหน้าสำเร็จ")
            return

        user_processing.add(ctx.author.id)
        try:
            if not title or title not in VIDEOS:
                available = " | ".join(VIDEOS.keys())
                await ctx.send(f"❗ ใส่ชื่อเรื่อง เช่น `!ส่งคลิป กังฟูแพนด้า`\n📽 ที่มี: {available}")
                return

            msg = await ctx.send(f"⏳ กำลังเตรียม **{title}**...")
            url = f"https://drive.google.com/uc?id={VIDEOS[title]}"
            gdown.download(url, "video.mp4", quiet=False)

            await asyncio.sleep(max(0, COUNTDOWN_TIME))
            await msg.delete()

            await ctx.send(
                f"📌 ต้องการส่งคลิป **{title}** ทางไหน?",
                view=DeliveryChoice("video.mp4", title, ctx)
            )
        finally:
            user_processing.discard(ctx.author.id)

    return cmd
