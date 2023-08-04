import deta
import asyncio
import aiohttp
import discohook
from utils.database import db


async def fetch_channel(channel_id: str) -> dict:
    url = f"https://aiotube.deta.dev/channel/{channel_id}/info"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()


channel_select = discohook.Select(
    placeholder="select channel(s) from list",
)


@channel_select.on_interaction()
async def selection_menu(i: discohook.Interaction, values: list):
    await i.response.defer(ephemeral=True)
    updater = deta.Updater()
    for value in values:
        updater.delete(f"CHANNELS.{value}")
    await db.update(i.guild_id, updater)
    await i.response.followup("> ✅ Unsubscribed selected channels(s)")


@discohook.command(
    options=[
        discohook.IntegerOption(
            "option",
            "the option to remove",
            required=True,
            choices=[
                discohook.Choice("YouTube", 1),
                discohook.Choice("Ping Role", 2),
                discohook.Choice("Welcomer", 3),
            ]
        ),
    ],
    permissions=[discohook.Permission.manage_guild],
    dm_access=False,
)
async def remove(i: discohook.Interaction, option: int):
    """
    Remove a previously set option.
    """
    if option == 1:
        try:
            record = await db.get(i.guild_id)
        except deta.NotFound:
            return await i.response.send("> ⚠️ No channels subscribed", ephemeral=True)
        else:
            await i.response.defer(ephemeral=True)
            channel_ids = list(record.get("CHANNELS", {}).keys())
            tasks = [fetch_channel(channel_id) for channel_id in channel_ids]
            channels = await asyncio.gather(*tasks)
            valids = [channel for channel in channels if channel]
            options = [
                discohook.SelectOption(f"{channel['name']} ({channel['id']})", channel['id']) for channel in valids
            ]
            channel_select.options = options
            channel_select.max_values = len(options)

            view = discohook.View()
            view.add_select(channel_select)
            await i.response.followup(view=view)

    elif option == 2:
        await db.put(deta.Record({"PINGROLE": None}, key=i.guild_id))
        await i.response.send("> ✅ Ping Role removed", ephemeral=True)

    elif option == 3:
        await db.put(deta.Record({"RECEPTION": None}, key=i.guild_id))
        await i.response.send("> ✅ Welcomer removed", ephemeral=True)


def setup(app: discohook.Client):
    app.add_commands(remove)
