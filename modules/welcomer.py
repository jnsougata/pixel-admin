import deta
import discohook as dh
from utils.db import db, drive


@dh.command(
    name="welcomer",
    description="setup the welcomer",
    options=[
        dh.ChannelOption(
            "channel",
            "the channel to send the welcome message to",
            required=True, channel_types=[dh.ChannelType.guild_text]
        ),
        dh.AttachmentOption("image", "the image to send with the welcome message"),
    ],
    permissions=[dh.Permissions.manage_guild],
    dm_access=False,
)
async def welcomer(i: dh.Interaction, channel: dh.Channel, image: dh.Attachment = None):
    await i.defer(ephemeral=True)
    updater = deta.Updater()
    updater.set("RECEPTION", channel.id)
    await db.update(i.guild_id, updater)
    if image:
        await drive.put(await image.read(), save_as=f"{i.guild_id}_card.png", folder="covers")
        embed = dh.Embed(description=f'> ✅ Welcomer bound to {channel.mention} with given Image')
        embed.image(url=image.url)
        await i.followup(embed=embed, ephemeral=True)
    else:
        await i.followup(f'> ✅ Welcomer bound to {channel.mention}', ephemeral=True)


def setup(app: dh.Client):
    app.load_commands(welcomer)
