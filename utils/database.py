import os
import deta
from deta import NotFound, Updater


service = deta.Deta(os.getenv('COLLECTION_KEY'))
db = service.base(os.getenv('BASE_NAME'))
drive = service.drive(os.getenv('DRIVE_NAME'))


async def get_subscriptions(guild_id: str):
    try:
        return await db.get(guild_id)
    except NotFound:
        return None

async def update_subscriptions(guild_id: str, updater: Updater):
    await db.update(guild_id, updater)