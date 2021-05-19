import discord
from discord.ext import commands
from cesi import get_notes, get_token
from db import get_db_info, if_exist, open_database
from pdf import pdf

bot = commands.Bot(command_prefix='_')

@bot.event
async def on_ready():
    print("[Discord] Le bot shiba est lancé")

@bot.event
async def on_command_error(ctx, error):
    print("[Discord] %s" % error)
    await ctx.reply("La commande n'existe pas :/")

@bot.command(name="detail")
async def detail(ctx):
    
    if if_exist(ctx.author.id):
        email, password = get_db_info(ctx.author.id)
        get_notes(email, password)
        detail = pdf(email, detailed=True)
        await ctx.reply("je t'envoie ça en privé bg")
        message = "**Voici toutes tes notes bg**\n\n"
        for note in detail:
            message += "%s\n" % note
            if len(message) > 1800:
                await ctx.reply(message)
                message = ""
        await ctx.reply(message)
        
        #await ctx.reply(res)
    else:
        await ctx.reply("jveux pas te vexer mais jte coco pas mon reuf\njtai envoyé un dm pour te connaitre un peu plus")
        await ctx.author.send("salut mek\nfais la commande suivante pour que je puisse te montrer tes notes\n_register email password\nles codes pour me co sur ton ent du cesi qoa\n(remplace email et password par tes codes ent hein)")

@bot.command(name="note")
async def note(ctx):
    
    if if_exist(ctx.author.id):
        email, password = get_db_info(ctx.author.id)
        a,b,c,d,r = get_notes(email, password)
        moyenne = ((a*5+b*4+c*3+d*1)/(a+b+c+d))*4
        await ctx.reply("Tu as %s/20 de moyenne (avec %s rattrapages quand même fais pas le fou)" % (round(moyenne, 2), r))
        #await ctx.reply(get_notes(email, password))
    else:
        await ctx.reply("jveux pas te vexer mais jte coco pas mon reuf\njtai envoyé un dm pour te connaitre un peu plus")
        await ctx.author.send("salut mek\nfais la commande suivante pour que je puisse te montrer tes notes\n_register email password\nles codes pour me co sur ton ent du cesi qoa\n(remplace email et password par tes codes ent hein)")
    
@bot.command(name='register')
async def register(ctx, *args):

    #try:
    email = args[0]
    password = args[1]

    res = get_token(email, password)

    if res != False or res != "error":
        db, cursor = open_database()
        cursor.execute("INSERT INTO discord (email, password, discordid) VALUES ('%s', '%s', '%s')" % (email, password, ctx.author.id))
        db.commit()
        await ctx.reply("nickel c'est bon jme rappelle de toi bg")
    else:
        pass

    #except:
    #    await ctx.reply("alors par contre la commande c'est\n_register email motdepasse")

    
    
    
    


bot.run("ODQxMDkwNzI0ODM2NDA5MzQ0.YJhsxw.Um1KBw2bmpT0D5GL2h9LvNWiUsc")