import deta
import discohook
from utils.db import db


@discohook.command(
    name="pingrole",
    description="set the role to ping with youtube feeds",
    options=[discohook.RoleOption("role", "the role to ping", required=True)],
    permissions=[discohook.Permissions.manage_guild],
    dm_access=False,
)
async def pingrole(i: discohook.Interaction, role: discohook.Role):
    if role.managed:
        return await i.response("> ⚠️ Role must be a guild role", ephemeral=True)
    await i.defer(ephemeral=True)
    updater = deta.Updater()
    updater.set("PINGROLE", role.id)
    await db.update(i.guild_id, updater)
    mention = role.mention if role.position != 0 else '@everyone'
    emd = discohook.Embed(description=f'> ✅ {mention} added successfully as pingrole', color=0xc4302b)
    await i.followup(embed=emd, ephemeral=True)


def setup(app: discohook.Client):
    app.add_commands(pingrole)