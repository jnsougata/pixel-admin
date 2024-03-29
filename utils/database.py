import os
import deta


service = deta.Deta(os.getenv('COLLECTION_KEY'))
base = service.base(os.getenv('BASE_NAME'))
drive = service.drive(os.getenv('DRIVE_NAME'))


def create_ping(data: dict) -> str:
    role_id = data.get('PINGROLE')
    if not (role_id and role_id.isdigit()):
        return ''
    return f'<@&{role_id}>'


def custom_message(data: dict) -> str:
    ping = create_ping(data)
    channel_name = data['channel_name']
    video_url = data['video_url']
    default = (
        f'> <:YouTube:862734568708898856> **{channel_name}** has a new content {ping}\n'
        f'> Go check it out! {video_url}'
    )
    scopes = {'[ping]': ping, '[name]': channel_name, '[url]': video_url}
    data = data.get('CUSTOM')
    if not (data and data.get("youtube")):
        return default
    text = data['youtube']
    if '[url]' not in text:
        text += f'\n{video_url}'
    for key, value in scopes.items():
        text = text.replace(key, value)
    return text
