def create_ping(guild_id: str, cache: dict) -> str:
    role_id = cache[guild_id].get('PINGROLE')
    if not (role_id and role_id.isdigit()):
        return ''
    return f'<@&{role_id}>'


def custom_message(
    guild_id: str,
    data: dict
) -> str:
    ping = create_ping(guild_id, data)
    channel_name = data['channel_name']
    video_url = data['video_url']
    default = (
        f'> [SPACE] <:YouTube:862734568708898856> **{channel_name}** has a new content {ping}\n'
        f'> Go check it out! {video_url}'
    )
    scopes = {'[ping]': ping, '[name]': channel_name, '[url]': video_url}
    data = data[guild_id].get('CUSTOM')
    if not (data and data.get("youtube")):
        return default
    text = data['youtube']
    if '[url]' not in text:
        text += f'\n{video_url}'
    for key, value in scopes.items():
        text = text.replace(key, value)
    return text
