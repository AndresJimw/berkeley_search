# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print("ACTION:", action)
        # print("newPos:", newPos)
        # print("newFood.asList():", newFood.asList())
        # print("newGhostPositions:", [ghost.getPosition() for ghost in newGhostStates])
        # print("newScaredTimes:", newScaredTimes)
        
        score = 0
        
        if action == Directions.STOP:
            score -= 10 # Penalizar quedarse quieto
            
        for ghost in newGhostStates:
            dist = manhattanDistance(newPos, ghost.getPosition())
            if ghost.scaredTimer == 0:
                if dist <= 1:
                    score -= 200  # Muy cerca de fantasma no asustado
                elif dist <= 3:
                    score -= 10 / dist
            else:
                score += 5 / (dist + 1)  # Incentiva ir hacia fantasmas asustados
                
        foodList = newFood.asList()
        if foodList:
            foodDistances = [manhattanDistance(newPos, food) for food in foodList]
            score += 10 / (min(foodDistances) + 1)  # Proximidad a comida
            score += 100 / len(foodList) # Incentivar estados con menos comida
            
        score += successorGameState.getScore() # Agrega el puntaje base del estado
        
        currentPos = currentGameState.getPacmanPosition()
        if newPos == currentPos:
            score -= 50 # Penaliza por movimientos redundantes

        return score
        # return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, state):
            # Corte si es victoria, derrota o se alcanzó la profundidad
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            nextAgent = (agentIndex + 1) % state.getNumAgents()  # Siguiente agente (pacman = 0, fantasmas >= 1)
            nextDepth = depth + 1 if nextAgent == 0 else depth   # Solo aumenta con Pacman

            actions = state.getLegalActions(agentIndex)  # Acciones
            scores = [minimax(nextAgent, nextDepth, state.generateSuccessor(agentIndex, a)) for a in actions]

            if agentIndex == 0:  # Pacman
                return max(scores)
            else:  # Fantasma
                return min(scores)

        actions = gameState.getLegalActions(0)  # Acciones para Pacman
        # Retorna la mejor acción para Pacman usando minimax
        return max(actions, key=lambda a: minimax(1, 0, gameState.generateSuccessor(0, a)))
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(agentIndex, depth, state, alpha, beta):
            # Corte si se alcanza profundidad o estado terminal
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            nextAgent = (agentIndex + 1) % state.getNumAgents()  # Siguiente agente
            nextDepth = depth + 1 if nextAgent == 0 else depth   # Aumenta solo si vuelve a Pacman

            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            if agentIndex == 0:  # Pacman (Max)
                value = float('-inf')
                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, alphabeta(nextAgent, nextDepth, successor, alpha, beta))
                    if value > beta:
                        return value  # Poda beta
                    alpha = max(alpha, value)
                return value
            else:  # Fantasma (Min)
                value = float('inf')
                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = min(value, alphabeta(nextAgent, nextDepth, successor, alpha, beta))
                    if value < alpha:
                        return value  # Poda alpha
                    beta = min(beta, value)
                return value

        # Elije acción con poda alfa-beta
        bestAction = None
        alpha, beta = float('-inf'), float('inf')
        bestValue = float('-inf')
        for action in gameState.getLegalActions(0):  # Acciones Pacman
            successor = gameState.generateSuccessor(0, action)
            value = alphabeta(1, 0, successor, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, bestValue)
        return bestAction
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
