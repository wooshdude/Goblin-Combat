import json
import random
import asyncio

class Player:

    def __init__(self, user, level, faction, weapon, armor, trinket):
        self.user = user
        f = open(f"factions/{faction}.json")
        self.faction = json.load(f)
        self.screen = None
        self.percent = 0.005

        self.weapon = weapon
        self.armor = armor
        self.trinket = trinket

        self.inventory = []

        self.level = level
        self.experience = 0
        self.max_hit_points = self.faction['health'] + self.armor.health + self.trinket.health + self.level - 1
        self.hit_points = self.max_hit_points
        self.attack = int(self.faction['attack'] + (self.weapon.attack + self.trinket.attack) + self.level - 1)
        self.magic = int(self.faction['magic'] + (self.weapon.magic + self.armor.magic + self.trinket.magic) + self.level - 1)
        self.shield = 0
        self.defence = int(self.faction['defence'] + (self.armor.defence + self.trinket.defence + self.shield))
        self.magic_defence = int((self.faction['magic_defence'] + self.armor.magic_defence + self.trinket.magic_defence) + self.level - 1)
        self.speed = (self.faction['speed'] + self.armor.speed + self.weapon.speed)


        # cosmetics
        self.hat = 0
        self.shirt = 0
        self.pants = 0

        self.kills = 0

    def restore(self):
        self.hit_points = self.max_hit_points

    def heal(self, pts):
        self.hit_points += pts
        if self.hit_points >= self.max_hit_points:
           self.hit_points = self.max_hit_points

    def test(self):
        print('test')

    async def melee(self, enemy):
        enemy.health -= self.attack
        await self.weapon.special.activate(self, enemy)

    def update(self):
        self.max_hit_points = self.faction['health'] + self.armor.health + self.trinket.health + self.level - 1
        self.hit_points = self.max_hit_points
        self.attack = int(self.faction['attack'] + (self.weapon.attack + self.trinket.attack) + self.level - 1)
        self.magic = int(
            self.faction['magic'] + (self.weapon.magic + self.armor.magic + self.trinket.magic) + self.level - 1)
        self.shield = 0
        self.defence = int(
            self.faction['defence'] + (self.armor.defence + self.trinket.defence + self.shield))
        self.magic_defence = int(
            (self.faction['magic_defence'] + self.armor.magic_defence + self.trinket.magic_defence) + self.level - 1)
        self.speed = (self.faction['speed'] + self.armor.speed + self.weapon.speed)

    def setScreen(self, screen):
        self.screen = screen

    def levelUp(self, pts):
        self.experience += pts
        needed = self.level * 100 - self.experience
        while self.experience >= needed:
            self.level += 1
            self.experience = pts - needed
            needed = self.level * 100 - self.experience

        with open(f'players/{self.user.id}.json', 'r') as f:
            playerJson = json.load(f)

        p = open(f'players/{self.user.id}.json', 'w')
        playerJson['level'] = self.level
        playerJson['experience'] = self.experience
        json.dump(playerJson, p)
        p.close()

        self.update()

    def testHealth(self):
        if self.hit_points <= 0:
            self.hit_points = 0
            return True
        else:
            return False

    def takeDamage(self, enemy):
        if enemy.attack > self.defence:
            damage = enemy.attack - self.defence
            self.hit_points -= damage


class Boss:
    def __init__(self, name, desc, attack, health, speed):
        self.name = name
        self.desc = desc
        self.attack = attack
        self.max_health = health
        self.health = self.max_health
        self.speed = speed

        self.stunned = False


class Cave:
    name = "cave"

    health = 12 * 3
    attack = 4
    magic = 1
    defence = 3
    magic_defence = 1
    speed = 1


class Desert:
    name = "desert"

    health = 6 * 3
    attack = 1
    magic = 4
    defence = 1
    magic_defence = 2
    speed = 3


class Forest:
    name = "forest"

    health = 6 * 3
    attack = 1
    magic = 4
    defence = 2
    magic_defence = 3
    speed = 2


class Jungle:
    name = "jungle"

    health = 8 * 3
    attack = 3
    magic = 2
    defence = 2
    magic_defence = 2
    speed = 4


class Beach:
    name = "beach"

    health = 8 * 3
    attack = 2
    magic = 2
    defence = 3
    magic_defence = 3
    speed = 3


class Plains:
    name = "plains"

    health = 10 * 3
    attack = 3
    magic = 2
    defence = 3
    magic_defence = 2
    speed = 2


class Snow:
    name = "snow"

    health = 12 * 3
    attack = 2
    magic = 3
    defence = 4
    magic_defence = 4
    speed = 1


class Weapon:
    def __init__(self, attack, magic, special, speed, name, desc):
        self.attack = attack
        self.magic = magic
        self.speed = speed
        self.name = name
        self.desc = desc
        self.special = special

    def attack(self, enemy):
        enemy.health -= self.attack
        self.special.activate()


class Armor:
    def __init__(self, defence, health, magic, magic_defence, speed, name, desc):
        self.defence = defence
        self.health = health
        self.magic = magic
        self.magic_defence = magic_defence
        self.speed = speed
        self.name = name
        self.desc = desc


class Trinket:
    def __init__(self, attack, health, defence, magic, magic_defence, special, name, desc):
        self.attack = attack
        self.health = health
        self.defence = defence
        self.magic = magic
        self.magic_defence = magic_defence
        self.special = special
        self.name = name
        self.desc = desc








