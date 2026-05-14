import discord
from discord import app_commands
from discord.ext import commands
import os
import time
from dotenv import load_dotenv
from services.check_user import verifyBio

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ROLE_NAME = os.getenv("ROLE_NAME", "Verificado")
SEARCH_STRING = os.getenv("VERIFY_STRING", "red")

# 5 minutos = 300 segundos
COOLDOWN_TIME = 300
cooldowns = {}


class VerifyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="verify",
        description="Verifica sua conta e adiciona o cargo se aprovado"
    )
    async def verify(self, interaction: discord.Interaction):

        author_id = interaction.user.id
        current_time = time.time()

        if author_id in cooldowns:

            remaining = cooldowns[author_id] - current_time

            if remaining > 0:

                minutes = int(remaining // 60)
                seconds = int(remaining % 60)

                embed = discord.Embed(
                    title="Aguarde antes de tentar novamente",
                    description=(
                        f"Você precisa esperar "
                        f"`{minutes}m {seconds}s` "
                        f"para usar o comando novamente."
                    ),
                    color=discord.Color.orange()
                )

                return await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )

        cooldowns[author_id] = current_time + COOLDOWN_TIME

        await interaction.response.defer(ephemeral=True)

        try:

            matches = verifyBio(
                user_id=str(author_id),
                search_string=SEARCH_STRING,
            )

            if not matches:

                embed = discord.Embed(
                    title="Verificação falhou",
                    description="Sua conta não atende aos critérios.",
                    color=discord.Color.red()
                )

                await interaction.followup.send(
                    embed=embed,
                    ephemeral=True
                )

                return

            guild = interaction.guild
            member = interaction.user

            role = discord.utils.get(
                guild.roles,
                name=ROLE_NAME
            )

            if role is None:

                embed = discord.Embed(
                    title="Cargo não encontrado",
                    description=f"O cargo '{ROLE_NAME}' não existe neste servidor.",
                    color=discord.Color.red()
                )

                await interaction.followup.send(
                    embed=embed,
                    ephemeral=True
                )

                return

            await member.add_roles(role)

            embed = discord.Embed(
                title="Verificado com sucesso!",
                description=f"Você recebeu o cargo **{role.name}**.",
                color=discord.Color.green()
            )

            await interaction.followup.send(
                embed=embed,
                ephemeral=True
            )

        except Exception as error:

            embed = discord.Embed(
                title="Erro ao verificar",
                description=str(error),
                color=discord.Color.red()
            )

            await interaction.followup.send(
                embed=embed,
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyCog(bot))