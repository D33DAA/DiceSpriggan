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

@client.async_event
def dice_roller(message):
    sender = message.author
    content = (message.content).split()[1]
    diceNum = int(content.split("d")[0])
    diceRem = content.split("d")[1]
    diceSide = 0
    diceMod = 0
    diceOpr = 0

    if diceNum == 0:
        yield from client.send_message(message.channel,"Is {0} is want spriggy roll dice with no dice? ... Jig?".format(sender))
        return None
    
    if "+" in diceRem:
        diceSide = int(diceRem.split("+")[0])
        diceMod = int(diceRem.split("+")[1])
        diceOpr = "+"
    elif "-" in diceRem:
        diceSide = int(diceRem.split("-")[0])
        diceMod = int(diceRem.split("-")[1])
        diceOpr = "-"
    elif "*" in diceRem:
        diceSide = int(diceRem.split("*")[0])
        diceMod = int(diceRem.split("*")[1])
        diceOpr = "*"
    elif "/" in diceRem:
        diceSide = int(diceRem.split("/")[0])
        diceMod = int(diceRem.split("/")[1])
        diceOpr = "/"
    else:
        diceSide = int(diceRem)

    if diceSide == 0:
        yield from client.send_message(message.channel,"Is {0} is want spriggy is roll dice with no SIDES?! Is Spriggy is LOSE DICE? WHERE IS DICE?! **AAAAIIEEEEEE!!**".format(sender))
        return None

    diceTotal = []
    for num in range(diceNum):
        diceTotal.append(random.randint(1,diceSide))

    if diceMod != 0:
        if diceOpr == "+":
            diceFinal = sum(diceTotal) + diceMod
        elif diceOpr == "-":
            diceFinal = sum(diceTotal) - diceMod
        elif diceOpr == "*":
            diceFinal = sum(diceTotal) * diceMod
        elif diceOpr == "/":
            diceFinal = sum(diceTotal) / diceMod
            
    diceMessage = "{0}: ```{1}```*{2}{3}{4}* (**{5}**)"
    output = diceMessage.format(sender,content,diceTotal,diceOpr,diceMode,diceFinal)
    return output

@client.async_event
def on_message(message):
    if message.content.startswith("/roll"):
        print(dice_roller(message))
        #yield from client.send_message(message.channel,dice_roller(message))
    if message.content == ("/jig"):
        global jigs
        yield from client.send_message(message.channel,"**Jig!**\nThere have been "+str(jigs)+" jigs since last restart.")
        jigs += 1
    if message.content == ("/egg"):
        yield from client.send_message(message.channel,"SHINY EGG! **GIVE TO SPRIGGY!!**")
    if message.content == ("/help") or message.content == ("/?"):
        yield from client.send_message(message.channel,
            '''```DiceSpriggan Commands:
===========
/help /? - display this menu
/jig - Jig!
/roll 1d20 - rolls a 20-sided dice. accepts modifiers and multiple dice
/egg - we don't talk about eggs here...```''')

jigs = 0
with open("client key.txt", "r") as f:
    key = f.readline().strip("\n")
client.run(key)
