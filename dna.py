import random

class DNA:
  """
  Each rocket contains a DNA class. This class holds information regarding the action
  the rocket will take for each frame that its alive.

  Attributes
  ----------
  genes : list
    A list where each index represents a frame. Each index contains a list of 
    4 booleans.  These booleans correspond to the a specific action the rocket will make in the frame.
  """
  def __init__(self, max_frames_alive=500, mutation_rate=0.02, genes=None):
    """
    Parameters
    ----------
    max_frames_alive : int
      Max number of frames the rocket will be alive for
    mutation_rate : float
      Probability that a specific index/frame/gene is mutated in a random manner.  Helps encourage exploration
    genes : list
      Represents genes that were created by merging two parent genes together.
      
    """
    self.mutation_rate = mutation_rate
    
    if genes:
      self.genes = genes
    else: # Initialize with random actions
      self.genes = []
      for i in range(max_frames_alive):
        self.genes.append([random.choice([True,False]) for _ in range(4)])

  def crossover(self, partner):
    """ Merges the properties of two dna by randomly selecting an index in the middle. The returned 
        DNA will contain the first from the parentA and the second part from parentB

    Parameters
    ----------
    partner : DNA
      The partner DNA self will be merging with

    Returns
    -------
    DNA
      DNA object that contains genes from both self and partner
    """
    newdna = []
    mid = random.randint(0,len(self.genes))

    newdna[0:mid] = self.genes[0:mid]
    newdna[mid:] = self.genes[mid:]
    return DNA(genes=newdna)

  def mutation(self):
    """ Mutates somes genes into a random action to promote exploration
    """
    for i in range(len(self.genes)):
      if random.uniform(0, 1) < self.mutation_rate:
        self.genes[i] = [random.choice([True,False]) for _ in range(4)]

