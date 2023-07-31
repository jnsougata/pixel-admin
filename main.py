import os
import traceback
import discohook
from fastapi import Request
from fastapi.responses import JSONResponse

from utils.database import get_subscriptions, update_subscriptions
from deta import Updater
from notifier import custom_message

app = discohook.Client(
    application_id=os.getenv("APPLICATION_ID"),
    public_key=os.getenv("PUBLIC_KEY"),
    token=os.getenv("DISCORD_TOKEN"),
    password=os.getenv("APPLICATION_PASSWORD"),
)

app.load_modules("cogs")


@app.get("/")
async def index():
    return {"message": "PixeL is Online!"}


@app.on_error()
async def on_error(i: discohook.Interaction, e: Exception):
    embed = discohook.Embed(
        title='Oops!',
        description=f'Something went wrong!'
                    f'\nTrying again might fix it.'
                    f'\nIf not, please contact the developer.'
                    f'\n\nTo Join Development Server [Click Here](https://discord.gg/ChJbUv7z8V)',
        color=0xff0000
    )
    if i.responded:
        await i.response.followup(embed=embed, ephemeral=True)
    else:
        await i.response.send(embed=embed, ephemeral=True)
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = discohook.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```', 
        color=0xff0000
    )
    await app.send_message(os.getenv("LOG_CHANNEL_ID"), embed=embed)


@app.get("/{guild_id}/subscriptions")
async def subscriptions(guild_id: int):
    return JSONResponse(await get_subscriptions(str(guild_id)))


@app.post("/notify")
async def notify(request: Request):
    data = await request.json()
    guild_id = data["guild_id"]
    subs = await get_subscriptions(guild_id)
    if not subs:
        return JSONResponse({"message": "No subscriptions found"})
    channels = subs.get("CHANNELS", {})
    channel_id = data["channel_id"]
    if not channels.get(channel_id):
        return JSONResponse({"message": "No subscriptions found"})
    channel = channels[channel_id]
    channel_name = channel["channel_name"]
    video_url = data["video_url"]
    receiver = channel["receiver"]
    published_timestamp = int(data['video_published'])
    last_published_timestamp = int(channel.get('last_published', 0))
    if not (published_timestamp > last_published_timestamp):
        return JSONResponse({"message": "No new videos found"})
    u = Updater()
    u.set(f'CHANNELS.{channel_id}.last_published', published_timestamp)
    await update_subscriptions(guild_id, u)
    message = custom_message(guild_id, channel_name, video_url, subs)
    await app.send_message(receiver, message)
