import pygame
import sys

from population import Population

PRIMARY_FONT_SIZE = 32
SECONDAY_FONT_SIZE = 18

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Environment():
  """ 
  Class that represents the environment that the game will run in.

  Attributes
  ----------
  width : int
    Width of pygame screen
  height : int
    Height of pygame screen
  screen : pygame display
    Used to specify where images, shapes, colors will be rendered
  message_cords : list
    Specifies the coordinates for where directions will be displayed on the screen
  clock : pygame clock
    Used to specify the FPS the environment will run in 
  cur_frame : int
    Current frame of the environment
  running : Boolean
    If environment is running
  population : Population
    Contains the population of rockets used for training
  barriers : list
    A list of pygame.Rect which act as the barriers the rockets need to avoid
  target : tuple
    The x,y coordinates of the target circle the rockets need to reach

  """
  def __init__(self, width, height, pop_size): 
    """
    Parameters
    ----------
    width, height : int
      Width and height of pygame window
    pop_size : int
      Number of rockets in our population
    """
    self.width = width
    self.height = height
    self.screen = pygame.display.set_mode((self.width, self.height))
    self.message_coords = [self.width/2, 50]

    self.clock = pygame.time.Clock()
    self.cur_frame = 0
    self.running = False    
    self.population = Population(pop_size)
    self.barriers = []
    self.target = None

  def create_barriers(self):
    """ Contains loop that allows the user to click and drag to create rectangles. Due to pygame API, the first click the
    user makes represents the top left point of the rectangle. Thus the rectangle will invert when user drags their mouse 
    above or to the left of their initial click.
    """
    drawing = False
    start_pos = None

    # Draw rectangles loop
    while(True):
      self.screen.fill(BLACK)

      self.draw_barriers()
      self.population.rockets[0].display(self.screen)

      # Display instructions for user
      if not drawing:
        self.display_text("Click & Drag to create barriers", 
          self.message_coords, PRIMARY_FONT_SIZE)

        self.display_text("Press space when complete", 
          (self.message_coords[0], self.message_coords[1] + PRIMARY_FONT_SIZE), PRIMARY_FONT_SIZE) 

        self.display_text("Press U to undo barrier", 
          (self.message_coords[0], self.message_coords[1] + (PRIMARY_FONT_SIZE * 2)), SECONDAY_FONT_SIZE) 

      # Read in user events for determining rectangle placements
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          start_pos = event.pos
          drawing = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            return
          elif event.key == pygame.K_u:
            self.barriers.pop()

      rect = None
      if drawing and start_pos:
        current_pos = pygame.mouse.get_pos()
        top_left_x = min(start_pos[0], current_pos[0])
        top_left_y = min(start_pos[1], current_pos[1])
        width = abs(current_pos[0] - start_pos[0])
        height = abs(current_pos[1] - start_pos[1])
        pygame.draw.rect(self.screen, WHITE, (top_left_x, top_left_y, width, height))
        rect = pygame.Rect(top_left_x, top_left_y, width, height)

      if event.type == pygame.MOUSEBUTTONUP:
        drawing = False
        start_pos = None
        if rect:  
          self.barriers.append(rect)
        
      self.update()

  def place_target(self):
    """ Contains a loop that allows the user to place a target anywhere by clicking once on the screen.

    """
    while(True):
      self.screen.fill((0,0,0))

      self.draw_barriers()
      self.population.rockets[0].display(self.screen)

      self.display_text("Click to place target point", (self.width/2, 100), PRIMARY_FONT_SIZE)

      for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN:
          self.target = pygame.mouse.get_pos()
          return
      self.update()

  def draw_target(self):
    """ Function that draws target circle to screen
    """
    pygame.draw.circle(self.screen, WHITE, self.target, 10)

  def draw_barriers(self):
    """ Function that draws all the rectangle barriers to screen
    """
    if self.barriers:
      for barrier in self.barriers:
        pygame.draw.rect(self.screen, WHITE, barrier) 

  def display_text(self, text, coords, font_size):
    """ Contains pygame boiler place code for displaying text to screen

    Parameters
    ----------
    text : string 
      Text that will displayed to screen
    coords : list
      x,y coordinates of where the message will be located
    font_size : int
      Size of the messages font
    """
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(text, True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = coords

    self.screen.blit(text, textRect)

  def training_loop(self):
    """ The main loop where the rockets will evolve. This is infinite unless the user presses Q to quit the environment.
    """
    crashed_rockets = []

    while (self.running): 
      self.screen.fill(BLACK)

      # If max frames reached or all rockets crashed, evolve into the next 
      # population of rockets
      if self.cur_frame == 500 or len(self.population.rockets) == len(crashed_rockets):
        self.population.evalutate(self.target)
        self.population.selection()
        self.cur_frame = 0
        crashed_rockets = []

      # Check if user has pressed Q to quit
      for event in pygame.event.get():         
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            self.running = False

      # Perform several updates and state checks on the rockets.
      # Update location, check collision, draw to screen
      for rocket in self.population.rockets:
        if rocket.alive == True:
          rocket.decide_next_move(self.cur_frame)
        else:
          if rocket not in crashed_rockets:
            rocket.speed = 0
            crashed_rockets.append(rocket)

        rocket.check_collision(self.width, self.height, self.barriers)
        rocket.check_reached_target(self.target)
        rocket.update()
        if rocket.alive:
          rocket.display(self.screen)

      self.draw_target()
      self.draw_barriers()
      self.display_text("Press Q to quit", self.message_coords, SECONDAY_FONT_SIZE)
      
      self.cur_frame += 1
      self.update()

  def update(self):
    """ After each frame must specify fps and update the display
    """
    self.clock.tick(60)
    pygame.display.update()

  def run(self):
    """ Run the environment
    """
    self.running = True
    pygame.init()
    pygame.key.set_repeat(1000)

    self.create_barriers()
    self.place_target()
    self.training_loop()
      
    pygame.quit()
