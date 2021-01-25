import pygame
import math

def rotate_center(image, angle):
  """ Rotates image

  Parameters
  ----------
  image : pygame surface
    Image of the rocket
  angle : int
    angle to rotate image
  """
  orig_rect = image.get_rect()
  rot_image = pygame.transform.rotate(image, angle)
  rot_rect = orig_rect.copy()
  rot_rect.center = rot_image.get_rect().center
  rot_image = rot_image.subsurface(rot_rect).copy()
  return rot_image

def get_distance(p1, p2):
  """ Calculate distance between two (x,y) points

  Parameters
  ----------
  p1, p2 : list
    x,y point
  """
  return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))