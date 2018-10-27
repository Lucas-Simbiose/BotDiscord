import discord
import os

from bot.utils.error_messages import errorMessages
from bot.libs.worker.workers import Workers
from bot import config

workers_collection = Workers(**config.get("mongo", {}))

client = discord.Client()

COLOR = 0X690FC3
MSG_ID = None
MSG_USER = None
ENTRY_CHANNEL = client.get_channel("505587406615871498")

@client.event
async def on_ready():
    print("Your God has arrived!")

@client.event
async def on_message(message):
    if message.content.lower().startswith("!pause"): #When user takes a break
        targeted_channel = client.get_channel("505587406615871498") # entry channel
        msg = message.content.split()
        if not check_right_channel(message.channel, targeted_channel):
            msg = f"{errorMessages[1000]} {message.author.mention}"
            await client.send_message(message.channel, msg)
            return
        elif len(msg) != 2:
            msg = f"{errorMessages[1001]} {message.author.mention}"
            await client.send_message(targeted_channel, msg)
            return
        try:
            time = int(msg[-1])
            await client.send_message(targeted_channel, f"{message.author.mention} will be away for {time} minutes.")
        except ValueError:
            msg = f"{errorMessages[1001]} {message.author.mention}"
            await client.send_message(targeted_channel, msg)
            return

    elif message.content.lower().startswith("!back"): #When user is back from break
        targeted_channel = client.get_channel("505587406615871498")  # entry channel
        if not check_right_channel(message.channel, targeted_channel):
            msg = f"{errorMessages[1000]} {message.author.mention}"
            await client.send_message(message.channel, msg)
            return
        await client.send_message(targeted_channel, f"{message.author.mention} is back.")
        return

    elif message.content.lower().startswith("!hello"): #When user arrives to start working
        targeted_channel = client.get_channel("505587406615871498") # entry channel
        if not check_right_channel(message.channel, targeted_channel):
            msg = f"{errorMessages[1000]} {message.author.mention}"
            await client.send_message(message.channel, msg)
            return
        await client.send_message(targeted_channel, f"Welcome to work {message.author.mention}!")
        return

    elif message.content.lower().startswith("!leaving"): #When user leaves work
        targeted_channel = client.get_channel("505587406615871498")  # entry channel
        if not check_right_channel(message.channel, targeted_channel):
            msg = f"{errorMessages[1000]} {message.author.mention}"
            await client.send_message(message.channel, msg)
            return
        await client.send_message(targeted_channel, f"See you tomorrow {message.author.mention}!")
        return

    # elif message.content.lower().startswith("!remember"): #When user creates an appointment
    #     msg = f"New appointment scheduled for {message.author.mention}."
    #     await client.send_message(message.channel, msg)
    #     return

    elif message.content.lower().startswith("!register"): #When user register himself to the database
        user_ = await client.get_user_info(message.author.id)
        user_ = workers_collection.create_worker(user_)
        if user_['status'] == 'error':
            await client.send_message(message.channel, errorMessages[user_['code']].format(message.author.mention))
            return
        await client.send_message(message.channel, user_['msg'].format(message.author.mention))
        return


    elif message.content.lower().startswith("!roles"): #Show roles
        embed = discord.Embed(
            title = "Choose your fate, soldier!",
            color = COLOR,
            description = "- Developers = 😀\n"
                            "- SlicingDice Devs = 😉\n"
                            "- DB18 = 😎\n"
        )
        botmsg = await client.send_message(message.channel, embed=embed)
        await client.add_reaction(botmsg, "😀")
        await client.add_reaction(botmsg, "😉")
        await client.add_reaction(botmsg, "😎")

        global MSG_ID
        global MSG_USER
        MSG_ID = botmsg.id
        MSG_USER = message.author
        return

@client.event
async def on_member_join(member):
    targeted_channel = client.get_channel("505587406615871498")
    msg = "Welcome {}!".format(member.mention)
    await client.send_message(targeted_channel, msg)

@client.event
async def on_member_remove(member):
    targeted_channel = client.get_channel("505587406615871498")
    msg = "Goodbye {}! It was very nice to work with you.".format(member.mention)
    await client.send_message(targeted_channel, msg)

@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if reaction.emoji == "😀" and msg.id == MSG_ID and user == MSG_USER:
        role = discord.utils.find(lambda r: r.name == "Developers", msg.server.roles)
    elif reaction.emoji == "😉" and msg.id == MSG_ID:
        role = discord.utils.find(lambda r: r.name == "SlicingDice Devs", msg.server.roles)
    elif reaction.emoji == "😎" and msg.id == MSG_ID:
        role = discord.utils.find(lambda r: r.name == "DB18", msg.server.roles)
    await client.add_roles(user, role)



@client.event
async def on_reaction_remove(reaction, user):
    msg = reaction.message
    if reaction.emoji == "😀" and msg.id == MSG_ID and user == MSG_USER:
        role = discord.utils.find(lambda r: r.name == "Developers", msg.server.roles)
    elif reaction.emoji == "😉" and msg.id == MSG_ID:
        role = discord.utils.find(lambda r: r.name == "SlicingDice Devs", msg.server.roles)
    elif reaction.emoji == "😎" and msg.id == MSG_ID:
        role = discord.utils.find(lambda r: r.name == "DB18", msg.server.roles)
    await client.remove_roles(user, role)

def check_right_channel(sent_channel, expected_channel):
    if sent_channel == expected_channel:
        return True
    return False















client.run(config["token"])