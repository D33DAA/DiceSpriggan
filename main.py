try:
    import discord, random, logging, asyncio
except:
    input("Some modules don't appear to be in place.\nPress Enter to exit.")
    quit()

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
    diceNumber = int(content.split("d")[0])
    diceRemain = content.split("d")[1]
    diceSide = 0
    diceMod = 0
    diceOperator = 0

    if diceNumber == 0:
        errorCode = "Is {0} is want spriggy roll dice with no dice? ... Jig?\n```The spriggan is confused. You cannot roll zero dice.```"
        return errorCode.format(sender)
    
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

    if diceSide == 0:
        errorCode = "Is {0} is want spriggy is roll dice with no SIDES?! Is Spriggy is LOSE DICE? WHERE IS DICE?! **AAAAIIEEEEEE!!**\n```The spriggan is confused. You cannot roll a dice with no sides.```"
        return errorCode.format(sender)

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
        diceMessage = "{0} rolls: `{1}`*{2}{3}{4}* (**{5}**)"
        output = (diceMessage.format(sender,content,str(diceTotal),diceOperator,str(diceMod),str(diceFinal)))  
    else:
        diceFinal = sum(diceTotal)
        diceMessage = "{0} rolls: `{1}`*{2}* (**{3}**)"
        output = diceMessage.format(sender,content,str(diceTotal),str(diceFinal))
    
    return output

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
            output += ("\nThere have been "+str(jigs)+" jigs since last restart.")
        await client.send_message(message.channel,output)
        await client.delete_message(message)
    if message.content == ("/egg"):
        await client.send_message(message.channel,"SHINY EGG! **GIVE TO SPRIGGY!!**")
    if message.content == ("/help") or message.content == ("/?"):
        await client.send_message(message.channel,
            '''```DiceSpriggan Commands:
===========
/help /? - display this menu
/jig - Jig!
/roll 1d20 /r 1d20 - rolls a 20-sided dice. accepts modifiers and multiple dice
/egg - we don't talk about eggs here...```''')
        await client.delete_message(message)

jigs = 0
with open("client key.txt", "r") as f:
    key = f.readline().strip("\n")
client.run(key)
