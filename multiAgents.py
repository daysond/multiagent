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
        scared because of Pacn mahaving eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # print(f'successorGameState:\n {successorGameState}')
        newPos = successorGameState.getPacmanPosition()
        # print(f'newPos: {newPos}')
        newFood = successorGameState.getFood()
        # print(f'newFood: \n {newFood}')
        newGhostStates = successorGameState.getGhostStates()
        # print(f'newGhostStates: {[str(s)for s in newGhostStates]}')
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print(f'newScaredTimes: {newScaredTimes}')
        # print("###############################################\n")
        "*** YOUR CODE HERE ***"
        
        # Reflex Agent: an agent that considers food locations, ghost locations, and the score of the current situation to decide its next action.
        
        #https://www.clear.rice.edu/comp140/labs/12/
        
        # find the closest food
        
        # if ghost is not too close (2 steps away), go to food else run away from ghost (unless scared)
        
        #Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newFood = successorGameState.getFood()
        newFoodList = newFood.asList()
        ghostPositions = successorGameState.getGhostPositions()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # print ('Successor game state:\n', successorGameState)
        # print ('Pacman current position: ', newPos)
        # print('oldFood:\n', oldFood)
        # print('newFood:\n', newFoodList)
        # print('ghostPositions: ', ghostPositions)
        # print('successorGameState.score: ', successorGameState.getScore())
        print('newScaredTimes: ', newScaredTimes)
        
        #shake the pacman out of the stuch position  
        shake = random.random()

        minDistanceGhost = float("+inf")
        for position in ghostPositions:
            minDistanceGhost = min(minDistanceGhost, util.manhattanDistance(newPos, position))

        # pac man meets ghost, game over
        if minDistanceGhost == 0:
            return float("-inf")
        
        # win state
        if successorGameState.isWin():
            return float("+inf")
        
        score = successorGameState.getScore()
        # score = 0  

        # keep distant from ghost if not scared
        if newScaredTimes[0] < 5 and minDistanceGhost < 3:
            score += minDistanceGhost
        
        # try to eat ghost when its scared
        if 40 > newScaredTimes[0] >= 5:
            score -= (2+shake) * minDistanceGhost
        
        minDistanceFood = float("+inf")
        for foodPos in newFoodList:
            minDistanceFood = min(minDistanceFood, util.manhattanDistance(foodPos, newPos))
        
        
        # go towards food 
        score -= (1+shake) * minDistanceFood
        
        # get food
        if(successorGameState.getNumFood() < currentGameState.getNumFood()):
            score += 5

        # keep pac man moving
        if action == Directions.STOP:
            score -= 10
        
        return score
    
     # s = w 1/food -  w 1/ghost
        
        
        
        
        
        
        
        
        
        
        
        
        ###### sol 1 ######
        
        # minDist = 999999
        # for point in newFood:
        #     minDist = min(minDist, manhattanDistance(newPos, point))

        # ghostDanger = 0
        # for ghost in successorGameState.getGhostPositions():
        #     dist = max(4 - manhattanDistance(newPos, ghost), 0)
        #     ghostDanger += dist*dist

        # return successorGameState.getScore() + 10.0/minDist - ghostDanger
        
        
        ###### sol 2 ######
        # score = 0

        # closestGhostPosition = newGhostStates[0].configuration.pos
        # closestGhost = manhattanDistance(newPos, closestGhostPosition)

        # # Minimize distance from pacman to food
        # newFoodPositions = newFood.asList()
        # foodDistances = [manhattanDistance(newPos, foodPosition) for foodPosition in newFoodPositions]

        # if len(foodDistances) == 0:
        #     return 0

        # closestFood = min(foodDistances)

        # # Stop action would reduce score because of the pacman's timer constraint
        # if action == 'Stop':
        #     score -= 50

        # return successorGameState.getScore() + closestGhost / (closestFood * 10) + score
    

        ####### sol 3 #######
        # newFood = successorGameState.getFood().asList()
        # minFoodist = float("inf")
        # for food in newFood:
        #     minFoodist = min(minFoodist, manhattanDistance(newPos, food))

        # # avoid ghost if too close
        # for ghost in successorGameState.getGhostPositions():
        #     if (manhattanDistance(newPos, ghost) < 2):
        #         return -float('inf')
        # # reciprocal
        # return successorGameState.getScore() + 1.0/minFoodist

        
        
        return successorGameState.getScore()

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
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
