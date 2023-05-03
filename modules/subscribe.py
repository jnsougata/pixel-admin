import re
import deta
import aiohttp
import discohook as dh
from utils.db import db
from datetime import datetime


def form_id(url: str) -> str:
    pattern = re.compile("UC(.+)|c/(.+)|@(.+)")
    results = pattern.findall(url)
    if not results:
        return url
    elif results[0][0]:
        return 'UC' + results[0][0]
    elif results[0][1]:
        return results[0][1]
    elif results[0][2]:
        return '@' + results[0][2]


async def fetch_channel(channel_id: str) -> dict:
    url = f"https://aiotube.deta.dev/channel/{channel_id}/info"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()


@dh.command(
    name="subscribe",
    description="subscribe to a youtube feed",
    options=[
        dh.StringOption("url", "the url of the youtube channel", required=True),
        dh.ChannelOption(
            "channel",
            "the channel to send the updates to",
            required=True,
            channel_types=[dh.ChannelType.guild_text]
        ),
    ],
    permissions=[dh.Permissions.manage_guild],
    dm_access=False,
)
async def subscribe(i: dh.Interaction, url: str, channel: dh.Channel):
    await i.defer(ephemeral=True)
    channel_info = await fetch_channel(form_id(url))
    if not channel_info:
        return await i.followup("Invalid channel url", ephemeral=True)
    channel_id = channel_info["id"]
    existing = await db.get(i.guild_id)
    if existing:
        if existing[0].get("CHANNELS") and len(existing[0]["CHANNELS"]) >= 10:
            await i.followup("> ⚠️ Max subscription limit reached!")
            return
        elif not existing[0].get("CHANNELS"):
            updater = deta.Updater()
            updater.set(
                "CHANNELS",
                {
                    channel_id: {
                        'receiver': channel_id,
                        'last_published': str(int(datetime.utcnow().timestamp()))
                    }
                }
            )
            await db.update(i.guild_id, updater)
        else:
            updater = deta.Updater()
            updater.set(
                f"CHANNELS.{channel_id}",
                {
                    'receiver': channel.id,
                    'last_published': str(int(datetime.utcnow().timestamp()))
                }
            )
            await db.update(i.guild_id, updater)

    emd = dh.Embed(
        title=channel_info["name"],
        url=channel_info["url"],
        description=(
            f'> ✅ Subscribed Successfully'
            f'\n\n> **Subs:** {channel_info["subscribers"]}\n> **Views:** {channel_info["views"]}'
            f'\n> **Bound to:** <#{channel.id}>'
        ),
        color=0xc4302b
    )
    avatar = channel_info.get("avatar")
    banner = channel_info.get("banner")
    if avatar:
        emd.thumbnail(channel_info["avatar"])
    if banner:
        emd.image(channel_info["banner"])
    await i.followup(embed=emd, ephemeral=True)


def setup(app: dh.Client):
    app.load_commands(subscribe)
