# Pygame Genetic Algorithm

## About the project
Developed a genetic algorithm that evolves a population of rockets to avoid user drawn barriers and reach a destination.
Used [Daniel Shiffman's 'Nature of Code'](https://natureofcode.com/book/chapter-9-the-evolution-of-code/) as a reference in developing the algorithm.

## Usage
Only pygame is required to run the program.
```sh
$ pip install pygame
```
Once in the project directory, the project can be run with
```sh
$ python main.py
```
Below is the contents of `main.py` where window size and number of rockets in the population can be altered.
```python
if __name__ == "__main__":
  width = 800
  height = 600
  pop_size = 50

  env = Environment(width, height, pop_size)
  env.run()
```
