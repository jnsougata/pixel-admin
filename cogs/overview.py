import io

import deta
import discohook
from utils.database import db, drive


@discohook.command(
    name="overview",
    description="check any currently set server config",
    options=[
        discohook.IntegerOption(
            "option",
            "the option to check",
            required=True,
            choices=[
                discohook.Choice("YouTube", 1),
                discohook.Choice("Pingrole", 2),
                discohook.Choice("Welcomer", 3),
            ]
        ),
    ],
    permissions=[discohook.Permissions.manage_guild],
    dm_access=False,
)
async def overview(i: discohook.Interaction, option: int):
    await i.defer(ephemeral=True)
    try:
        record = await db.get(i.guild_id)
    except deta.NotFound:
        return await i.followup("> ⚠️ No Server Config Found")
    else:
        if option == 1:
            if not record.get("CHANNELS"):
                return await i.followup("> ⚠️ No channels subscribed")
            else:
                channel_ids = list(record["CHANNELS"].keys())
                embed = discohook.Embed(title="Subscribed Channels")
                for channel_id in channel_ids:
                    embed.add_field(name=channel_id, value=f"[link](https://youtube.com/channel/{channel_id})")
                await i.followup(embed=embed)
        elif option == 2:
            if not record.get("PINGROLE"):
                return await i.followup("> ⚠️ No pingrole set")
            else:
                await i.followup(
                    embed=discohook.Embed(title="Ping Role", description=f"<@&{record['PINGROLE']}>"),
                    ephemeral=True
                )
        elif option == 3:
            if not record.get("RECEPTION"):
                return await i.followup("> ⚠️ No welcomer set", ephemeral=True)
            else:
                embed = discohook.Embed(title="Welcomer")
                embed.description = f"Welcomer bound to <#{record['RECEPTION']}>"
                try:
                    card_stream = await drive.get(f"covers/{i.guild_id}_card.png")
                except deta.NotFound:
                    card_stream = await drive.get("covers/default_card.png")
                card_data = await card_stream.read()
                embed.image("attachment://welcome_card.png")
                file = discohook.File("welcome_card.png", content=io.BytesIO(card_data))
                await i.followup(embed=embed, file=file, ephemeral=True)


def setup(client: discohook.Client):
    client.add_commands(overview)
