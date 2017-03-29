#DiceSpriggan, a Discord chat bot
#Copyright (C) 2017  George Gale
import discord, random, logging, asyncio, re

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client() 

@client.event
async def dice_roller(message):
    sender = message.author.display_name or message.author.name
    content = (message.content).split()[1]
    #ensure correct syntax via RegEx - <dice>d<sides><opr><mod>
    if not re.search((r"^\d+d\d+[+/*-]{0,1}\d*$"),content):
        errorCode = "... Jig?\n```The spriggan is confused. Please ensure your roll follows the correct syntax.```"
        return errorCode
    
    diceNumber = int(content.split("d")[0])
    diceRemain = content.split("d")[1]
    diceSide = 0
    diceMod = 0
    diceOperator = 0

    if diceNumber < 1:
        errorCode = "Is {0} is want spriggy roll dice with no dice? ... Jig?\n```The spriggan is confused. You cannot roll fewer than one dice.```"
        return errorCode.format(sender)
    if diceNumber > 25:
        errorCode = "***AAAAAIIEEEEEEEEEEEEEE!!!***\n```Now you've scared him. He only has tiny hands. Please don't ask him to roll so many dice.```"
        return errorCode
    
    if "+" in diceRemain:
        diceSide = int(diceRemain.split("+")[0])
        diceMod = int(diceRemain.split("+")[1])
        diceOperator = "+"
    elif "-" in diceRemain:
        diceSide = int(diceRemain.split("-")[0])
        diceMod = int(diceRemain.split("-")[1])
        diceOperator = "-"
    elif "*" in diceRemain:
        diceSide = int(diceRemain.split("*")[0])
        diceMod = int(diceRemain.split("*")[1])
        diceOperator = "*"
    elif "/" in diceRemain:
        diceSide = int(diceRemain.split("/")[0])
        diceMod = int(diceRemain.split("/")[1])
        diceOperator = "/"
    else:
        diceSide = int(diceRemain)
        
    if diceSide == 1:
        errorCode = "Spriggy roll! And roll! And roll! And roll! And roll... and... spriggy... sleepyzzzz...\n```Now you've done it. The non-stop rolling put the spriggan to sleep. Please do not roll spherical dice.```"
        return errorCode
    elif diceSide < 2:
        errorCode = "Is {0} is want spriggy is roll dice with no SIDES?! Is Spriggy is LOSE DICE? WHERE IS DICE?! **AAAAIIEEEEEE!!**\n```The spriggan is confused. You cannot roll a dice with no sides.```"
        return errorCode.format(sender)
    elif diceSide > 1000:
        errorCode = "J-Jig? Jiiiiiiig! ... **JIIIIIIIG!** ...\n```The spriggan struggles to lift the dice. Please roll smaller dice.```"
        return errorCode

    diceTotal = []
    for num in range(diceNumber):
        diceTotal.append(random.randint(1,diceSide))
    
    if diceMod != 0:
        if diceOperator == "+":
            diceFinal = sum(diceTotal) + diceMod
        elif diceOperator == "-":
            diceFinal = sum(diceTotal) - diceMod
        elif diceOperator == "*":
            diceFinal = sum(diceTotal) * diceMod
        elif diceOperator == "/":
            diceFinal = sum(diceTotal) / diceMod
        diceMessage = "{0} rolls: `{1}`\n{2} {3} {4} (**{5}**)"
        output = diceMessage.format(sender,content,diceTotal,diceOperator,diceMod,diceFinal)  
    else:
        diceFinal = sum(diceTotal)
        diceMessage = "{0} rolls: `{1}`\n{2} (**{3}**)"
        output = diceMessage.format(sender,content,diceTotal,diceFinal)
    
    return output

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="with shiny rocks"))

@client.event
async def on_message(message):
    if message.content.startswith("/roll") or message.content.startswith("/r"):
        await client.send_message(message.channel,(await dice_roller(message)))
        await client.delete_message(message)
    if message.content.startswith("/jig"):
        global jigs
        output = "**Jig!**"
        jigs += 1
        if message.content == ("/jig -total"):
            output += ("\nThere have been {0} jigs since last restart.".format(jigs))
        await client.send_message(message.channel,output)
        await client.delete_message(message)
    if message.content == ("/egg"):
        await client.send_message(message.channel,"SHINY EGG! **GIVE TO SPRIGGY!!**")
    if message.content == ("/help") or message.content == ("/?"):
        await client.send_message(message.channel,
            '''```DiceSpriggan Commands:

/help /? - display this menu
/jig - Jig!
/roll /r - rolls a dice. specify number, sides and modifier (example: 1d20+2, 2d6-1, 4d8*2, 2d4/2)
/egg - we don't talk about eggs here...```''')
        await client.delete_message(message)

jigs = 0
with open("client key.txt", "r") as f:
    key = f.readline().strip("\n")
client.run(key)
