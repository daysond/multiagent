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

from operator import itemgetter

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        
        #   pacman gets higher score if foods eaten
        foodBonus = int(successorGameState.getNumFood() < currentGameState.getNumFood()) * 10
        #   encourage pacman to eat food
        stopPenalty = -10 * int(action == Directions.STOP)
        
        minFoodDistance = float("inf")
        for foodPosition in newFood.asList():
            minFoodDistance = min(minFoodDistance, manhattanDistance(newPos, foodPosition))

        minGhostDistance = float("inf")
        for ghostPosition in successorGameState.getGhostPositions():
            minGhostDistance = min(minGhostDistance, manhattanDistance(newPos, ghostPosition))
        
        #   stay away from the ghost unless scared
        danger = int (minGhostDistance < 2 and newScaredTimes[0] < 2) * 9999
        
        # for ghostPosition in successorGameState.getGhostPositions():
        #     if (manhattanDistance(newPos, ghostPosition) < 2 and newScaredTimes[0] < 2):
        #         return -float('inf')
       
        return  1 / minFoodDistance + foodBonus + stopPenalty - danger

        

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
        
        numAgents = gameState.getNumAgents()

        def maxValue(state: GameState, currentAgent, currentDepth, actionTaken):
            #   terminal test
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state), actionTaken
            
            nextAgent = currentAgent + 1    #   index of next agent
            actions = state.getLegalActions(currentAgent)
            #   gets a list of scores of the successor states
            scores = [minValue(state.generateSuccessor(currentAgent, action), nextAgent, currentDepth, action)[0] for action in actions]

            v = max(scores)
            a = actions[scores.index(max(scores))]
            
            return v, a

        def minValue(state: GameState, currentAgent, currentDepth, actionTaken):
            #   terminal test
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state), actionTaken
            
            nextAgent = currentAgent + 1    #   index of next agent
            if nextAgent == numAgents:
                nextAgent = 0               #   resets agent index to pacman (max agent)
                currentDepth += 1           #   keeping track of the depth explored

            actions = state.getLegalActions(currentAgent)

            if currentDepth == self.depth and currentAgent == numAgents - 1:
                #   max depth reached, evaluating successor states    
                scores = [self.evaluationFunction(state.generateSuccessor(currentAgent, action)) for action in actions]         
            else:
                #   gets a list of scores of the successor states depending on the agent
                scores =[maxValue(state.generateSuccessor(currentAgent, action), nextAgent, currentDepth, action)[0] for action in actions] if nextAgent == 0 else [minValue(state.generateSuccessor(currentAgent, action), nextAgent, currentDepth, action)[0] for action in actions]
     
            v = min(scores)
            a = actions[scores.index(v)]  
            
            return v, a

        _, action = maxValue(gameState, 0, 0, None)
        
        return action
        

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
        action, score = self.getBestActionAndScore(gameState, 0, 0, float("-inf"), float("inf"))

        # Return the action from result
        return action
        #util.raiseNotDefined()

    def getBestActionAndScore(self, gameState, agentIndex, depth, alpha, beta):
        """
        Returns value as pair of [action, score] based on the different cases:
        1. Terminal state
        2. Max-agent
        3. Min-agent
        """
        # Terminal states:
        if len(gameState.getLegalActions(agentIndex)) == 0 or depth == self.depth:
            return "", gameState.getScore()

        # Max-agent: Pacman has index = 0
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth, alpha, beta)

        # Min-agent: Ghost has index > 0
        else:
            return self.minValue(gameState, agentIndex, depth, alpha, beta)

    def maxValue(self, game_state, agentIndex, depth, alpha, beta):
        """
        Returns the max utility action-score for max-agent with alpha-beta pruning
        """
        legalActions = game_state.getLegalActions(agentIndex)
        maxValue = float("-inf")
        maxAction = ""

        for action in legalActions:
            successor = game_state.generateSuccessor(agentIndex, action)
            successor_index = agentIndex + 1
            successor_depth = depth

            # Update the successor agent's index and depth if it's pacman
            if successor_index == game_state.getNumAgents():
                successor_index = 0
                successor_depth += 1

            # Calculate the action-score for the current successor
            current_action, current_value \
                = self.getBestActionAndScore(successor, successor_index, successor_depth, alpha, beta)

            # Update max_value and max_action for maximizer agent
            if current_value > maxValue:
                maxValue = current_value
                maxAction = action

            # Update alpha value for current maximizer
            alpha = max(alpha, maxValue)

            # Pruning: Returns max_value because next possible max_value(s) of maximizer
            # can get worse for beta value of minimizer when coming back up
            if maxValue > beta:
                return maxAction, maxValue

        return maxAction, maxValue

    def minValue(self, game_state, agentIndex, depth, alpha, beta):
        """
        Returns the min utility action-score for min-agent with alpha-beta pruning
        """
        legalActions = game_state.getLegalActions(agentIndex)
        minValue = float("inf")
        minAction = ""

        for action in legalActions:
            successor = game_state.generateSuccessor(agentIndex, action)
            successor_index = agentIndex + 1
            successor_depth = depth

            # Update the successor agent's index and depth if it's pacman
            if successor_index == game_state.getNumAgents():
                successor_index = 0
                successor_depth += 1

            # Calculate the action-score for the current successor
            current_action, current_value \
                = self.getBestActionAndScore(successor, successor_index, successor_depth, alpha, beta)

            # Update min_value and min_action for minimizer agent
            if current_value < minValue:
                minValue = current_value
                minAction = action

            # Update beta value for current minimizer
            beta = min(beta, minValue)

            # Pruning: Returns min_value because next possible min_value(s) of minimizer
            # can get worse for alpha value of maximizer when coming back up
            if minValue < alpha:
                return minAction, minValue

        return minAction, minValue    

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
