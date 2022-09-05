from discord.ext import tasks

gameObjs = []


class Game:
    def __init__(self):
        self.gameTicks.start()

    @tasks.loop(seconds=1)
    async def gameTicks(self):
        for i in reversed(range((len(gameObjs)))):
            #print(self.objs[i])
            try:
                gameObjs[i]()
            except TypeError:
                pass
