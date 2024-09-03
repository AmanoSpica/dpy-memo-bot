import discord
from discord import app_commands
from discord.ext import commands

import constants


class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="github-init",
    )
    @app_commands.describe(
        url="Github URL",
    )
    @app_commands.guild_only()
    async def github_init(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(ephemeral=True)
        if url.startswith("https://github.com"):
            formatted_url = url.replace("https://github.com", "github.com")
        elif url.startswith("https://www.github.com"):
            formatted_url = url.replace("https://www.github.com", "github.com")
        elif url.startswith("www.github.com"):
            formatted_url = url.replace("www.github.com", "github.com")
        else:
            await interaction.followup.send("Invalid URL")
            return

        git_user_name = formatted_url.split("/")[1]
        git_repo_name = formatted_url.split("/")[2]

        guild = interaction.guild
        category = await guild.create_category(f"GitHub/{git_user_name}/{git_repo_name}")
        main_channel = await category.create_text_channel(git_repo_name)
        webhook = await main_channel.create_webhook(name=f"GitHub-Webhook",
                                                    reason="MemoServerBot GitHub-init Command")

        embed = discord.Embed(
            title=f"[GitHub] {git_user_name}/{git_repo_name}",
            description=f"**GitHub Repository:** [{git_repo_name}]({url})\n**Webhook:** {webhook.url}/github",
            color=discord.Color.green(),
        )
        await main_channel.send(embed=embed)

        channel_names = ["memo", "log"]
        for channel_name in channel_names:
            await category.create_text_channel(channel_name)

        embed = discord.Embed(
            title="[Success] GitHub Init Command",
            description=f"**GitHub Repository:** [{git_repo_name}]({url})",
            color=discord.Color.green(),
        )
        await interaction.followup.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(GitHub(bot))
