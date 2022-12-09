import os
import traceback
import discohook as dh
from fastapi.responses import RedirectResponse

app = dh.Client(
    application_id=os.getenv("APPLICATION_ID"),
    public_key=os.getenv("PUBLIC_KEY"),
    token=os.getenv("DISCORD_TOKEN"),
    log_channel_id=int(os.getenv("LOG_CHANNEL_ID")),
)

@app.get("/")   
def root():
    return RedirectResponse("https://top.gg/bot/848304171814879273")

@app.get("/policy")
def policy():
    return RedirectResponse("https://verified.gitbook.io/pixel/privacy-policy")

@app.get("/source")
def src():
    return RedirectResponse("https://github.com/jnsougata/pixel")

@app.on_error
async def on_error(e: Exception, _: dict):
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = dh.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```', 
        color=0xff0000
    )
    await app.send_message(app.log_channel_id, {'embeds': [embed.json()]})

cogs = [
    f"cogs.{script[:-3]}" for script in os.listdir("cogs") 
    if script.endswith(".py")
]

app.load_cogs(*cogs)