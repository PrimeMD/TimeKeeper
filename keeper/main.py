from keeper.client import *
import commands


@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user} (ID: {client.user.id})')


client.run(config["bot"]["token"])
