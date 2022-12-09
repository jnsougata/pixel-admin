import deta
import discohook as dh
from utils.db import db


class Help(dh.Cog):
    
    @dh.Cog.command(
        id="938724027776761877",
        name="help",
        description="get help with the bot",
    )
    async def help_(self, i: dh.CommandInteraction):
        inv = 'https://top.gg/bot/848304171814879273/invite'
        sup = 'https://discord.gg/VE5qRFfmG2'
        uv = 'https://top.gg/bot/848304171814879273/vote'

        view = dh.View()
        inv_btn = dh.Button(label='Invite', style=dh.ButtonStyle.link, url=inv)
        sup_btn = dh.Button(label='Support', style=dh.ButtonStyle.link, url=sup)
        uv_btn = dh.Button(label='Upvote', style=dh.ButtonStyle.link, url=uv)
        view.add_button_row(inv_btn, sup_btn, uv_btn)

        embed = dh.Embed(
            title='Commands', 
            color=0xc4302b, 
            description = (
                f'\n\n1️⃣ </subscribe:1049447008433340540>'
                f'\n● set up the YouTube channel for the server'
                f'\n\n2️⃣ </welcomer:1049447008433340541>'
                f'\n● set up the welcome message for the server'
                f'\n\n3️⃣ </pingrole:1049447008433340538>'
                f'\n● set up the ping role for the server'
                f'\n\n4️⃣ </dialogue:1049447008433340537>'
                f'\n● set up dialogue for welcomer and feed'
                f'\n\n5️⃣ </remove:1049447008433340539>'
                f'\n● remove a specific option from the server'
                f'\n\n6️⃣ </overview:936634659763286076>'
                f'\n● check any currently set server config'
            )
        )
        await i.response(embed=embed, view=view)
        
        
def setup(app: dh.Client):
    app.add_cog(Help())
