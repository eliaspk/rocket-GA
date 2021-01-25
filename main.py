from environment import Environment

if __name__ == "__main__":
  width = 800
  height = 600
  pop_size = 50

  env = Environment(width, height, 50)
  env.run()