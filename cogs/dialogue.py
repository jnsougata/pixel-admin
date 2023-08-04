import deta
import discohook
from utils.database import db


feed = (
    '[ping] will be replaced with Role Ping'
    '\n[url] will be replaced with the Video URL'
    '\n[name] will be replaced with the Channel NAME'
)


@discohook.modal(
    "YouTube Feed Custom Dialogue",
    fields=[
        discohook.TextInput(
            "Dialogue",
            "custom",
            default_text=feed,
            style=discohook.TextInputFieldLength.long,
            required=True,
        )
    ]
)
async def dialogue_modal(m: discohook.Interaction, custom: str):
    record = await db.get(m.guild_id)
    if not record or not record.get("CUSTOM"):
        u = deta.Updater()
        u.set("CUSTOM", {"youtube": ""})
        await db.update(m.guild_id, u)
    updater = deta.Updater()
    updater.set("CUSTOM.youtube", custom)
    await db.update(m.guild_id, updater)
    embed = discohook.Embed(description=f'> ✅ Custom Dialogue set for YouTube Feed\n\n```\n{custom}\n```')
    await m.response.send(embed=embed, ephemeral=True)


@discohook.command(
    permissions=[discohook.Permission.manage_guild],
    dm_access=False,
)
async def dialogue(i: discohook.Interaction):
    """
    Set a custom dialogue for the feed.
    """
    await i.response.send_modal(modal=dialogue_modal)


def setup(app: discohook.Client):
    app.add_commands(dialogue)
