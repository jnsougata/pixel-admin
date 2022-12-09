import deta
import discohook as dh
from utils.db import db


class Pingrole(dh.Cog):
    
    @dh.Cog.command(
        id="1049447008433340538",
        name="pingrole",
        description="set the role to ping with youtube feeds",
        options=[dh.RoleOption("role", "the role to ping", required=True)],
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def pingrole(self, i: dh.CommandInteraction, role: dh.Role):
        if role.managed:
            return await i.response("> ⚠️ Role must be a guild role", ephemeral=True)
        await i.defer(ephemeral=True)
        updater = deta.Updater()
        updater.set("PINGROLE", role.id)
        await db.update(i.guild_id, updater)
        mention = role.mention if role.position != 0 else '@everyone'
        emd = dh.Embed(description=f'> ✅ {mention} added successfully as pingrole', color=0xc4302b)
        await i.follow_up(embed=emd, ephemeral=True)
        

def setup(app: dh.Client):
    app.add_cog(Pingrole())
