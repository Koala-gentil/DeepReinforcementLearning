import game

game = game.Game()

while not game.gameState.isEndGame:
    game.gameState.display_console()
    action = int(input())
    game.step(action)

game.gameState.display_console()