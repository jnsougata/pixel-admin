import deta
import discohook as dh
from utils.db import db

for_welcomer = (
    '[guild.name] will be replaced with name of the Guild'
    '\n[member.name] will be replaced with name of the Member'
    '\n[member.mention] will mention the member inside the embed'
    '\n[ping.member] will ping the member with their welcome card'
)

for_feed = (
    '[ping] will be replaced with Role Ping'
    '\n[url] will be replaced with the Video URL'
    '\n[name] will be replaced with the Channel NAME'
)

class CustomText(dh.Cog):
    
    @dh.Cog.command(
        id="1049447008433340537",
        name="dialogue",
        description="set a custom dialogue for the welcomer and feed",
        options=[
            dh.IntegerOption("option", "the type of dialogue", required=True, choices=[
                dh.Choice("Feed", 1),
                dh.Choice("Welcomer", 2),
            ]),
        ],
        permissions=[dh.Permissions.manage_guild],
        dm_access=False,
    )
    async def dialogue(self, i: dh.CommandInteraction, option: int):
        if option == 1:
            modal = dh.Modal("YouTube Feed Custom Dialogue")
            modal.add_field("Options", "options", default_text=for_feed, style=dh.TextInputFieldLength.long)
            modal.add_field("Cutom Dialogue", "dialogue", required=True, style=dh.TextInputFieldLength.long)

            @modal.onsubmit
            async def submit(m: dh.Interaction, options: str=None, dialogue: str=None):
                record = await db.get(m.guild_id)
                if not record or not record[0].get("CUSTOM"):
                    u = deta.Updater()
                    u.set("CUSTOM", {"youtube": ""})
                    await db.update(m.guild_id, u)

                updater = deta.Updater()
                updater.set("CUSTOM.youtube", dialogue)
                await db.update(m.guild_id, updater)
                embed = dh.Embed(description=f'> ✅ Custom Dialogue set for YouTube Feed\n\n```\n{dialogue}\n```')
                await m.response(embed=embed, ephemeral=True)
                
            await i.send_modal(modal=modal)

        elif option == 2:
            modal = dh.Modal("Welcomer Custom Dialogue")
            modal.add_field("Options", "options", default_text=for_welcomer, style=dh.TextInputFieldLength.long)
            modal.add_field("Cutom Dialogue", "dialogue", required=True, style=dh.TextInputFieldLength.long)

            @modal.onsubmit
            async def submit(m: dh.Interaction, options: str=None, dialogue: str=None):
                record = await db.get(m.guild_id)
                if not record or not record[0].get("CUSTOM"):
                    u = deta.Updater()
                    u.set("CUSTOM", {"welcome": ""})
                    await db.update(m.guild_id, u)

                updater = deta.Updater()
                updater.set("CUSTOM.welcome", dialogue)
                await db.update(m.guild_id, updater)
                embed = dh.Embed(description=f'> ✅ Custom Dialogue set for Welcomer\n\n```\n{dialogue}\n```')
                await m.response(embed=embed, ephemeral=True)

            await i.send_modal(modal=modal)
        
        else:
            await i.response("> ❌ Invalid Option", ephemeral=True)
        

def setup(app: dh.Client):
    app.add_cog(CustomText())
