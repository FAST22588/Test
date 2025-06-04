import os
import discord
from config import CHANNEL_ID, LOG_CHANNEL_ID

class DeliveryChoice(discord.ui.View):
    def __init__(self, file_name, title, ctx):
        super().__init__(timeout=60)
        self.file_name = file_name
        self.title = title
        self.ctx = ctx

    @discord.ui.button(label="📤 ส่งในกลุ่ม", style=discord.ButtonStyle.primary)
    async def send_to_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"❌ ใช้ได้เฉพาะ {self.ctx.author.display_name}", ephemeral=True)
            return

        await interaction.response.defer()
        video_channel = self.ctx.bot.get_channel(CHANNEL_ID)
        if video_channel:
            await video_channel.send(f"🎬 เรื่อง: **{self.title}**", file=discord.File(self.file_name))
        await self.log("กลุ่ม")
        await interaction.followup.send("✅ ส่งในกลุ่มแล้ว", ephemeral=True)
        self.cleanup()

    @discord.ui.button(label="📩 ส่งทาง DM", style=discord.ButtonStyle.secondary)
    async def send_to_dm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"❌ ใช้ได้เฉพาะ {self.ctx.author.display_name}", ephemeral=True)
            return

        await interaction.response.defer()
        try:
            await interaction.user.send(f"🎬 เรื่อง: **{self.title}**", file=discord.File(self.file_name))
            await self.log("DM")
            await interaction.followup.send("✅ ส่งทาง DM แล้ว", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ ไม่สามารถส่ง DM ได้", ephemeral=True)
        self.cleanup()

    def cleanup(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.stop()

    async def log(self, method):
        log_channel = self.ctx.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"👀 {self.ctx.author.display_name} ดูเรื่อง **{self.title}** ทาง {method}")
