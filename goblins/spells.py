import asyncio

from game_ticks import Game, gameObjs


class Sunray:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.magic / 2) + 8
        for i in players.values():
            i.heal(int(player.magic / 2))
        print(f'{player.user.name} cast sunray')


class SacredLight:
    def __init__(self):
        self.ticks = 0
        self.player = None
        self.players = None
        self.listIndex = None

    async def activate(self, player, players, enemy):
        print(f'{player.user.name} cast sacred light')
        gameObjs.append(self.effect)
        self.player = player
        self.players = players

    def effect(self):
        if self.ticks < int(5):
            self.ticks += 1
            for i in self.players.values():
                i.heal(int(self.player.magic * 0.05))
                print(f'healed {i.user.name}')
        else:
            gameObjs.remove(self.effect)
            self.ticks = 0


class SaltSplash:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.magic + 5)
        print(f'{player.user.name} cast sunray')


class SandCastle:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        for i in players.values():
            i.shield = player.defence * 0.25

        await asyncio.sleep(6)

        for i in players.values():
            i.shield = 0

        print(f'{player.user.name} cast sunray')


class Ooga:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= player.attack + int(player.attack * 0.10)


class Umga:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= player.attack + int(player.attack * 0.15)


class CrushingSands:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= player.magic - int(player.magic * 0.50)
        enemy.stunned = True

        await asyncio.sleep(4)

        enemy.stunned = False


class SandWave:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= player.magic


class Blowgun:
    def __init__(self):
        self.enemy = None
        self.ticks = 0

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.magic * 0.05)
        self.enemy = enemy

        gameObjs.append(self.effect)

    def effect(self):
        if self.ticks < 5:
            self.enemy.health -= 5
        else:
            gameObjs.remove(self.effect)


class Machette:
    def __init__(self):
        self.enemy = None
        self.ticks = 0

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.attack + (player.magic * 0.10))


class Pumpkin:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.magic)


class Pitchfork:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.attack + (player.magic * 0.10))


class FreezingTouch:
    def __init__(self):
        self.ticks = 0
        self.enemy = None
        self.player = None

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.magic * 0.10)
        self.player = player
        self.enemy = enemy

        gameObjs.append(self.effect)

    def effect(self):
        if self.ticks < 6:
            self.enemy.health -= int(self.player.magic * 0.10)
            self.enemy.stunned = True
        else:
            gameObjs.remove(self.effect)
            self.enemy.stunned = False


class IceSpikes:
    def __init__(self):
        pass

    async def activate(self, player, players, enemy):
        enemy.health -= int(player.magic)


spells = {
    'sunray': Sunray(),
    'sacred light': SacredLight(),
    'salt splash': SaltSplash(),
    'sand castle': SandCastle(),
    'ooga oo': Ooga(),
    'umga um': Umga(),
    'crushing sands': CrushingSands(),
    'sand wave': SandWave(),
    'blowgun': Blowgun(),
    'machette': Machette(),
    'rolling pumpkin': Pumpkin(),
    'pitchfork': Pitchfork(),
    'freezing touch': FreezingTouch(),
    'ice spikes': IceSpikes(),
}


