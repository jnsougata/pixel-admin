import os
import traceback
import discohook

app = discohook.Client(
    application_id=os.getenv("APPLICATION_ID"),
    public_key=os.getenv("PUBLIC_KEY"),
    token=os.getenv("DISCORD_TOKEN"),
)

app.load_modules("cogs")


@app.get("/")
async def index():
    return {"message": "PixeL is Online!"}


@app.on_error
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
        await i.followup(embed=embed, ephemeral=True)
    else:
        await i.response(embed=embed, ephemeral=True)
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    embed = discohook.Embed(
        title='Stack Trace', 
        description=f'```py\n{err}\n```', 
        color=0xff0000
    )
    await app.send_message(os.getenv("LOG_CHANNEL_ID"), embed=embed)
