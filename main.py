import os
import traceback

import deta
import discohook
from fastapi import Request
from fastapi.responses import JSONResponse
from deta import Updater
from notifier import custom_message
from utils.database import db

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
async def on_error(_, e: discohook.GlobalException):
    embed = discohook.Embed(
        title='Oops!',
        description=f'Something went wrong!'
                    f'\nTrying again might fix it.'
                    f'\nIf not, please contact the developer.'
                    f'\n\nTo Join Development Server [Click Here](https://discord.gg/ChJbUv7z8V)',
        color=0xff0000
    )
    if e.interaction.responded:
        await e.interaction.response.followup(embed=embed, ephemeral=True)
    else:
        await e.interaction.response.send(embed=embed, ephemeral=True)
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = discohook.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```', 
        color=0xff0000
    )
    await app.send_message(os.getenv("LOG_CHANNEL_ID"), embed=embed)


@app.get("/subscriptions")
async def subscriptions(request: Request):
    token = request.headers.get("X-Server-Token")
    if not token:
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
    guild_id = token.split('.')[0]
    try:
        data = await db.get(guild_id)
    except deta.NotFound:
        return JSONResponse({"message": "No subscriptions found"}, status_code=404)
    if data and data.get("TOKEN") == token:
        return JSONResponse(data)


@app.post("/notify")
async def notify(request: Request):
    token = request.headers.get("X-Server-Token")
    if not token:
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
    guild_id = token.split('.')[0]
    scanned_data = await request.json()
    channel_name = scanned_data['channel_name']
    video_url = scanned_data['video_url']
    channel_id = scanned_data['channel_id']
    receiver_id = scanned_data['receiver_id']
    published_timestamp = int(scanned_data['video_published'])
    data = await db.get(guild_id)
    if not (data and data.get("TOKEN") == token):
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
    data.update({
        "channel_name": channel_name,
        "video_url": video_url,
    })
    await app.send_message(receiver_id, custom_message(guild_id, data))
    u = Updater()
    u.set(f'CHANNELS.{channel_id}.last_published', published_timestamp)
    await db.update(guild_id, u)
    return JSONResponse({"message": "Success"}, status_code=200)
