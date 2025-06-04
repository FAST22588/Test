import discord
from discord.ext import commands
from config import TARGET_CHANNEL_ID
from views.menu_view import MenuView

class MenuTrigger(discord.ui.View):
    @discord.ui.button(label="📋 เปิดเมนูวิดีโอ", style=discord.ButtonStyle.success)
    async def menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
        if channel:
            await channel.send("📋 กรุณาเลือกชื่อเรื่อง:", view=MenuView(interaction))
            await interaction.followup.send("✅ เปิดเมนูแล้ว", ephemeral=True)
        else:
            await interaction.followup.send("❌ ไม่พบห้องที่กำหนด", ephemeral=True)

def setup(bot):
    @bot.command()
    async def แสดงปุ่มเมนู(ctx):
        channel = ctx.bot.get_channel(TARGET_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="🎬 เมนูวิดีโอฟรี",
                description="กดปุ่มเพื่อเปิดเมนูเลือกวิดีโอ",
                color=discord.Color.green()
            )
            await channel.send(embed=embed, view=MenuTrigger())
            await ctx.send("✅ ส่งปุ่มเมนูแล้ว")
        else:
            await ctx.send("❌ ไม่พบห้องเป้าหมาย")
