from classes import *
import random
from game_ticks import Game, gameObjs


class Speeds:
    sword = 2
    axe = 5
    cleaver = 8
    bow = 6
    wand = 4
    staff = 7


# special traits
class Bleed:
    # harder to proc but chunks health
    def __init__(self):
        self.name = "Bleed"
        self.desc = 'Striking an enemy with three sucessful hits will cause them to bleed for a short time.'

        self.count = 1
        self.dmgTicks = 0

        self.enemy = None

        self.listIndex = None

    async def activate(self, player, enemy):
        if self.count >= 3:
            print('bleed activated')
            self.enemy = enemy
            gameObjs.append(self.damage)
            self.count = 1
        else:
            self.count += 1

    def damage(self):
        if self.dmgTicks < 5:
            print('bled enemy')
            self.enemy.health -= 2
            self.dmgTicks += 1
        else:
            self.enemy = None
            gameObjs.remove(self.damage)


class Explode:
    # does AOE damage
    def __init__(self):
        self.name = "Explode"
        self.desc = "Striking an enemy with 3 successful hits will cause them to explode, dealing damage to surrounding enemies."

        self.count = 1

    async def activate(self, player, enemy):
        if self.count >= 3:
            enemy.health -= 15
            print('exploded')
            self.count = 1
        else:
            self.count += 1


class Stun:
    # prevents boss from attacking
    def __init__(self):
        self.name = 'Stun'
        self.desc = "Small chance to stun the enemy in question, preventing them from attacking for a short while."

        self.chance = 0

    async def activate(self, player, enemy):
        if not enemy.stunned:
            self.chance = random.randint(1, 10)

        if self.chance == 10:
            enemy.stunned = True
            await asyncio.sleep(5)
            enemy.stunned = False


class Shockwave:
    def __init__(self):
        self.name = "Shockwave"
        self.desc = "After 7 final blows, you send out a shockwave, stunning and damaging surrounding enemies."

    async def activate(self, player, enemy):
        if player.kills >= 7:
            enemy.health -= 12


items = {
    # weapons
    'unarmed': Weapon(1, 1, None, 1, "Unarmed", 'Your fist.'),
    'rusty sword': Weapon(2, 3, None, Speeds.sword, "Rusty Sword",
                            "An old rusty sword you found. You could probably find something better..."),
    'old battleaxe': Weapon(5, 2, None, Speeds.axe, "Old Battleaxe", "It's older than you are. What does it know?"),
    'rusted axe': Weapon(4, 4, None, Speeds.axe, "Rusted Axe", "It's in poor condition, but it can definitely still do some damage!"),
    
    # cleaver high attack with slow speed
    'damaged cleaver': Weapon(12,3, None, Speeds.cleaver, "Damaged Cleaver", "How did something this big get busted up anyway?"),
    'rusted cleaver': Weapon(16, 4, None, Speeds.cleaver, "Rusted Cleaver", "This would probably take a while to clean."),
    'reinforced cleaver': Weapon(24, 5, None, Speeds.cleaver, "Reinforced Cleaver", "A well forged cleaver."),
    'buster sword': Weapon(32, 12, None, Speeds.cleaver, "Buster Sword", "It's big. Too big. How are you supposed to swing this anyway?"),

    'rusted hammer': Weapon(8, 5, None, Speeds.axe, "Rusted Hammer", "The rust flakes off when you strike."),
    #'rusted scythe': Weapon(7, 5, Speeds.bow, "Rusted Scythe", "The least menacing weapon"),
    
    # mace good attack and magic
    'damaged mace': Weapon(4, 4, None, Speeds.axe, "Damaged Mace", "Be careful with it!"),
    'iron mace': Weapon(8, 8, None, Speeds.axe, "Iron Mace", "Clearly, this was designed to bash some skulls..."),
    'reinforced mace': Weapon(12, 12, None, Speeds.axe, "Reinforced Mace", "The ground trembles when you swing this mighty weapon."),
    
    # bow good attack with slower speed
    # 'damaged bow': Weapon(6, 2, Speeds.bow, "Damaged Bow", "It's amazing that it doesn't snap.."),
    'wooden bow': Weapon(12, 4, None, Speeds.bow, "Wooden Bow", "As long as it shoots, right?"),
    'reinforced bow': Weapon(16, 4, None, Speeds.bow, "Reinforced Bow", "Straight and true, just like God intended."),
    'frost bow': Weapon(20, 20, None, Speeds.bow, "Frost Bow", "You feel the ice cold chill of your bolts as you draw back."),
    
    # wand good magic attack with decent speed
    # 'damaged wand': Weapon(2, 6, Speeds.wand, "Damaged Wand", "some description"),
    'wooden wand': Weapon(3, 12, None, Speeds.wand, "Wooden Wand", "some description"),
    'reinforced wand': Weapon(4, 16, None, Speeds.wand, "Reinforced Wand", "some description"),
    'pocket wand': Weapon(6, 8, None, Speeds.wand, "Pocket Wand", "some description"),

    # staff high magic attack with slow speed
    # 'damaged staff': Weapon(3, 12, Speeds.staff, "Damaged Staff", "some description"),
    'wooden staff': Weapon(5, 16, None, Speeds.staff, "Wooden Staff", "some description"),
    'reinforced staff': Weapon(7, 24, None, Speeds.staff, "Reinforced Staff", "some description"),

    'the splinter': Weapon(10, 15, Bleed(), Speeds.sword, "The Splinter", "The Legendary sword of Animal Farm."),
    'demon scythe': Weapon(12, 6, None, Speeds.bow, "Demon Scythe", "This dark bladed weapon was used to cut the bone grass of The Skeletal Fields."),
    'monk spade': Weapon(14, 11, None, Speeds.staff, "Monk Spade", "This weapon was used by an ancient group of monks, and is deeply connected to the soul."),
    'gem blade': Weapon(20, 11, Explode(), Speeds.staff, "Gem Blade", "you should kill yourself."),

    #armor
    'unarmored': Armor(0, 0, 0, 0, 10, "Unarmored", "Your birthday suit"),
    'chainmail': Armor(3, 8, 0, 5, 7, "Chainmail", "A nice mix of defence and mobility."),
    'leather': Armor(1, 3, 1, 5, 9, "Leather", "It's a lot easier to move in this armor, but you feel like it might not offer that much protection."),
    'platemail': Armor(5, 13, 3, 10, 5, "Platemail", "A much sturdier set of armor."),
    'ritual armor': Armor(2, 12, 10, 16, 8, "Ritual Armor", "A set of robes meant for magic rituals."),
    'golem plate': Armor(8, 18, 8, 12, 7, "Golem Plate", "An ancient hollow golem, once made to protect it's maker."),

    #trinkets
    'none': Trinket(0, 0, 0, 0, 0, None, "None", "Empty"),
    'bracelet of life': Trinket(-1, 2, 0, -1, 0, None, "Bracelet of life", "You feel invigorated while wearing this."),
    'bracelet of strength': Trinket(2, -1, -1, 0, 0, None, "Bracelet of Strength", "You feel strengthened while wearing this."),
    'bracelet of defence': Trinket(-2, 0, 2, 0, 0, None, "Bracelet of Defence", "You feel sturdier while wearing this."),
    'bracelet of magic': Trinket(0, 0, 0, 2, -2, None, "Bracelet of Magic", "You feel powerful while wearing this."),
    'bracelet of magic defence': Trinket(0, 0, 0, -2, 2, None, "Bracelet of Magic Defence", "You feel fortified while wearing this."),

    #'the debug sword': Weapon(100, 100, Speeds.sword, "The Debug Sword", "Get fucked, idiot")
}


