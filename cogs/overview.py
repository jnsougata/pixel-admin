import deta
import discohook
from utils.database import base, drive


@discohook.command(
    options=[
        discohook.IntegerOption(
            "option",
            "the option to check",
            required=True,
            choices=[
                discohook.Choice(name="YouTube", value=1),
                discohook.Choice(name="Ping Role", value=2),
                discohook.Choice(name="Welcomer", value=3),
                discohook.Choice(name="Server Token", value=4),
            ]
        ),
    ],
    permissions=[discohook.Permission.manage_guild],
    dm_access=False,
)
async def overview(i: discohook.Interaction, option: int):
    """
    Check any currently set server config.
    """
    await i.response.defer(ephemeral=True)
    try:
        record = await base.get(i.guild_id)
    except deta.NotFound:
        return await i.response.followup("> ⚠️ No Server Config Found")
    else:
        if option == 1:
            if not record.get("CHANNELS"):
                return await i.response.followup("> ⚠️ No channels subscribed")
            else:
                channel_ids = list(record["CHANNELS"].keys())
                embed = discohook.Embed(title="Subscriptions")
                embed.description = "\n".join(
                    [f"[{channel_id}](https://youtube.com/channel/{channel_id})" for channel_id in channel_ids])
                await i.response.followup(embed=embed)
        elif option == 2:
            if not record.get("PINGROLE"):
                return await i.response.followup("> ⚠️ No pingrole set")
            else:
                await i.response.followup(
                    embed=discohook.Embed(
                        title="Ping Role",
                        description=f"<@&{record['PINGROLE']}> is set as pingrole"
                    )
                )
        elif option == 3:
            if not record.get("RECEPTION"):
                return await i.response.followup("> ⚠️ No welcomer set")
            else:
                embed = discohook.Embed(title="Welcomer")
                embed.description = f"Welcomer bound to <#{record['RECEPTION']}>"
                try:
                    card_stream = await drive.get(f"covers/{i.guild_id}_card.png")
                except deta.NotFound:
                    card_stream = await drive.get("covers/default_card.png")
                card_data = await card_stream.read()
                embed.set_image("attachment://welcome_card.png")
                file = discohook.File("welcome_card.png", content=card_data)
                await i.response.followup(embed=embed, file=file)
        elif option == 4:
            if not record.get("TOKEN"):
                return await i.response.followup("> ⚠️ No server token set")
            else:
                await i.response.followup(
                    embed=discohook.Embed(
                        title="Server Token",
                        description=f"```{record['TOKEN']}```"
                    )
                )


def setup(client: discohook.Client):
    client.add_commands(overview)
