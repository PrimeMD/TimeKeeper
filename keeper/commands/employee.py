from keeper.client import *

# import typing

logging.debug("loading employee commands")


@client.tree.command()
async def clock_in(interaction: discord.Interaction, user: discord.User = None):
    """Lets you clock in yourself or another user."""
    print(user)
    await interaction.response.send_message("Hi :)", delete_after=1)


print(client)
