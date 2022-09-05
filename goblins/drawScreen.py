import PIL
from PIL import Image, ImageFont, ImageDraw

def draw(player1, player2):
    image1 = Image.open('goblinImages/screen.png').convert("RGBA")
    leftGoblinPos = (280,730)
    rightGoblinPos = (1000, 730)
    
    image_editable = ImageDraw.Draw(image1)

    faction1 = player1.faction['name']
    faction2 = player2.faction['name']

    #faction1 = "Forest Goblin"
    #faction2 = "Desert Goblin"

    title_font = ImageFont.truetype('Squared.ttf', 64)
    header_font = ImageFont.truetype('Squared.ttf', 24)
    text_font = ImageFont.truetype('Squared.ttf', 16)

    health_tick = Image.open('goblinImages/health_tick.png').convert("RGBA")
    percent = player1.hit_points / player1.max_hit_points;
    size = percent * 68;
    for i in range(int(size)):
        image1.paste(health_tick, (180 + (i * 10), 200))

    health_tick = Image.open('goblinImages/health_tick.png').convert("RGBA")
    percent = player2.hit_points / player2.max_hit_points;
    size = percent * 68;
    for i in range(int(size)):
        image1.paste(health_tick, (750 + (i * 10), 480))

    image_editable.text((200,110), player1.user.name, (3, 3, 3), font=title_font)
    image_editable.text((760,400), player2.user.name, (3, 3, 3), font=title_font)

    if faction1 == 'Cave Goblin':
        goblin = Image.open('goblinImages/factions/cave-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    elif faction1 == 'Beach Goblin':
        goblin = Image.open('goblinImages/factions/beach-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    elif faction1 == 'Forest Goblin':
        goblin = Image.open('goblinImages/factions/forest-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    elif faction1 == 'Jungle Goblin':
        goblin = Image.open('goblinImages/factions/jungle-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    elif faction1 == 'Desert Goblin':
        goblin = Image.open('goblinImages/factions/desert-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    elif faction1 == 'Plains Goblin':
        goblin = Image.open('goblinImages/factions/plains-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    elif faction1 == 'Snow Goblin':
        goblin = Image.open('goblinImages/factions/snow-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)
    else:
        goblin = Image.open('goblinImages/factions/plains-export.png').convert("RGBA")
        image1.paste(goblin, leftGoblinPos, goblin)

    if faction2 == "Cave Goblin":
        goblin = Image.open('goblinImages/factions/cave-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    elif faction2 == "Beach Goblin":
        goblin = Image.open('goblinImages/factions/beach-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    elif faction2 == "Forest Goblin":
        goblin = Image.open('goblinImages/factions/forest-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    elif faction2 == "Jungle Goblin":
        goblin = Image.open('goblinImages/factions/jungle-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    elif faction2 == "Desert Goblin":
        goblin = Image.open('goblinImages/factions/desert-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    elif faction2 == "Plains Goblin":
        goblin = Image.open('goblinImages/factions/plains-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    elif faction2 == "Snow Goblin":
        goblin = Image.open('goblinImages/factions/snow-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)
    else:
        goblin = Image.open('goblinImages/factions/plains-export.png').convert("RGBA")
        goblin = goblin.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image1.paste(goblin, rightGoblinPos, goblin)

    image1.save('final.png')
    #image1.show()

#draw(69, 100)