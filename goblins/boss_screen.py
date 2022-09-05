import PIL
from PIL import Image, ImageFont, ImageDraw
from bosses import enemies


def drawBoss(boss):
    image1 = Image.open('goblinImages/new-boss-arena.png').convert("RGBA")
    image1 = image1.resize((1600, 1440), Image.BOX)
    bossPos = (450, 500)

    image_editable = ImageDraw.Draw(image1)

    title_font = ImageFont.truetype('Squared.ttf', 64)
    header_font = ImageFont.truetype('Squared.ttf', 24)
    text_font = ImageFont.truetype('Squared.ttf', 16)

    health_tick = Image.open('goblinImages/health_tick.png').convert("RGBA")
    percent = boss.health / boss.max_health

    size = percent * 125
    for i in range(int(size)):
        image1.paste(health_tick, (190 + (i * 10), 190))

    image_editable.text((200, 110), f'{boss.name}, {boss.desc}', (3, 3, 3), font=title_font)

    bossImage = Image.open(f'goblinImages/bosses/{boss.name.lower()}.png').convert("RGBA")
    image1.paste(bossImage, bossPos, bossImage)

    image1.save('boss-screen-export.png')
    #image1.show()


drawBoss(enemies['zydron'])

