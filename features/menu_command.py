import discord
from features.video_data import VIDEOS
from config import TARGET_CHANNEL_ID

def menu_cmd(bot):
    class MenuView(discord.ui.View):
        def __init__(self, ctx):
            super().__init__(timeout=60)
            self.ctx = ctx
            self.used = False
            for title in VIDEOS.keys():
                self.add_item(MenuButton(title, ctx, self))

    class MenuButton(discord.ui.Button):
        def __init__(self, title, ctx, view):
            super().__init__(label=title, style=discord.ButtonStyle.primary)
            self.title = title
            self.ctx = ctx
            self.parent_view = view

        async def callback(self, interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message(
                    f"❌ เมนูนี้สำหรับ **{self.ctx.author.display_name}** เท่านั้น", ephemeral=True)
                return
            if self.parent_view.used:
                await interaction.response.send_message("⚠️ เลือกได้ครั้งเดียว", ephemeral=True)
                return

            self.parent_view.used = True
            await interaction.response.defer()
            await self.ctx.invoke(bot.get_command("ส่งคลิป"), title=self.title)

            for child in self.parent_view.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await interaction.message.edit(view=self.parent_view)
            self.parent_view.stop()

    async def cmd(ctx):
        if ctx.channel.id != TARGET_CHANNEL_ID:
            await ctx.send("❌ ใช้คำสั่งนี้ได้เฉพาะในห้องที่กำหนด")
            return
        await ctx.send("📋 กรุณาเลือกชื่อเรื่อง:", view=MenuView(ctx))

    return cmd
