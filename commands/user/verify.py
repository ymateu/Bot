import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from services.check_user import verifyBio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ROLE_NAME = os.getenv("ROLE_NAME", "Verificado")
SEARCH_STRING = os.getenv("VERIFY_STRING", "Java")


class VerifyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="verify", description="Verifica sua própria bio e adiciona cargo se aprovado")
    async def verify(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        author_id = interaction.user.id

        try:
            matches = verifyBio(
                user_id=str(author_id),
                search_string=SEARCH_STRING,
            )

            if not matches:
                embed = discord.Embed(
                    title="Verificação falhou",
                    description=f"Sua bio não contém a string `{SEARCH_STRING}`.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            guild = interaction.guild
            member = interaction.user
            role = discord.utils.get(guild.roles, name=ROLE_NAME)

            if role is None:
                embed = discord.Embed(
                    title="Cargo não encontrado",
                    description=f"O cargo '{ROLE_NAME}' não existe neste servidor.",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            await member.add_roles(role)
            embed = discord.Embed(
                title="Verificado com sucesso!",
                description=f"Você recebeu o cargo **{role.name}**.",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as error:
            embed = discord.Embed(
                title="Erro ao verificar",
                description=str(error),
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyCog(bot))
