import os
import traceback
import discohook
from fastapi.responses import RedirectResponse

app = discohook.Client(
    application_id=os.getenv("APPLICATION_ID"),
    public_key=os.getenv("PUBLIC_KEY"),
    token=os.getenv("DISCORD_TOKEN"),
)

app.load_modules("cogs")


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
async def on_error(_, e: Exception):
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = discohook.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```', 
        color=0xff0000
    )
    await app.send_message(os.getenv("LOG_CHANNEL_ID"), embed=embed)
