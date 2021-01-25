import pygame
import os

from math import sin, cos, radians
from utils import rotate_center, get_distance
from dna import DNA

TURN_ANGLE = 15
SPEED_INCREASE = 2
SPEED_DECREASE = 1

current_path = os.path.dirname(__file__) 
image_path = os.path.join(current_path, 'rocket.png') 

class Rocket:
  """ 
  Class representing a rocket

  Attributes
  ----------
  pos : list
    x,y coordinates of the rocket
  img_surface : pygame surface
    The image of the rocket
  rotate_surface : pygame surface
    The rotated image of the rocket
  corners : list
    Three points that act as the collision sensor points for the rocket
  center : list
    x,y coordinates of the center rocket
  angle : int
    Angle of the rocket
  speed : int
    Speed at which the rocket is moving
  max_speed : int
    Speed of the rocket is limited by the max_speed
  min_speed : int
    Speed of the rocket cannot go below the min_speed
  alive : boolean
    Specifies whether or not the rocket has crashed/out bounds
  fitness : float
    fitness/score of the rocket
  reached_target : boolean
    Specifies whether rocket has reached target
  frames_alive : 0
    How many frames has the rocket survived for
  dna : DNA
    The object that contains the rockets genes. More specifically, the actions the rocket
    will take for each frame

  """
  def __init__(self, dna=None):
    """
    Parameters
    ----------
    dna : DNA
      DNA that is passed from the crossover/merging of two parents
    """
    self.pos = [100, 300] 
    self.img_surface = pygame.transform.scale(pygame.image.load(image_path), (50,50))
    self.img_surface = pygame.transform.rotate(self.img_surface, 270)
    self.rotate_surface = self.img_surface
    self.corners = [ [0,0] for _ in range(3) ]
    self.center = [self.pos[0] + 25, self.pos[1] + 25]
    self.angle = 0

    self.speed = 0
    self.max_speed = 10
    self.min_speed = 0

    self.alive = True
    self.fitness = 0.0
    self.reached_target = False
    self.frames_alive = 0

    if dna:
      self.dna = dna
    else:
      self.dna = DNA()

  def update(self):
    """ Updates attributes of the rocket such as location, angle, and image rotation.
    """
    if self.angle == 360 or self.angle == -360:
      self.angle = 0
    
    # Rotate rocket
    self.rotate_surface = rotate_center(self.img_surface, self.angle)
    angle = radians(360 - self.angle)

    # Update position
    self.pos[0] += cos(angle) * self.speed
    self.pos[1] += sin(angle) * self.speed

    self.center = [self.pos[0] + 25, self.pos[1] + 25]

    # Update the 3 corners of the rocket
    corner_angles = [0, 150, 210]
    for i in range(len(self.corners)):
      self.corners[i] = [
        self.center[0] + cos(angle + radians(corner_angles[i])) * 22, 
        self.center[1] + sin(angle + radians(corner_angles[i])) * 22
      ]
  
  def display(self, screen):
    """ Show the rocket on screen

    Parameters
    ----------
    screen : pygame display
      Main display of our environment
    """
    screen.blit(self.rotate_surface, self.pos)
    screen.blit(self.img_surface, self.pos)

  def check_collision(self, width, height, barriers):
    """ Collision detection of rocket. Not optimal.

    Parameters
    ----------
    width : int
      Width of environment
    height : int
      Height of environment
    barriers : list
      List of pygame rectangles that represent barriers
    """
    for barrier in barriers:
      for corner in self.corners:
        if barrier.collidepoint(corner):
          self.alive = False
        elif corner[0] < 0 or corner[0] > width:
          self.alive = False
        elif corner[1]< 0 or corner[1] > height:
          self.alive = False

  def check_reached_target(self, target):
    """ Check if rocket has reached target

    Parameters
    ----------
    target : tuple
      x,y coords of target
    """
    for corner in self.corners:
      if get_distance(corner, target) < 10:
        self.alive = False
        self.reached_target = True

  def calc_fitness(self, target):
    """ Calculate the fitness/score of the rocket. The closer it is the greater the 
        fitness. Also, the less time it takes to reach the target the greater the fitness.

    Parameters
    ----------
    target : tuple
      x,y coords of target
    """
    distance = get_distance(self.center, target)
    self.fitness = (1/distance)**2
    if self.reached_target:
      self.fitness += (1/self.frames_alive)**2
      self.fitness *= 2

  def decide_next_move(self, frame):
    """ Perform an action depending on what frame the rocket's genes are on

    Parameters
    ----------
    frame : int
      Current frame the game loop is on
    """
    self.frames_alive = frame

    if self.dna.genes[frame][0]:
      self.speed -= SPEED_DECREASE
    if self.dna.genes[frame][1]:
      self.speed += SPEED_INCREASE
    if self.dna.genes[frame][2]:
      self.angle += TURN_ANGLE
    if self.dna.genes[frame][3]:
      self.angle -= TURN_ANGLE

    # Limit speed
    if self.speed >= self.max_speed:
      self.speed = self.max_speed
    elif self.speed <= self.min_speed:
      self.speed = self.min_speed