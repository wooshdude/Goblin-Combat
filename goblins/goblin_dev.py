import asyncio
import discord
from discord.ext import commands, tasks
from os.path import exists
import os
import random

import nest_asyncio

nest_asyncio.apply()

from classes import *
from weapons import items
from drawScreen import *
from bosses import enemies
from boss_screen import drawBoss
from draw_profile import drawProfile, drawInfo
from game_ticks import Game, gameObjs
from spells import spells

# from spells import spells

commandPrefix = 'p!'
client = commands.Bot(command_prefix=commandPrefix, intents=discord.Intents.all())
client.remove_command('help')

# PVP stuff
inProgress = False
partyInvite = []  # keeps track of who is invited to join
combat = []  # pretty sure this is uselsss rn
playing = []  # player objects of both players
turn = False
step = 0

currentTurnAmmount = 0

# PVE stuff
dungeoneers = {}  # keeps track of players in the dungeon
currentBoss = None

dungeonMsg = None


# total list of players
players = {}

# config
with open("../config.json") as file:
    serverData = json.load(file)


@client.event
async def on_ready():
    path_of_the_directory = 'players'
    ext = '.json'
    # loop through the player profiles
    for files in os.listdir(path_of_the_directory):
        if files.endswith(ext):
            files = files.replace(ext, "", 1)  # turn file names into usable discord ID
            print(files)

            player = client.get_user(int(files))  # grabs member object
            try:
                addToDict(player)
            except AttributeError:
                print('user could not be added to dictionary')
        else:
            continue

    print(f'logged in with {client.user.name}')
    await asyncio.sleep(random.randint(1800, 3600))
    summonDungeon.start()


# random dungeon spawn
@tasks.loop(minutes=random.randint(30, 60))
async def summonDungeon():
    global currentBoss
    global dungeoneers
    global dungeonMsg
    try:
        await dungeonMsg.delete()  # if there is already a dungeon spawned, close it
    except:
        pass
    currentBoss = None
    dungeoneers.clear()

    em = discord.Embed(title="The Dungeon has been opened", description="Prepare your party...")

    view = DungeonInvite()

    channel = client.get_channel(serverData['game_channel_id'])
    dungeonMsg = await channel.send(view=view, embed=em)


@client.command()
async def credits(ctx):
    em = discord.Embed(title="Credits", description="Goblin Combat, made by thirdoul Games.")
    em.add_field(name="Game Director", value="wooshdude")
    em.add_field(name="Programmers", value="wooshdude, colin")
    em.add_field(name="Artists", value="wooshdude, jaikuu")
    em.add_field(name="Additional Support", value="JDMC, jamesjamin")
    em.set_footer(text="Thank You!")

    await ctx.channel.send(embed=em)


async def updatePlayerObj(ctx):
    with open(f'players/{ctx.author.id}.json', 'r') as f:
        player = json.load(f)

    players[ctx.author.id].weapon = items[player['weapon']]
    players[ctx.author.id].armor = items[player['armor']]
    players[ctx.author.id].trinket = items[player['trinket']]
    players[ctx.author.id].update()


# check if player has been assigned a goblin
async def testPlayer(userID, ctx):
    if exists(f"players/{userID}.json"):
        print('all good')
        return True
    else:
        await ctx.channel.send('You have not joined a Goblin Faction yet!')
        return False


@client.command()
async def music(ctx, ver):
    pass


# manages buttons when choosing a faction
class Factions(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Cave", style=discord.ButtonStyle.green)
    async def cave(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, 'cave', items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Desert", style=discord.ButtonStyle.green)
    async def desert(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, 'desert', items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Forest", style=discord.ButtonStyle.green)
    async def forest(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, 'forest', items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.green)
    async def jungle(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, 'jungle', items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Beach", style=discord.ButtonStyle.green)
    async def beach(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, "beach", items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Plains", style=discord.ButtonStyle.green)
    async def plains(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, 'plains', items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Snow", style=discord.ButtonStyle.green)
    async def snow(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = Player(interaction.user, 1, 'snow', items['unarmed'], items['unarmored'], items['none'])

        await writeToFile(player)

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)


@client.command()
async def login(ctx):
    em = discord.Embed(title=f"Choose a Faction")
    em.set_image(url="https://cdn.discordapp.com/attachments/955018181871812618/1008566922960449626/unknown.png")
    view = Factions()
    await ctx.author.send(ctx.author, embed=em, view=view)


# creates initial player file
async def writeToFile(player):
    newPlayer = {
        "name": player.user.name,
        "faction": player.faction['id'],
        "level": player.level,
        "experience": player.experience,
        "max_hit_points": player.max_hit_points,
        "hit_points": player.hit_points,
        "weapon": "unarmed",
        "armor": "unarmored",
        "trinket": "none",
        "inventory": ["unarmed", "unarmored", "none"],
        "cosmetics": [
            {
                "hat": player.hat,
                "shirt": player.shirt,
                "pants": player.pants
            }
        ]
    }

    if not exists(f'players/{player.user.id}.json'):
        open_file = open(f'players/{player.user.id}.json', 'a')
        open_file.write(json.dumps(newPlayer, indent=4))
        open_file.close()

        await asyncio.sleep(2)
        addToDict(player.user)


# often times always broken
@client.command()
async def test(ctx):
    if await testPlayer(ctx.author.id, ctx):
        weapon = items['the splinter']
        f = open(f'players/{ctx.author.id}.json', 'r')
        player = json.load(f)

        p = open(f'players/{ctx.author.id}.json', 'w')
        player['inventory'].append("the splinter")
        json.dumps(player, p)

        f.close()
        p.close()


# selector buttons that appear on inventory screen
class MenuSelect(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()

    @discord.ui.button(label="Weapons", style=discord.ButtonStyle.gray)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author == interaction.user and await testPlayer(interaction.user.id, interaction):
            await interaction.response.edit_message(view=WeaponSelectView(self.ctx))

    @discord.ui.button(label="Armors", style=discord.ButtonStyle.gray)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author == interaction.user and await testPlayer(interaction.user.id, interaction):
            await interaction.response.edit_message(view=ArmorSelectView(self.ctx))

    @discord.ui.button(label="Trinkets", style=discord.ButtonStyle.gray)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author == interaction.user and await testPlayer(interaction.user.id, interaction):
            await interaction.response.edit_message(view=TrinketSelectView(self.ctx))


# handles selecting a weapon from drop down menu
class WeaponSelect(discord.ui.Select):
    def __init__(self, ctx):
        options = []
        self.ctx = ctx

        with open(f'players/{self.ctx.author.id}.json', 'r') as f:
            player = json.load(f)

        em = discord.Embed(title='Items')
        for i in player['inventory']:
            if isinstance(items[i], Weapon):
                em.add_field(name=items[i].name, value=items[i].desc)
                options.append(discord.SelectOption(label=items[i].name, description=items[i].desc))

        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(f'players/{self.ctx.author.id}.json', 'r') as f:
            player = json.load(f)

        weapon = self.values[0].lower()

        if weapon in player['inventory'] and weapon != player['weapon']:
            with open(f'players/{self.ctx.author.id}.json', 'w') as p:
                player['weapon'] = str(weapon)
                json.dump(player, p)
            await updatePlayerObj(self.ctx)
            em = await profileImg(self.ctx)

            await interaction.response.edit_message(view=MenuSelect(self.ctx), embed=em)
        else:
            await interaction.response.edit_message(view=MenuSelect(self.ctx))


# creates the weapon drop down menu instance
class WeaponSelectView(discord.ui.View):
    def __init__(self, ctx, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(WeaponSelect(ctx))


# handles armor drop down menu
class ArmorSelect(discord.ui.Select):
    def __init__(self, ctx):
        options = []
        self.ctx = ctx

        with open(f'players/{self.ctx.author.id}.json', 'r') as f:
            player = json.load(f)

        em = discord.Embed(title='Items')
        for i in player['inventory']:
            if isinstance(items[i], Armor):
                em.add_field(name=items[i].name, value=items[i].desc)
                options.append(discord.SelectOption(label=items[i].name, description=items[i].desc))

        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(f'players/{self.ctx.author.id}.json', 'r') as f:
            player = json.load(f)

        armor = self.values[0].lower()

        if armor in player['inventory'] and armor != player['armor']:
            with open(f'players/{self.ctx.author.id}.json', 'w') as p:
                player['armor'] = str(armor)
                json.dump(player, p)
            await updatePlayerObj(self.ctx)
            em = await profileImg(self.ctx)
            await interaction.response.edit_message(view=MenuSelect(self.ctx), embed=em)
        else:
            await interaction.response.edit_message(view=MenuSelect(self.ctx))


# creates the armor dropdown menu instance
class ArmorSelectView(discord.ui.View):
    def __init__(self, ctx, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ArmorSelect(ctx))


# handles trinket dropdown menu
class TrinketSelect(discord.ui.Select):
    def __init__(self, ctx):
        options = []
        self.ctx = ctx

        with open(f'players/{self.ctx.author.id}.json', 'r') as f:
            player = json.load(f)

        em = discord.Embed(title='Items')
        for i in player['inventory']:
            if isinstance(items[i], Trinket):
                em.add_field(name=items[i].name, value=items[i].desc)
                options.append(discord.SelectOption(label=items[i].name, description=items[i].desc))

        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(f'players/{self.ctx.author.id}.json', 'r') as f:
            player = json.load(f)

        trinket = self.values[0].lower()

        if trinket in player['inventory'] and trinket != player['trinket']:
            with open(f'players/{self.ctx.author.id}.json', 'w') as p:
                player['trinket'] = str(trinket)
                json.dump(player, p)
            await updatePlayerObj(self.ctx)
            em = await profileImg(self.ctx)
            await interaction.response.edit_message(view=MenuSelect(self.ctx), embed=em)
        else:
            await interaction.response.edit_message(view=MenuSelect(self.ctx))


# creates trinket dropdown instance
class TrinketSelectView(discord.ui.View):
    def __init__(self, ctx, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(TrinketSelect(ctx))


# handles drawing user profile image
async def profileImg(ctx):
    drawProfile(players[ctx.author.id], ctx.author.avatar.url)
    prof = discord.Embed(color=discord.colour.Color.dark_purple())
    file = discord.File("profile-export.png")
    img = await client.get_channel(int(serverData['screen_updates_id'])).send(file=file)
    prof.set_image(url=img.attachments[0].url)

    return prof


# handles drawing user profile image
async def infoImg(item, type):
    em = discord.Embed(title=item.name, description=item.desc)

    if type == "weapon":
        em.add_field(name="Stats", value=f"ATK {item.attack}\n"
                                         f"MGK {item.magic}\n"
                                         f"SPD {item.speed}")
        if item.special is not None:
            em.add_field(name=item.special.name, value=item.special.desc)

    elif type == "armor":
        em.add_field(name="Stats", value=f"DEF {item.defence}\n"
                                         f"HP {item.health}\n"
                                         f"MGK {item.magic}\n")
        #if item.special.name is not None:
        #    pass
            #em.add_field(name=item.special.name, value=item.special.desc)

    elif type == 'trinket':
        em.add_field(name="Stats", value=f"ATK {item.attack}\n"
                                         f"DEF {item.magic}\ "
                                         f"HP {item.magic}\n"
                                         f"MGK {item.magic}\n")
        if item.special is not None:
            em.add_field(name=item.special.name, value=item.special.desc)

    drawInfo(item, type)
    file = discord.File(f"item-enlarge.png")
    img = await client.get_channel(int(serverData['screen_updates_id'])).send(file=file)
    em.set_thumbnail(url=img.attachments[0].url)

    return em


# draws player inventory and sends to chat
@client.command()
async def menu(ctx):
    if await testPlayer(ctx.author.id, ctx):
        await ctx.send(embed=await profileImg(ctx), view=MenuSelect(ctx))


# selector buttons that appear on inventory screen
class InfoSelect(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()

    @discord.ui.button(label="Weapon", style=discord.ButtonStyle.gray)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author == interaction.user and await testPlayer(interaction.user.id, interaction):
            player = players[interaction.user.id]
            await interaction.response.edit_message(view=self, embed=await infoImg(player.weapon, "weapon"))

    @discord.ui.button(label="Armor", style=discord.ButtonStyle.gray)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author == interaction.user and await testPlayer(interaction.user.id, interaction):
            player = players[interaction.user.id]
            await interaction.response.edit_message(view=self, embed=await infoImg(player.armor, "armor"))

    @discord.ui.button(label="Trinket", style=discord.ButtonStyle.gray)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.ctx.author == interaction.user and await testPlayer(interaction.user.id, interaction):
            player = players[interaction.user.id]
            await interaction.response.edit_message(view=self, embed=await infoImg(player.trinket, "trinket"))


@client.command()
async def info(ctx):
    if await testPlayer(ctx.author.id, ctx):
        await ctx.send(embed=await infoImg(players[ctx.author.id].weapon, "weapon"), view=InfoSelect(ctx))


# does nothing and probably never will again
@client.group(invoke_without_command=True)
async def equip(ctx, *, weapon):
    if await testPlayer(ctx.author.id, ctx):
        weapon = weapon.lower()
        f = open(f'players/{ctx.author.id}.json', 'r')
        player = json.load(f)

        p = open(f'players/{ctx.author.id}.json', 'w')
        if weapon in player['inventory']:
            player['weapon'] = str(weapon)
            json.dumps(player, p)
        else:
            await ctx.channel.send("You don't own that item!")

        f.close()
        p.close()


# does nothing but might soon
# could be an easier way to display a users pockets
@equip.command()
async def listItems(ctx):
    if await testPlayer(ctx.author.id, ctx):
        f = open(f'players/{ctx.author.id}.json', 'r')
        player = json.load(f)
        em = discord.Embed(title='Items')
        for i in player['inventory']:
            em.add_field(name=items[i].name, value=items[i].desc)

        await ctx.channel.send(embed=em)


# chooses a random item from list of items
def giveRandomItem():
    item = random.choice(list(items))

    return item


# creates the player object based on player profile.json
def addToDict(player):
    print(player.name)

    if player.id not in players.keys():
        f = open(f'players/{player.id}.json')
        data = json.load(f)
        players[player.id] = Player(player, data['level'], data['faction'], items[data['weapon'].lower()], items[data['armor'].lower()], items[data['trinket'].lower()])
    else:
        print('player already added to dictionary')


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

            em = discord.Embed(title=f"{interaction.user.name} has accepted the invitation")

            await interaction.response.edit_message(view=StartPVP(), embed=em)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f'{interaction.user} declined invitation')
        if partyInvite[1] == interaction.user:
            combat.clear()
            button.disabled = True
            for child in self.children:
                child.disabled = True

            em = discord.Embed(title=f"{interaction.user.name} has accepted the invitation")

            await interaction.response.edit_message(view=self, embed=em)


class StartPVP(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f'added {interaction.user.name} to party')
        if partyInvite[1] == interaction.user and await testPlayer(interaction.user.id, interaction):
            global inProgress
            if interaction.user in combat and inProgress == False and await testPlayer(interaction.user.id,
                                                                                       interaction):
                await firstScreen(interaction)
            elif inProgress:
                await interaction.channel.send(
                    'Someone has already been challenged to Goblin Combat. Sit back and enjoy the show!')
            elif interaction.user not in combat:
                await interaction.channel.send('You have not been invited to Goblin Combat. Sucks to be you!')

            em = discord.Embed(title=f"{interaction.user.name} has accepted the invitation")

            await interaction.response.edit_message(view=self, embed=em)


# invite logic
@client.command()
async def invite(ctx, member: discord.Member):
    if await testPlayer(ctx.author.id, ctx) and ctx.author != member:
        em = discord.Embed(title=f"{member.name}'s Goblin Combat Invite",
                           description=f"You've been invited to Goblin Combat by {ctx.author.name}!")
        playing.append(players[ctx.author.id])  # adds player oject to array
        combat.append(ctx.author)  # adds player id to list of combatants
        partyInvite.append(ctx.author)  # adds player user object to list of party members
        partyInvite.append(member)  # used to test accept and decline buttons
        view = Invite()
        await ctx.channel.send(embed=em, view=view)
        print(f'Invited {member.name} to Goblin Combat!')
    else:
        await ctx.channel.send("You can't invite yourself!")


# draws user profile and sends to chat
@client.command()
async def profile(ctx):
    if await testPlayer(ctx.author.id, ctx):
        await ctx.send(embed=await profileImg(ctx), view=MenuSelect(ctx))





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


# handles dungeon invite message and buttons
class DungeonInvite(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # self.children[1].disabled = True

    @discord.ui.button(label="Enter", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if testPlayer:
            dungeoneers[interaction.user.id] = players[interaction.user.id]
            print(f'{interaction.user.name} has entered the dungeon')
            await interaction.response.send_message(f"{interaction.user.name} has joined the dungeon")

    @discord.ui.button(label="Start", style=discord.ButtonStyle.gray)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if testPlayer and dungeoneers[interaction.user.id] and currentBoss is None:
            for i in dungeoneers:
                dungeoneers[i].restore()
            await startBoss()
            button.label = 'Join'
            em = discord.Embed(title="A Team has Entered the Dungeon!", description="Join the hunt...")
            await interaction.response.edit_message(view=self, embed=em)

        elif testPlayer and dungeoneers[interaction.user.id] and currentBoss is not None:
            dungeoneers[interaction.user.id].restore()
            em, img = await bossFight()
            view = BossButtons(interaction.user)
            await interaction.user.send(view=view, embed=em)


# manual summon command, only usable by devs
@client.command()
async def summon(ctx):
    devs = [176820746725752842, 228586830486962177]
    if ctx.author.id in devs:
        em = discord.Embed(title="The Dungeon has been opened", description="Prepare your party...")

        view = DungeonInvite()

        global dungeonMsg
        dungeonMsg = await ctx.channel.send(view=view, embed=em)
    else:
        await ctx.channel.send("You cannot summon a dungeon")


# handles buttons on boss screen seen in user DMs
class BossButtons(discord.ui.View):
    def __init__(self, usr):
        self.usr = usr
        super().__init__(timeout=None)

        with open(f"factions/{players[self.usr.id].faction['id']}.json") as f:
            faction = json.load(f)

        self.children[1].label = faction['spells'][0]['name']
        self.children[2].label = faction['spells'][1]['name']

    @discord.ui.button(label="Melee", style=discord.ButtonStyle.red)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if testPlayer and dungeoneers[interaction.user.id] and not dungeoneers[interaction.user.id].testHealth():
            await dungeoneers[interaction.user.id].melee(currentBoss)
            await testBossHealth()

            # controls button cooldown
            # local to player DMs
            button.disabled = True
            em, img = await bossFight()
            em.set_footer(
                text=f'HP: {dungeoneers[interaction.user.id].hit_points}, ATK: {dungeoneers[interaction.user.id].attack}')
            await interaction.response.edit_message(view=self, embed=em)
            await asyncio.sleep(players[interaction.user.id].weapon.speed)
            button.disabled = False
            await players[interaction.user.id].screen.edit(view=self)

    @discord.ui.button(label=f"Magic 1", style=discord.ButtonStyle.green)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if testPlayer and dungeoneers[interaction.user.id] and not dungeoneers[interaction.user.id].testHealth():
            # gets players faction spell data
            with open(f"factions/{players[self.usr.id].faction['id']}.json") as f:
                faction = json.load(f)
            spell = spells[faction['spells'][0]['name'].lower()]
            await spell.activate(dungeoneers[interaction.user.id], dungeoneers, currentBoss)
            await testBossHealth()

            # controls button cooldown
            # local to player DMs
            button.disabled = True
            em, img = await bossFight()
            em.set_footer(
                text=f'HP: {dungeoneers[interaction.user.id].hit_points}, ATK: {dungeoneers[interaction.user.id].attack}')
            await interaction.response.edit_message(view=self, embed=em)
            await asyncio.sleep(faction['spells'][0]['cooldown'])
            button.disabled = False
            await players[interaction.user.id].screen.edit(view=self)

    @discord.ui.button(label=f"Magic 2", style=discord.ButtonStyle.green)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if testPlayer and dungeoneers[interaction.user.id] and not dungeoneers[interaction.user.id].testHealth():
            # gets players faction spell data
            with open(f"factions/{players[self.usr.id].faction['id']}.json") as f:
                faction = json.load(f)
            spell = spells[faction['spells'][1]['name'].lower()]
            await spell.activate(dungeoneers[interaction.user.id], dungeoneers, currentBoss)

            # controls button cooldown
            # local to player DMs
            button.disabled = True
            em, img = await bossFight()
            em.set_footer(
                text=f'HP: {dungeoneers[interaction.user.id].hit_points}, ATK: {dungeoneers[interaction.user.id].attack}')
            await interaction.response.edit_message(view=self, embed=em)
            await asyncio.sleep(faction['spells'][1]['cooldown'])
            button.disabled = False
            await players[interaction.user.id].screen.edit(view=self)


async def startBoss():
    global currentBoss
    currentBoss = randBoss()
    currentBoss.health = currentBoss.max_health
    em, img = await bossFight()

    for i in dungeoneers:
        usr = client.get_user(i)
        view = BossButtons(usr)
        em.set_footer(text=f'HP: {dungeoneers[i].hit_points}, ATK: {dungeoneers[i].attack}')
        screen = await usr.send(view=view, embed=em)
        dungeoneers[i].setScreen(screen)
        gameObjs.append(dungeoneers[i].trinket.special)

    bossAttack.start()
    Game()


@tasks.loop(seconds=random.randint(5, 15))
async def bossAttack():
    try:
        randPlayer = random.choice(list(dungeoneers))
        dungeoneers[randPlayer].takeDamage(currentBoss)
        em, img = await bossFight()
        if not dungeoneers[randPlayer].testHealth():
            em.set_footer(text=f'HP: {dungeoneers[randPlayer].hit_points}, ATK: {dungeoneers[randPlayer].attack}')
            await dungeoneers[randPlayer].screen.edit(embed=em)
    except:
        pass


def randBoss():
    boss = random.choice(list(enemies))
    print(boss)

    return enemies[boss]


async def bossFight():
    em = discord.Embed(title=f"The Dungeon", color=discord.colour.Color.dark_purple())

    drawBoss(currentBoss)
    file = discord.File("boss-screen-export.png")
    img = await client.get_channel(int(serverData['screen_updates_id'])).send(file=file)
    em.set_image(url=img.attachments[0].url)

    return em, file


async def testBossHealth():
    global currentBoss
    if currentBoss.health <= 0:
        print(f'{currentBoss.name} has been slain')
        bossAttack.stop()

        em, img = await bossFight()
        for i in dungeoneers:
            em.description = f'{currentBoss.name} has been slain!'
            await dungeoneers[i].screen.edit(embed=em)
            rewards(i)
            dungeoneers[i].restore()

            await dungeonMsg.delete()

        dungeoneers.clear()
        currentBoss = None
        return True
    else:
        return False


def rewards(i):
    with open(f'players/{i}.json', 'r') as f:
        player = json.load(f)

    p = open(f'players/{i}.json', 'w')
    randItem = giveRandomItem()
    if randItem not in list(player['inventory']):
        player['inventory'].append(randItem)
        json.dump(player, p)
    else:
        print('player already has item')
        json.dump(player, p)
    p.close()

    dungeoneers[i].levelUp(120)
    dungeoneers[i].update()


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
            # for child in self.children:
            #    child.disabled = True
            # await interaction.response.edit_message(view=self)

            playing[not turnListNum[turn]].hit_points -= playing[turnListNum[turn]].attack

            em, img = await drawTheScreen()

            if playing[not turnListNum[turn]].hit_points <= 0:
                await endWithWinner(playing[turnListNum[turn]], self, interaction, button)
            else:
                await interaction.response.edit_message(embed=em)

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
                await interaction.response.edit_message(embed=em)

            await runGameTick()

    @discord.ui.button(label="Run", style=discord.ButtonStyle.gray)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        global turn
        global inProgress
        global step
        em = discord.Embed(title=f"{interaction.user.name} has fled", description="The battle has ended")
        stopGame()

        button.disabled = True
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self, embed=em)


async def drawTheScreen():
    em = discord.Embed(title=f"Goblin Combat", color=discord.colour.Color.green())
    em.add_field(name=f'{playing[0].user.name} Health', value=f'{playing[0].hit_points}')
    em.add_field(name=f'{playing[1].user.name} Health', value=f'{playing[1].hit_points}')

    global step
    turnList, turnListNum = await calcTurns()

    em.set_footer(text=f"{playing[turnListNum[step]].user.name}")

    draw(playing[0], playing[1])
    file = discord.File("final.png")
    img = await client.get_channel(int(serverData['screen_updates_id'])).send(file=file)
    em.set_image(url=img.attachments[0].url)

    return em, file


# sends first message with embed to be updated
async def firstScreen(ctx):
    global inProgress
    global turn
    global step

    step = 1

    player_order, turn_amount = await calcSpeed()
    turn = player_order

    em, img = await drawTheScreen()
    turnList, turnListNum = await calcTurns()
    em.set_footer(text=f"{playing[turnListNum[step - 1]].user.name}")

    view = Actions()

    await ctx.channel.send(embed=em, view=view)
    inProgress = True


async def calcTurns():
    player_order, turn_amount = await calcSpeed()
    turnList = []
    turnListNum = []
    for i in range(0, turn_amount + 1):
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

    if step >= len(turnList) - 1:
        step = 0
    else:
        step += 1


async def calcSpeed():
    if playing[0].speed > (playing[1].speed):
        for i in range(0, 5):
            if playing[0].speed / playing[1].speed >= i:
                numTurns = i

            else:
                return 0, numTurns
        turn_total = numTurns + 1
    elif playing[1].speed > (playing[0].speed):
        for i in range(0, 5):
            if playing[1].speed / playing[0].speed >= i:
                numTurns = i

            else:
                return 1, numTurns
        turn_total = numTurns + 1
    else:
        return 0, 0


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

    em = discord.Embed(title=f"{player.user.name} has won the duel!", description=f"The game has ended.")

    button.disabled = True
    for child in game.children:
        child.disabled = True

    await interaction.response.edit_message(view=game, embed=em)


# all the help options
@client.group(invoke_without_command=True, aliases=['?'])
async def help(ctx):
    em = discord.Embed(title='Help', description=f"Use {commandPrefix}help <command> for more info.", color=0x1abc9c)

    em.add_field(name='PVP', value='invite, stop')
    em.add_field(name='Users', value='login, profile, menu')

    await ctx.send(embed=em)


# @help.command()
# async def start(ctx):
#     em = discord.Embed(title = 'start', description = 'Starts a new game of Goblin Combat! Both members but be partied up using g!invite.', color = 0x1abc9c)
#     em.add_field(name = '**Syntax**', value=f'{commandPrefix}start')
#
#     await ctx.send(embed=em)


@help.command()
async def guess(ctx):
    em = discord.Embed(title='invite', description='Invite your competetor to a match of Goblin Combat.',
                       color=0x1abc9c)
    em.add_field(name='**Syntax**', value=f'{commandPrefix}invite @<user>')

    await ctx.send(embed=em)


@help.command()
async def stop(ctx):
    em = discord.Embed(title='stop', description='Stops the current game.', color=0x1abc9c)
    em.add_field(name='**Syntax**', value=f'{commandPrefix}stop')

    await ctx.send(embed=em)


@help.command()
async def profile(ctx):
    em = discord.Embed(title='profile', description='View your Goblin stats!', color=0x1abc9c)
    em.add_field(name='**Syntax**', value=f'{commandPrefix}profile')

    await ctx.send(embed=em)


@help.command()
async def menu(ctx):
    em = discord.Embed(title='menu', description='View your Goblin stats!', color=0x1abc9c)
    em.add_field(name='**Syntax**', value=f'{commandPrefix}profile')

    await ctx.send(embed=em)


try:
    client.run(serverData['server_id'])
except:
    print('Unauthorized key. Please double check you have the correct key.')


# prospero
# client.run(f"OTE4Nzg0MzI3NzY3MTkxNTcy.GDJgQn.K3jTzQc2eyeSHxNM86nSNaQGFTm2TDzz8_6fXg")

# goblin proctor
# client.run("OTQyODc0MjExNjgzMjcwNjY2.G-r-vD.Vs6I9KQIxqSRL5c14v5Jbzk2Sw4s-_LHLPAhNE")