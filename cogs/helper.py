import discohook


@discohook.command(name="help")
async def help_command(i: discohook.Interaction):
    """Get help with the bot."""
    inv = 'https://top.gg/bot/848304171814879273/invite'
    sup = 'https://discord.gg/VE5qRFfmG2'
    uv = 'https://top.gg/bot/848304171814879273/vote'

    view = discohook.View()
    inv_btn = discohook.Button(label='Invite', style=discohook.ButtonStyle.link, url=inv)
    sup_btn = discohook.Button(label='Support', style=discohook.ButtonStyle.link, url=sup)
    uv_btn = discohook.Button(label='Upvote', style=discohook.ButtonStyle.link, url=uv)
    view.add_buttons(inv_btn, sup_btn, uv_btn)

    embed = discohook.Embed(
        title='Commands',
        color=0xc4302b,
        description=(
            f'\n\n1️⃣ </subscribe:1049447008433340540>'
            f'\n● set up the YouTube channel for the server'
            f'\n\n3️⃣ </pingrole:1049447008433340538>'
            f'\n● set up the ping role for the server'
            f'\n\n4️⃣ </dialogue:1049447008433340537>'
            f'\n● set up dialogue for welcomer and feed'
            f'\n\n5️⃣ </remove:1049447008433340539>'
            f'\n● remove a specific option from the server'
            f'\n\n6️⃣ </overview:1112284625579024455>'
            f'\n● check any currently set server config'
            f'\n\n **Note:** Welcomer has been deprecated '
            f'\nand will be removed soon.'
            f'\nTo download the current welcomer card, '
            f'\nuse </overview:1112284625579024455> and click on the image.'
        )
    )
    await i.response.send(embed=embed, view=view)


def setup(app: discohook.Client):
    app.add_commands(help_command)
