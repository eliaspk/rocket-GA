import random

from rocket import Rocket

class Population:
  """ 
  Class that represents the population of the rockets.

  Attributes
  ----------
  rockets : list
    List of all rockets in game
  mating_pool : list
    List that will contain a distribution of rockets that depends on their fitness

  """
  def __init__(self, pop_size):
    """
    Parameters
    ----------
    pop_size : int
      Number of rockets in our population
    """
    self.rockets = []
    self.mating_pool = []

    for i in range(pop_size):
      self.rockets.append(Rocket())

  def evalutate(self, target):
    """ Fills our mating pool with a distribution of rockets that is proportional to 
        their fitness. The higher the rockets fitness, the higher its count is in the 
        mating pool
    
    Parameters
    ----------
    target : tuple
      The x,y coordinates of the rocket's target
    """

    maxfit = 0
    # Calculate each rocket fitness and save maximum fit
    for rocket in self.rockets:
      rocket.calc_fitness(target)
      if rocket.fitness > maxfit:
        maxfit = rocket.fitness
    
    # Normalize fitness of rocket between 0 - 1
    for rocket in self.rockets:
      rocket.fitness /= maxfit
    self.mating_pool = []

    # Add rockets to mating pool
    for rocket in self.rockets:
      n = rocket.fitness * 100
      for i in range(round(n)):
        self.mating_pool.append(rocket)

  def selection(self):
    """ Randomly select two parents from the mating pool to merge together
        and create a child rocket. Apply mutation to child to increase exploration
    """
    newpopulation = []
    for rocket in self.rockets:
      parentA = random.choice(self.mating_pool).dna
      parentB = random.choice(self.mating_pool).dna
      child = parentA.crossover(parentB)
      child.mutation()
      newpopulation.append(Rocket(child))
    self.rockets = newpopulation