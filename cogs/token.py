import secrets

import deta
import discohook
from utils.database import db


@discohook.command(
    permissions=[discohook.Permission.manage_guild],
    dm_access=False,
)
async def server_token(i: discohook.Interaction):
    """
    Generate a token for your server.
    """
    await i.response.defer(ephemeral=True)
    token = f"{i.guild_id}.{secrets.token_urlsafe(32)}"
    updater = deta.Updater()
    updater.set("TOKEN", token)
    await db.update(i.guild_id, updater)
    embed = discohook.Embed(description=f'> ✅ Token generated successfully\n\n```\n{token}\n```')
    await i.response.followup(embed=embed)


def setup(app: discohook.Client):
    app.add_commands(server_token)
