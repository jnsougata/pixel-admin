import re
import deta
import aiohttp
import discohook
from utils.database import db
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


@discohook.command(
    name="subscribe",
    description="subscribe to a youtube feed",
    options=[
        discohook.ChannelOption(
            "channel",
            "text channel to send the updates to",
            required=True,
            channel_types=[
                discohook.ChannelType.guild_text,
                discohook.ChannelType.guild_news
            ]
        ),
        discohook.StringOption("url", "youtube channel url", required=True),
    ],
    permissions=[discohook.Permissions.manage_guild],
    dm_access=False,
)
async def subscribe(i: discohook.Interaction, url: str, channel: discohook.Channel):
    await i.defer(ephemeral=True)
    channel_info = await fetch_channel(form_id(url))
    if not channel_info:
        return await i.followup("Invalid channel url", ephemeral=True)
    channel_id = channel_info["id"]
    try:
        record = await db.get(i.guild_id)
    except deta.NotFound:
        await db.put(deta.Record({"CHANNELS": {}}, key=i.guild_id))
        record = {"CHANNELS": {}}
    if record.get("CHANNELS") and len(record["CHANNELS"]) >= 10:
        return await i.followup("> ⚠️ Max subscription limit reached!")
    elif not record.get("CHANNELS"):
        updater = deta.Updater()
        updater.set(
            "CHANNELS",
            {
                channel_id: {
                    'receiver': channel.id,
                    'last_published': str(int(datetime.utcnow().timestamp()))
                }
            }
        )
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

    emd = discohook.Embed(
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


def setup(app: discohook.Client):
    app.add_commands(subscribe)
