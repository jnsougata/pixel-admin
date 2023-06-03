import deta
import discohook
from utils.database import db


for_feed = (
    '[ping] will be replaced with Role Ping'
    '\n[url] will be replaced with the Video URL'
    '\n[name] will be replaced with the Channel NAME'
)


@discohook.command(
    name="dialogue",
    description="set a custom dialogue for the welcomer and feed",
    permissions=[discohook.Permissions.manage_guild],
    dm_access=False,
)
async def dialogue_command(i: discohook.Interaction):
    modal = discohook.Modal("YouTube Feed Custom Dialogue")
    modal.add_field("Options", "options", default_text=for_feed, style=discohook.TextInputFieldLength.long)

    @modal.on_interaction
    async def submit(m: discohook.Interaction, dialogue: str = None):
        record = await db.get(m.guild_id)
        if not record or not record.get("CUSTOM"):
            u = deta.Updater()
            u.set("CUSTOM", {"youtube": ""})
            await db.update(m.guild_id, u)

        updater = deta.Updater()
        updater.set("CUSTOM.youtube", dialogue)
        await db.update(m.guild_id, updater)
        embed = discohook.Embed(description=f'> ✅ Custom Dialogue set for YouTube Feed\n\n```\n{dialogue}\n```')
        await m.response(embed=embed, ephemeral=True)

    modal.add_field("Custom Dialogue", "dialogue", required=True, style=discohook.TextInputFieldLength.long)
    await i.send_modal(modal=modal)


def setup(app: discohook.Client):
    app.add_commands(dialogue_command)
