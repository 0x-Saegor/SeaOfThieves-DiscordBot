import discord
from discord import app_commands
from login import discord_token
from discord.ui import Button, View

activeguild = discord.Object(id=1189134965766631476)


class aclient(discord.Client):
    def __init__(self, guild=activeguild):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.guild = guild
    async def on_ready(self):
        await self.wait_until_ready()
        game = discord.Game(f"Sea Of Thieves")
        await self.change_presence(status=discord.Status.online, activity=game)
        if not self.synced:
            await tree.sync(guild=activeguild)
            self.synced = True
        print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="help", description="Help command", guild=activeguild)
async def help(interaction: discord.Interaction):

    button1 = Button(label="Page Suivante", style=discord.ButtonStyle.primary)
    button2 = Button(label="Page Précédente",
                     style=discord.ButtonStyle.primary)

    view_n1 = View()
    view_n1.add_item(button1)

    view_n2 = View()
    view_n2.add_item(button2)

    async def button1_callback(interaction):
        await interaction.response.edit_message(embed=embed2, view=view_n2)

    async def button2_callback(interaction):
        await interaction.response.edit_message(embed=embed, view=view_n1)

    button1.callback = button1_callback
    button2.callback = button2_callback

    embed = discord.Embed(
        title="Menu d'aide - Page 1",
        color=0x5865f2).add_field(
        name="Bannir un membre",
        value="ban 'membre' 'raison'",
        inline=False
    ).add_field(
            name="Exclure un membre",
            value="kick 'membre' 'raison'",
            inline=False
    ).add_field(
            name="Supprimer des messages",
            value="clear 'number'",
            inline=False
    ).add_field(
            name="Assigner un rôle",
            value="assign 'membre' 'role'",
            inline=False
    ).set_footer(text=client.user, icon_url=client.user.avatar.url)

    embed2 = discord.Embed(
        title="Menu d'aide - Page 2",
        color=0x5865f2).add_field(
        name="Désassigner un rôle",
        value="unassign 'membre' 'role'",
        inline=False
    ).add_field(
        name="Avertir un membre",
        value="warn 'membre' 'raison'",
        inline=False
    ).add_field(
        name="Supprime tous les rôles",
        value="clearallroles 'member'",
        inline=False
    ).set_footer(text=client.user, icon_url=client.user.avatar.url)
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await logs.send(f"{interaction.user.name} a utilisé la commande help à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}. ")
    print(f"{interaction.user.name} a utilisé la commande help à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}. ")
    await interaction.response.send_message(embed=embed, view=view_n1)


@tree.command(name="ban", description="Bannir un membre", guild=activeguild)
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    if reason == None:
        reason = "Pas de raison donnée."
    await member.ban(reason=reason)
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await logs.send(f"{interaction.user.name} a utilisé la commande ban sur {member} pour {reason} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    print(f"{interaction.user.name} a utilisé la commande ban sur {member} pour {reason} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await interaction.response.send_message(f"{member.mention} a été banni pour : `{reason}`")

@tree.command(name="kick", description="Exclure un membre", guild=activeguild)
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    if reason == None:
        reason = "Pas de raison donnée."
    await member.kick(reason=reason)
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await logs.send(f"{interaction.user.name} a utilisé la commande kick sur {member} pour {reason} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    print(f"{interaction.user.name} a utilisé la commande kick sur {member} pour {reason} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await interaction.response.send_message(f"{member.mention} a été exclu pour : `{reason}`")


@tree.command(name="clear", description="Supprime des messages", guild=activeguild)
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, number: int):
    authors = {}
    num=0
    async for message in interaction.channel.history(limit=number):
        await message.delete()
        num +=1

    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await logs.send(f"{interaction.user.name} a utilisé la commande clear pour supprimer {num} messages à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    print(f"{interaction.user.name} a utilisé la commande clear pour supprimer {num} messages à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await interaction.response.send_message(f"J'ai bien supprimé **{num}** messages", ephemeral=True)


@tree.command(name="assign", description="Assigne un rôle", guild=activeguild)
@app_commands.checks.has_permissions(manage_roles=True)
async def assign(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    time = interaction.created_at.astimezone()
    try:
        await member.add_roles(role)
        logs = client.get_channel(1191462856546340864)
        await logs.send(f"{interaction.user.name} a utilisé la commande assign pour assigner {role} à {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
        print(f"{interaction.user.name} a utilisé la commande assign pour assigner {role} à {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
        await interaction.response.send_message(f"{member.mention} tu as bien reçu le rôle {role.mention} !")
    except:
        logs = client.get_channel(1191462856546340864)
        time = interaction.created_at.astimezone()
        await logs.send(f"{interaction.user.name} a utilisé la commande assign pour assigner {role} à {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')} (erreur permissions insuffisantes).")
        await interaction.response.send_message(f"Je n'ai pas les permissions pour assigner ce rôle.")


@tree.command(name="unassign", description="Désassigne un rôle", guild=activeguild)
@app_commands.checks.has_permissions(manage_roles=True)
async def unassign(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await logs.send(f"{interaction.user.name} a utilisé la commande unassign pour désassigner {role} à {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    print(f"{interaction.user.name} a utilisé la commande unassign pour désassigner {role} à {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await interaction.response.send_message(f"{role.mention} a bien été enlevé de {member.mention} ")


@tree.command(name="warn", description="Averti un membre", guild=activeguild)
@app_commands.checks.has_permissions(administrator=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):

    embed = discord.Embed(
        title=f"{interaction.user.display_name} a averti {member.display_name}",
        description=f"La raison est : {reason}",
        color=0xAA0000).set_footer(text=f"Merci de ne plus enfreindre les règles.")
    await interaction.response.send_message(embed=embed)

    embed_thesecond = discord.Embed(
        title=f"{interaction.user.display_name} vous a averti",
        description=f"La raison est : {reason}",
        color=0xAA0000).set_footer(text=f"Merci de ne plus enfreindre les règles.")
    await client.create_dm(member)
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await logs.send(f"{interaction.user.name} a utilisé la commande warn sur {member} pour {reason} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    print(f"{interaction.user.name} a utilisé la commande warn sur {member} pour {reason} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await member.send(embed=embed_thesecond)

@tree.command(name="clearallroles", description="Supprime tous les rôles.", guild=activeguild)
@app_commands.checks.has_permissions(manage_roles=True)
async def clearallroles(interaction: discord.Interaction, member: discord.Member):
    everyone = interaction.guild.get_role(1189134965766631476)
    roles = member.roles
    roles.remove(everyone)
    for i in roles:
        try:
            await member.remove_roles(i)
        except:
            print("")
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await interaction.response.send_message(f"J'ai bien supprimé tous les rôles de {member.mention}", ephemeral=True)
    print(f"{interaction.user.name} a utilisé la commande clearallroles sur {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await logs.send(f"{interaction.user.name} a utilisé la commande clearallroles sur {member} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
            
@tree.command(name="nickbot", description="Nick the bot", guild=activeguild)
@app_commands.checks.has_permissions(manage_nicknames=True)
async def nickbot(interaction: discord.Interaction, nick: str):
    logs = client.get_channel(1191462856546340864)
    time = interaction.created_at.astimezone()
    await interaction.guild.me.edit(nick=nick)
    await logs.send(f"{interaction.user.name} a utilisé la commande nickbot pour changer le surnom du bot en {nick} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    print(f"{interaction.user.name} a utilisé la commande nickbot pour changer le surnom du bot en {nick} à {time.strftime('%H:%M:%S')} le {time.strftime('%d/%m/%Y')}.")
    await interaction.response.send_message(f"Mon surnom est maintenant {nick}", ephemeral=True)    
    
            
client.run(discord_token)
