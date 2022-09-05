from operator import index
import discord
from discord.ext import commands
from classes import *
from weapons import items
from drawScreen import *

commandPrefix = 'g!'
client = commands.Bot(command_prefix=commandPrefix, intents=discord.Intents.all())
client.remove_command('help')

inProgress = False
partyInvite = []
combat = []
playing = []
turn = False
step = 0


currentTurnAmmount = 0

players = {}


# large dungeons
dungeonPlayers = []


@client.event
async def on_ready():
    print('ready to battle')


# check if player has been assigned a goblin
async def testPlayer(userID, ctx):
    try: 
        if players[userID]:
            print('all good')
            return True        
    except:
        await ctx.channel.send('You have not joined a Goblin Faction yet!')
        return False
        


class Factions(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Cave", style=discord.ButtonStyle.green)
    async def cave(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Cave(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Desert", style=discord.ButtonStyle.green)
    async def desert(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Desert(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Forest", style=discord.ButtonStyle.green)
    async def forest(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Forest(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.green)
    async def jungle(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Jungle(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Beach", style=discord.ButtonStyle.green)
    async def beach(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Beach(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)


    @discord.ui.button(label="Plains", style=discord.ButtonStyle.green)
    async def plains(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Plains(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Snow", style=discord.ButtonStyle.green)
    async def snow(self, interaction: discord.Interaction, button: discord.ui.Button):
        players[interaction.user.id] = Player(interaction.user, Snow(), items['unarmed'], items['unarmored'])

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)




@client.command()
async def login(ctx):
    em = discord.Embed(title=f"Choose a Faction")
    view = Factions()
    await ctx.author.send(ctx.author, embed=em, view=view)



@client.command()
async def test(ctx):
    draw('wooshdude', 'Forest')
    file = discord.File("final.png")
    em = discord.Embed()
    em.set_image(url="attachment://final.png")
    await ctx.channel.send(file = file, embed = em)


# handles invites
# invite buttons
class Invite(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f'added {interaction.user.name} to party')
        if partyInvite[1] == interaction.user and await testPlayer(interaction.user.id, interaction):
            combat.append(interaction.user)
            playing.append(players[interaction.user.id])
            button.disabled = True
            for child in self.children:
                child.disabled = True

            em = discord.Embed(title = f"{interaction.user.name} has accepted the invitation")

            await interaction.response.edit_message(view=self, embed=em)


    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f'{interaction.user} declined invitation')
        if partyInvite[1] == interaction.user:
            combat.clear()
            button.disabled = True
            for child in self.children:
                child.disabled = True

            em = discord.Embed(title = f"{interaction.user.name} has accepted the invitation")

            await interaction.response.edit_message(view=self, embed=em)



# invite logic
@client.command()
async def invite(ctx, member: discord.Member):
    if await testPlayer(ctx.author.id, ctx) and ctx.author != member:
        em = discord.Embed(title=f"{member.name}'s Goblin Combat Invite", description=f"You've been invited to Goblin Combat by {ctx.author.name}!")
        playing.append(players[ctx.author.id])  # adds player oject to dictionary
        combat.append(ctx.author)  # adds player id to list of combatants
        partyInvite.append(ctx.author) # adds player user object to list of party members
        partyInvite.append(member)  # used to test accept and decline buttons
        view = Invite()
        await ctx.channel.send(embed=em, view=view)
        print(f'Invited {member.name} to Goblin Combat!')
    else:
        await ctx.channel.send("You can't invite yourself!")


@client.command()
async def profile(ctx):
    if await testPlayer(ctx.author.id, ctx):
        em = discord.Embed(title=f"{ctx.author.name}'s Goblin Stats")
        em.add_field(name="Class", value=players[ctx.author.id].faction.name)
        em.add_field(name="Level", value=players[ctx.author.id].level)
        em.add_field(name="HP", value=players[ctx.author.id].hit_points)
        em.add_field(name="ATK", value=players[ctx.author.id].attack)
        await ctx.channel.send(embed=em)


# starts game
@client.command()
async def start(ctx):
    global inProgress
    if ctx.author in combat and inProgress == False and await testPlayer(ctx.author.id, ctx):
        await firstScreen(ctx)
    elif inProgress == True:
        await ctx.channel.send('Someone has already been challenged to Goblin Combat. Sit back and enjoy the show!')
    elif ctx.author not in combat:
        await ctx.channel.send('You have not been invited to Goblin Combat. Sucks to be you!')


@client.command()
async def stop(ctx):
    await stopGame()
    await ctx.channel.send('Current game has been stopped')


# game buttons
class Actions(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Attack", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        global turn
        print(f'turn {turn}')
        turnList, turnListNum = await calcTurns()
        print(f'id {interaction.user.id} vs {turnList[turn]}')
        if interaction.user.id == turnList[turn]:
            #for child in self.children:
            #    child.disabled = True
            #await interaction.response.edit_message(view=self)

            playing[not turnListNum[turn]].hit_points -= playing[turnListNum[turn]].attack

            em, img = await drawTheScreen()

            if playing[not turnListNum[turn]].hit_points <= 0:
                await endWithWinner(playing[turnListNum[turn]], self, interaction, button)
            else:
                await interaction.response.edit_message(embed = em)

            await runGameTick()

    @discord.ui.button(label="Magic", style=discord.ButtonStyle.green)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        global turn
        turnList, turnListNum = await calcTurns()
        if interaction.user.id == turnList[turn]:
            # for child in self.children:
            #     child.disabled = True

            playing[not turnListNum[turn]].hit_points -= playing[turnListNum[turn]].magic

            em, img = await drawTheScreen()

            if playing[not turnListNum[turn]].hit_points <= 0:
                await endWithWinner(playing[turnListNum[turn]], self, interaction, button)
            else:
                await interaction.response.edit_message(embed = em)

            await runGameTick()

    @discord.ui.button(label="Run", style=discord.ButtonStyle.gray)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        global turn
        global inProgress
        global step
        em = discord.Embed(title = f"{interaction.user.name} has fled", description = "The battle has ended")
        stopGame()

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self, embed = em)


async def drawTheScreen():

    em = discord.Embed(title=f"Goblin Combat", color=discord.colour.Color.green())
    em.add_field(name=f'{playing[0].user.name} Health', value=f'{playing[0].hit_points}')
    em.add_field(name=f'{playing[1].user.name} Health', value=f'{playing[1].hit_points}')

    global step
    turnList, turnListNum = await calcTurns()
    
    em.set_footer(text=f"{playing[turnListNum[step]].user.name}")
        
    draw(playing[0], playing[1])
    file = discord.File("final.png")
    img = await client.get_channel(1001238232094224444).send(file=file)
    em.set_image(url=img.attachments[0].url)

    return em, file


# sends first message with embed to be updated
async def firstScreen(ctx):
    global inProgress
    global turn
    global step

    step = 1

    #if len(await calcTurns()) % 2 == 0:
    #    #print(f'length {len(await calcTurns())}')
    #    step = 0
    #    #print(f'first step {step}')
    #else:
    #    #print(f'length {len(await calcTurns())}')
    #    step = 1
    #    #print(f'first step {step}')


    player_order, turn_amount = await calcSpeed()
    turn = player_order

    em, img = await drawTheScreen()
    turnList, turnListNum = await calcTurns()
    em.set_footer(text=f"{playing[turnListNum[step-1]].user.name}")

    view = Actions()

    await ctx.channel.send(embed=em, view=view)
    inProgress = True

async def calcTurns():
    player_order, turn_amount = await calcSpeed()
    turnList = []
    turnListNum = []
    for i in range(0,turn_amount+1):
        turnList.append(playing[player_order].user.id)
        turnListNum.append(player_order)
        
    if player_order == 0:
        turnList.append(playing[1].user.id)
        turnListNum.append(1)
    else:
        turnList.append(playing[0].user.id)
        turnListNum.append(0)

    return turnList, turnListNum

# the game
async def runGameTick():   
    global turn
    global step
    player_order, turn_amount = await calcSpeed()
    
    turnList, turnListNum = await calcTurns()
    turn = step
    
    print(f'step {step}')

    if step >= len(turnList) -1:
        step = 0
    else:
        step += 1

async def calcSpeed():
    if playing[0].speed > (playing[1].speed):
        for i in range(0,5):
            if playing[0].speed/playing[1].speed >= i:
                numTurns = i
                
            else:
                return 0, numTurns
        turn_total = numTurns+1
    elif playing[1].speed > (playing[0].speed):
        for i in range(0,5):
            if playing[1].speed/playing[0].speed >= i:
                numTurns = i
                
            else:
                return 1, numTurns
        turn_total = numTurns+1
    else: 
        return 0,0
    
async def stopGame():
    global turn
    global inProgress
    global step

    for player in playing:
        print(player.user.name)
        player.restore()

    playing.clear()
    partyInvite.clear()
    combat.clear()
    turn = False
    inProgress = False
    step = 0


async def endWithWinner(player, game, interaction, button):
    await stopGame()

    em = discord.Embed(title = f"{player.user.name} has won the duel!", description = f"The game has ended.")

    button.disabled = True
    for child in game.children:
        child.disabled = True

    await interaction.response.edit_message(view=game, embed = em)


# all the help options
@client.group(invoke_without_command = True, aliases = ['?'])
async def help(ctx):
    em = discord.Embed(title = 'Help', description = f"Use {commandPrefix}help <command> for more info.", color = 0x1abc9c)

    em.add_field(name = 'Game', value = 'start, invite, stop')
    em.add_field(name = 'Users', value = 'login, profile')

    await ctx.send(embed=em)


@help.command()
async def start(ctx):
    em = discord.Embed(title = 'start', description = 'Starts a new game of Goblin Combat! Both members but be partied up using g!invite.', color = 0x1abc9c)
    em.add_field(name = '**Syntax**', value=f'{commandPrefix}start')

    await ctx.send(embed=em)


@help.command()
async def guess(ctx):
    em = discord.Embed(title = 'invite', description = 'Invite your competetor to a match of Goblin Combat.', color = 0x1abc9c)
    em.add_field(name = '**Syntax**', value=f'{commandPrefix}invite @<user>')

    await ctx.send(embed=em)


@help.command()
async def stop(ctx):
    em = discord.Embed(title = 'stop', description = 'Stops the current game.', color = 0x1abc9c)
    em.add_field(name = '**Syntax**', value=f'{commandPrefix}stop')

    await ctx.send(embed=em)


@help.command()
async def profile(ctx):
    em = discord.Embed(title = 'profile', description = 'View your Goblin stats!', color = 0x1abc9c)
    em.add_field(name = '**Syntax**', value=f'{commandPrefix}profile')

    await ctx.send(embed=em)

client.run("OTQyODc0MjExNjgzMjcwNjY2.G-r-vD.Vs6I9KQIxqSRL5c14v5Jbzk2Sw4s-_LHLPAhNE")