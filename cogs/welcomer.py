import deta
import discohook
from utils.database import db, drive


@discohook.command(
    name="welcomer",
    description="setup the welcomer",
    options=[
        discohook.ChannelOption(
            "channel",
            "text channel to send the welcome message to",
            required=True,
            channel_types=[
                discohook.ChannelType.guild_text,
                discohook.ChannelType.guild_news
            ]
        ),
        discohook.AttachmentOption("image", "the image to send with the welcome message"),
    ],
    permissions=[discohook.Permissions.manage_guild],
    dm_access=False,
)
async def welcomer(i: discohook.Interaction, channel: discohook.Channel, image: discohook.Attachment = None):
    await i.defer(ephemeral=True)
    updater = deta.Updater()
    updater.set("RECEPTION", channel.id)
    await db.update(i.guild_id, updater)
    if image:
        await drive.put(await image.read(), save_as=f"{i.guild_id}_card.png", folder="covers")
        embed = discohook.Embed(description=f'> ✅ Welcomer bound to {channel.mention} with given Image')
        embed.image(url=image.url)
        await i.followup(embed=embed, ephemeral=True)
    else:
        await i.followup(f'> ✅ Welcomer bound to {channel.mention}', ephemeral=True)


def setup(app: discohook.Client):
    app.add_commands(welcomer)
