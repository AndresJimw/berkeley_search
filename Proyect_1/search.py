# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    closed = []
    # Q= util.Queue()
    Q= util.Stack()
    s = (problem.getStartState(), [])
    Q.push(s)
    while not Q.isEmpty():
        (u, path) = Q.pop()
        if problem.isGoalState(u):
            return path
        if u not in closed:
            closed.append(u)
            for v, action, cost in problem.getSuccessors(u):
                newPath = path.copy()
                newPath.append(action)
                Q.push((v, newPath))
    return []
    # from util import Stack

    # # Initialize the stack with the starting state and an empty path
    # frontier = Stack()
    # frontier.push((problem.getStartState(), []))
    
    # # Set to keep track of visited states
    # visited = set()

    # while not frontier.isEmpty():
    #     current_state, path = frontier.pop()
        
    #     # Check if current state is the goal
    #     if problem.isGoalState(current_state):
    #         return path
        
    #     if current_state not in visited:
    #         visited.add(current_state)
            
    #         # Get all successors and add them to the frontier
    #         for successor, action, _ in problem.getSuccessors(current_state):
    #             if successor not in visited:
    #                 new_path = path + [action]
    #                 frontier.push((successor, new_path))
    
    # # Return empty list if no solution found (though Pacman mazes always have solutions)
    # return []

    # util.raiseNotDefined()    

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed = []
    Q= util.Queue()
    # Q= util.Stack()
    s = (problem.getStartState(), [])
    Q.push(s)
    while not Q.isEmpty():
        (u, path) = Q.pop()
        if problem.isGoalState(u):
            return path
        if u not in closed:
            closed.append(u)
            for v, action, cost in problem.getSuccessors(u):
                newPath = path.copy()
                newPath.append(action)
                Q.push((v, newPath))
    return []
    # util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Q = util.PriorityQueue()
    closed = []
    s = (problem.getStartState(), [], 0)  # (state, path, cost)
    Q.push(s, 0)

    while not Q.isEmpty():
        (u, path, accumulated_cost) = Q.pop()
        if problem.isGoalState(u):
            return path
        if u not in closed:
            closed.append(u)
            for v, action, step_cost in problem.getSuccessors(u):
                newPath = path.copy()
                newPath.append(action)
                newCost = accumulated_cost + step_cost
                Q.push((v, newPath, newCost), newCost)
    return []
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Q = util.PriorityQueue()
    g_scores = {}
    s = (problem.getStartState(), [], 0)  # (state, path, cost)
    g_scores[s[0]] = 0
    Q.push(s, heuristic(s[0], problem))

    while not Q.isEmpty():
        (u, path, accumulated_cost) = Q.pop()
        if problem.isGoalState(u):
            return path
        if g_scores[u] < accumulated_cost:
            continue
        for v, action, step_cost in problem.getSuccessors(u):
            newPath = path.copy()
            newPath.append(action)
            newCost = accumulated_cost + step_cost
            if v not in g_scores or newCost < g_scores[v]:
                g_scores[v] = newCost
                f = newCost + heuristic(v, problem)
                Q.push((v, newPath, newCost), f)
    return []
    # util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
