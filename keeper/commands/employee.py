from typing import Optional
from enum import Enum

from keeper.client import *
from keeper.dbfunctions import dbfunctions as db

logging.debug("loading employee commands")


@client.tree.command()
async def clock_in(interaction: discord.Interaction, user: discord.User = None):
    """Lets you clock in yourself or another user."""
    print(user)
    await interaction.response.send_message("Hi :)", delete_after=1)


class ActiveClockOut(Enum):
    on = 1
    off = 0


@client.tree.command()
async def auto_clock_out(interaction: discord.Interaction, active: ActiveClockOut):
    if active is None:
        await interaction.response.send_message(f"Currently turned off")
    else:
        await interaction.response.send_message(f"Turned o{'n' if active else 'ff'}")


@client.tree.command()
async def info(interaction: discord.Interaction, user: discord.User = None):
    db_guild = db.get_guild(interaction.guild_id)
    if not user:
        user = interaction.user
    else:
        ia_user = interaction.user
        if not (ia_user.guild_permissions.administrator or db_guild.manager_role in [r.id for r in ia_user.roles]):
            await interaction.response.send_message("Missing permissions!", ephemeral=True)
            return

    db_user = db.get_employee(user.id, interaction.guild_id)
    if db_user:
        await interaction.response.send_message(str(db_user), ephemeral=True)
        # TODO: Embed
    else:
        await interaction.response.send_message("User is not in the system!", ephemeral=True)
