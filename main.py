# Please don't touch the code if you don't know!
# All rights reserved to YonatanDEV - yonatanyh (915624756055801896)


import discord, os
from datetime import datetime
from discord import app_commands, utils, Webhook
from discord.ext import commands
import aiohttp
import asyncio
import time
import json

with open('./config.json') as f:
  data = json.load(f)
  print("Welcome to Yonatan Bot! Checking the config.json")
  for c in data['botConfig']:
    os.system('color a')
    os.system('cls')
    if c['guildid'] == '0':
        os.system('color a')
        print("Make Sure the config is right!")
        time.sleep(1)
        print("Exiting...")
        time.sleep(2)
        exit()
    elif c['token'] == 'token':
        os.system('color a')
        print("Make Sure the config is right!")
        time.sleep(1)
        print("Exiting...")
        time.sleep(2)
        exit()
    elif c['ticketscategory'] == '0':
        os.system('color a')
        print("Make Sure the config is right!")
        time.sleep(1)
        print("Exiting...")
        time.sleep(2)
        exit()
    elif c['staffrole'] == '0':
        os.system('color a')
        print("Make Sure the config is right!")
        time.sleep(1)
        print("Exiting...")
        time.sleep(2)
        exit()
    else:
        print("Welcome to Yonatan Bot! Checking the config.json")
        time.sleep(2)
        os.system('cls')
        os.system('color b')
        print('Guild ID: ' + c['guildid'])
        print('Token: ' + c['token'])
        guild_id = c['guildid']
        token = c['token']
        staffrole = c['staffrole']
        ticketscategory = c['ticketscategory']


guildid = int(guild_id)
staffidrole = int(staffrole)
ticketcate = int(ticketscategory)


class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        ticket = utils.get(interaction.guild.text_channels,
                           name=f"ticket--{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}")
        if ticket is not None:
            await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!",
                                                    ephemeral=True)
        else:
            if type(client.ticket_mod) is not discord.Role:
                client.ticket_mod = interaction.guild.get_role(staffrole)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                              send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                                  read_message_history=True),
                client.ticket_mod: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                               send_messages=True, attach_files=True, embed_links=True),
            }
            try:
                category = discord.utils.get(interaction.guild.categories, id=ticketcate)
                channel = await interaction.guild.create_text_channel(
                    name=f"ticket--{interaction.user.name}-{interaction.user.discriminator}", overwrites=overwrites,category=category,
                    reason=f"Ticket for {interaction.user}")
            except:
                return await interaction.response.send_message(
                    "Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral=True)
            await channel.send(f"{client.ticket_mod.mention}, {interaction.user.mention} created a ticket!",
                               view=main())


            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}!",
                                                    ephemeral=True)


class confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red, custom_id="confirm")
    async def confirm_button(self, interaction, button):
        try:
            await interaction.channel.delete()
        except:
            await interaction.response.send_message(
                "Channel deletion failed! Make sure I have `manage_channels` permissions!", ephemeral=True)


class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close")
    async def close(self, interaction, button):
        embed = discord.Embed(title="Are you sure you want to close this ticket?", color=discord.Colour.blurple())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True)


class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.synced = False
        self.added = False
        self.ticket_mod = 1

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=guildid))
            self.synced = True
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.added = True
        print(f"We have logged in as {self.user}.")




client = aclient()
tree = app_commands.CommandTree(client)



@tree.command(guild=discord.Object(id=guildid), name='ticketpanel', description='Launches the ticketing system')
@app_commands.default_permissions(manage_guild=True)
async def ticketing(interaction: discord.Interaction):
    embed = discord.Embed(title="If you need support, click the button below and create a ticket!",
                          color=discord.Colour.blue())
    await interaction.channel.send(embed=embed, view=ticket_launcher())
    await interaction.response.send_message("Ticketing system launched!", ephemeral=True)




@tree.context_menu(name="Open a Ticket", guild=discord.Object(id=guildid))
@app_commands.default_permissions(manage_guild=True)
async def open_ticket_context_menu(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)
    ticket = utils.get(interaction.guild.text_channels,
                       name=f"ticket--{user.name.lower().replace(' ', '-')}-{user.discriminator}")
    if ticket is not None:
        await interaction.followup.send(f"{user.mention} already has a ticket open at {ticket.mention}!",
                                        ephemeral=True)
    else:
        if type(client.ticket_mod) is not discord.Role:
            client.ticket_mod = interaction.guild.get_role(staffrole)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True,
                                              attach_files=True, embed_links=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                              read_message_history=True),
            client.ticket_mod: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                           send_messages=True, attach_files=True, embed_links=True),
        }
        try:
            category = discord.utils.get(interaction.guild.categories, id=ticketcate)
            channel = await interaction.guild.create_text_channel(name=f"ticket--{user.name}-{user.discriminator}",
                                                                  overwrites=overwrites,
                                                                  category=category,
                                                                  reason=f"Ticket for {user}, generated by {interaction.user}")
        except:
            return await interaction.followup.send(
                "Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral=True)
        await channel.send(f"{interaction.user.mention} created a ticket for {user.mention}!", view=main())
        await interaction.followup.send(f"I've opened a ticket for {user.mention} at {channel.mention}!",
                                        ephemeral=True)


@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(error, ephemeral=True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        return await interaction.response.send_message(error, ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred!", ephemeral=True)
        raise error


client.run("MTA0MDMzNTUxMzA1MzMxOTI2OQ.GOwGwP.q2PV1GA7QO4odTEHJ3tg4FEm2fZW25lZXxZkg4")