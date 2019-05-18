import numpy as np
import logging

class Game:

    def __init__(self):
        self.currentPlayer = 1 # 1 = bleu, -1 = rouge
        self.gameState = GameState(np.zeros(121, dtype=np.int), self.currentPlayer) # 11 x 11 board
        self.actionSpace = np.zeros(121, dtype=np.int)
        self.pieces = {'1': 'B', '0': '-', '-1': 'R'}
        self.grid_shape = (11, 11)
        self.input_shape = (2, 11, 11)
        self.name = 'hex'
        self.state_size = len(self.gameState.binary)
        self.action_size = len(self.actionSpace)
        
    def reset(self):
        self.currentPlayer = 1 # 1 = bleu, -1 = rouge
        self.gameState = GameState(np.zeros(121, dtype=np.int), self.currentPlayer) # 11 x 11 board
        return self.gameState
    
    def step(self, action):
        next_state, value, done = self.gameState.takeAction(action)
        self.gameState = next_state
        self.currentPlayer = -self.currentPlayer
        info = None
        return ((next_state, value, done, info))
       
    def identities(self, state, actionValues):
        identities = [(state,actionValues)]

        currentBoard = np.array(state.board)
        currentAV = np.array(actionValues)

        identities.append((GameState(currentBoard, state.playerTurn), currentAV))

        return identities

class GameState:

    def __init__(self, board, playerTurn):
        self._DIRECTIONS = [10, -1, -10, 1, 11, -11]
        self.board = board
        self.playerTurn = playerTurn
        self.binary = self._binary()
        self.pieces = {'1': 'B', '0': '-', '-1': 'R'}
        self.id = self._convertStateToId()
        self.allowedActions = self._allowedActions()
        self.isEndGame = self._checkForEndGame()
        self.value = self._getValue()
        self.score = self._getScore()


    def _allowedActions(self):
        return [i for i in range(121) if self.board[i] == 0] # index where cell is empty

    def _binary(self):
        currentplayer_position = np.zeros(len(self.board), dtype=np.int)
        currentplayer_position[self.board == self.playerTurn] = 1

        other_position = np.zeros(len(self.board), dtype=np.int)
        other_position[self.board==-self.playerTurn] = 1

        position = np.append(currentplayer_position,other_position)

        return (position)

    def _convertStateToId(self):
        player1_position = np.zeros(len(self.board), dtype=np.int)
        player1_position[self.board==1] = 1

        other_position = np.zeros(len(self.board), dtype=np.int)
        other_position[self.board==-1] = 1

        position = np.append(player1_position,other_position)

        id = ''.join(map(str,position))

        return id


    def _getNeighbors(self, index):
        for dir in self._DIRECTIONS:
            neighbor = index + dir
            if neighbor >= 0 and neighbor < 121:
                yield neighbor


    def _checkForEndGame(self):
        # pas besoin de vérifier une égalité (impossible dans le jeu de hex)
        # TODO: ne pas vérifier la victoire du joueur courant ???

        # check red player (-1) (ligne de haut en bas)
        seen = np.zeros(121, dtype=np.int)
        pile = [i for i in range(11) if self.board[i] == -1] # flood fill algo
        seen[pile] = 1
        while len(pile) > 0 :
            index = pile.pop(0)
            for neighbor in self._getNeighbors(index):
                if self.board[neighbor] == -1 and seen[neighbor] == 0:
                    if neighbor // 11 == 10: # atteint le bas
                        return 1
                    seen[neighbor] = 1
                    pile.append(neighbor)

        # check blue player (1) (ligne de gauche a droite)
        seen = np.zeros(121, dtype=np.int)
        pile = [i for i in range(0, 121, 11) if self.board[i] == 1] # flood fill algo
        seen[pile] = 1
        while len(pile) > 0 :
            index = pile.pop(0)
            for neighbor in self._getNeighbors(index):
                if self.board[neighbor] == 1 and seen[neighbor] == 0:
                    if neighbor % 11 == 10: # atteint le côté droit
                        return 1
                    seen[neighbor] = 1
                    pile.append(neighbor)

        return 0
    
    def _getValue(self):
        # TODO: incompréhensible
        if self.isEndGame:
            return (-1, -1, 1)
        return (0, 0, 0)

    def _getScore(self):
        tmp = self.value
        return (tmp[1], tmp[2])


    def takeAction(self, action):
        newBoard = np.array(self.board)
        newBoard[action] = self.playerTurn

        newState = GameState(newBoard, -self.playerTurn)
        value = 0
        done = 0

        if newState.isEndGame:
            value = newState.value[0]
            done = 1

        return (newState, value, done)

    def render(self, logger):
        for r in range(11):
            logger.info([self.pieces[str(x)] for x in self.board[11*r : (11*r + 7)]])
        logger.info('--------------')
