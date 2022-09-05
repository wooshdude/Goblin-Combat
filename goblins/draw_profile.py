from PIL import Image, ImageFont, ImageDraw
import requests
from io import BytesIO


def drawProfile(player, picture):
    image1 = Image.open('goblinImages/profile-2.png').convert("RGBA")
    playerPos = (110, 470)
    response = requests.get(picture)
    pfp = Image.open(BytesIO(response.content))
    pfp = pfp.resize((280, 280), Image.ANTIALIAS)
    pfpPos = (110, 110)

    image_editable = ImageDraw.Draw(image1)

    title_font = ImageFont.truetype('Squared.ttf', 128)
    header_font = ImageFont.truetype('Squared.ttf', 72)
    text_font = ImageFont.truetype('Squared.ttf', 64)

    image_editable.text((450, 160), player.user.name, (3, 3, 3), font=title_font)
    image_editable.text((450, 280), f"Level {player.level} {player.faction['name']}", (3, 3, 3), font=text_font)
    image_editable.text((750, 500), f"ATK {player.attack}", (3, 3, 3), font=header_font)
    image_editable.text((750, 650), f"HP {player.max_hit_points}", (3, 3, 3), font=header_font)
    image_editable.text((750, 800), f"DEF {player.defence}", (3, 3, 3), font=header_font)
    image_editable.text((750, 950), f"MGK {player.magic}", (3, 3, 3), font=header_font)

    playerImg = Image.open(f"goblinImages/factions/{player.faction['id']}-export.png").convert("RGBA")
    playerImg = playerImg.resize((550, 550), Image.BOX)
    image1.paste(playerImg, playerPos, playerImg)
    image1.paste(pfp, pfpPos)

    weapon = Image.open(f"goblinImages/weapons/{player.weapon.name.lower()}.png").convert("RGBA")
    weapon = weapon.resize((240, 240), Image.BOX)
    image1.paste(weapon, (1300, 470), weapon)

    armor = Image.open(f"goblinImages/armor/{player.armor.name.lower()}.png").convert("RGBA")
    armor = armor.resize((240, 240), Image.BOX)
    image1.paste(armor, (1300, 760), armor)

    trinket = Image.open(f"goblinImages/baubles/{player.trinket.name.lower()}.png").convert("RGBA")
    trinket = trinket.resize((160, 160), Image.BOX)
    image1.paste(trinket, (1340, 1060), trinket)

    image1.save('profile-export.png')
    #image1.show()


def drawInfo(item, type):
    image1 = None
    if type == "weapon":
        image1 = Image.open(f'goblinImages/weapons/{item.name.lower()}.png').convert("RGBA")

    elif type == "armor":
        image1 = Image.open(f'goblinImages/armor/{item.name.lower()}.png').convert("RGBA")

    elif type == 'trinket':
        image1 = Image.open(f'goblinImages/baubles/{item.name.lower()}.png').convert("RGBA")

    image1 = image1.resize((120, 120), Image.BOX)
    image1.save('item-enlarge.png')

