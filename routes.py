import deta
from deta import Updater

from starlette.requests import Request
from starlette.responses import JSONResponse

from utils.database import base, custom_message


async def subscriptions(request: Request):
    token = request.headers.get("X-Server-Token")
    if not token:
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
    guild_id = token.split('.')[0]
    try:
        data = await base.get(guild_id)
    except deta.NotFound:
        return JSONResponse({"message": "No subscriptions found"}, status_code=404)
    if data and data.get("TOKEN") == token:
        return JSONResponse(data)


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
    published_timestamp = scanned_data['video_published']
    data = await base.get(guild_id)
    if not (data and data.get("TOKEN") == token):
        return JSONResponse({"message": "Unauthorized"}, status_code=401)
    data.update({
        "channel_name": channel_name,
        "video_url": video_url,
    })
    await request.app.send(receiver_id, custom_message(data))
    u = Updater()
    u.set(f'CHANNELS.{channel_id}.last_published', published_timestamp)
    await base.update(guild_id, u)
    return JSONResponse({"message": "Success"}, status_code=200)
