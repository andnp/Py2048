import numpy as np
from Py2048 import Game

game = Game()
print(game)

for _ in range(1000000):
    act = np.random.randint(4)

    done = game.takeAction(act)

    if done:
        print('done', _)
        break

print(game)
print(game.getScore())
