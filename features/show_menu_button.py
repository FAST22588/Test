import discord
from config import TARGET_CHANNEL_ID
from features.menu_command import menu_cmd

def show_menu_button_cmd(bot):
    class MenuTrigger(discord.ui.View):
        @discord.ui.button(label="📋 เปิดเมนูวิดีโอ", style=discord.ButtonStyle.success)
        async def menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            channel = interaction.guild.get_channel(TARGET_CHANNEL_ID)
            if channel:
                view = menu_cmd(bot).__closure__[0].cell_contents(interaction)
                await channel.send("📋 กรุณาเลือกชื่อเรื่อง:", view=view)
                await interaction.followup.send("✅ เปิดเมนูในห้องแล้ว", ephemeral=True)
            else:
                await interaction.followup.send("❌ ไม่พบห้องที่กำหนด", ephemeral=True)

    async def cmd(ctx):
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="🎬 เมนูวิดีโอฟรี",
                description="กดปุ่มด้านล่างเพื่อเปิดเมนูเลือกวิดีโอ",
                color=discord.Color.green()
            )
            await channel.send(embed=embed, view=MenuTrigger())
            await ctx.send("✅ ส่งปุ่มเมนูเรียบร้อยแล้ว")
        else:
            await ctx.send("❌ ไม่พบห้องเป้าหมาย")

    return cmd
