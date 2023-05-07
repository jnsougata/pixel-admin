import deta
import asyncio
import aiohttp
import discohook
from utils.db import db


async def fetch_channel(channel_id: str) -> dict:
    url = f"https://aiotube.deta.dev/channel/{channel_id}/info"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()


@discohook.command(
    name="remove",
    description="remove a previously set option",
    options=[
        discohook.IntegerOption(
            "option",
            "the option to remove",
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
async def remove(i: discohook.Interaction, option: int):
    if option == 1:
        record = await db.get(i.guild_id)
        if not record or not record[0].get("CHANNELS"):
            return await i.response("> ⚠️ No channels subscribed", ephemeral=True)
        await i.defer(ephemeral=True)
        channel_ids = list(record[0]["CHANNELS"].keys())
        tasks = [fetch_channel(channel_id) for channel_id in channel_ids]
        channels = await asyncio.gather(*tasks)
        valids = [channel for channel in channels if channel]
        channel_menu = discohook.Select(
            options=[discohook.SelectOption(channel["name"], channel["id"]) for channel in valids],
            max_values=len(valids),
            placeholder="select channel(s) from list",
        )

        @channel_menu.on_interaction
        async def selection_menu(ci: discohook.ComponentInteraction, values: list):
            updater = deta.Updater()
            for value in values:
                updater.delete(f"CHANNELS.{value}")
            await db.update(ci.guild_id, updater)
            await ci.update_message("> ✅ Unsubscribed selected channels(s)", view=None, embed=None)

        view = discohook.View()
        view.add_select_menu(channel_menu)
        await i.followup(view=view)

    elif option == 2:
        await db.put(deta.Record({"PINGROLE": None}, key=i.guild_id))
        await i.response("> ✅ PingRole removed", ephemeral=True)

    elif option == 3:
        await db.put(deta.Record({"RECEPTION": None}, key=i.guild_id))
        await i.response("> ✅ Welcomer removed", ephemeral=True)


def setup(app: discohook.Client):
    app.add_commands(remove)
