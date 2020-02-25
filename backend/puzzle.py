from .graph import Graph
import random
import math
import copy

class Puzzle:

    def __init__(self, n = None, puzzle = None):
        if not n and not puzzle:
            raise ValueError

        self.n = n
        self.puzzle = puzzle

        if self.puzzle:
            self.n = self.valid_square_matrix(puzzle)

        if self.n < 0:
            raise ValueError

        self.minRow = 0
        self.minCol = 0
        self.maxRow = self.n - 1
        self.maxCol = self.n - 1

        self.start = 0
        self.goal = (self.n * self.n) - 1

        if not self.puzzle:
            self.fill()
        
    def __str__(self):
        if not self.puzzle:
            return ""
        res = "\n"
        for x in range(self.n):
            for y in range(self.n):
                res += '{:4}'.format(self.puzzle[x][y])
            res += "\n"
            
        return res

    def index_to_coord(self, index):
        row = index // self.n
        col = index % self.n

        if row > self.maxRow or row < self.minRow:
            return None, None

        if col > self.maxCol or col < self.minCol:
            return None, None

        return row, col

    def coord_to_index(self, row, col):
        if row > self.maxRow or row < self.minRow:
            return None
        if col > self.maxCol or col < self.minCol:
            return None

        return row * self.n + col

    def valid_square_matrix(self, puzzle):
        if not all(len(row) == len(puzzle) for row in puzzle):
            return -1
        return len(puzzle)

    def neighbors(self, row, col):
        if not self.puzzle:
            raise ValueError
        if row > self.maxRow or row < self.minRow:
            raise ValueError
        if col > self.maxCol or col < self.minCol:
            raise ValueError
        if row == self.maxRow and col == self.maxCol:
            return (None, None, None, None)

        el = self.puzzle[row][col]
        north = self.coord_to_index(row - el, col)
        south = self.coord_to_index(row + el, col)
        west = self.coord_to_index(row, col - el)
        east = self.coord_to_index(row, col + el)

        return (north, west, east, south)

    def random_legal_move(self, row, col):
        maxValue = max(
            self.maxRow - row,
            self.maxCol - col,
            row - self.minRow,
            col - self.minCol
        )
        return random.randint(1, maxValue)

    def fill(self):
        if self.puzzle:
            return

        self.puzzle = [[0 for _ in range(self.n)] for _ in range(self.n)]

        for row in range(self.n):
            for col in range(self.n):
                self.puzzle[row][col] = self.random_legal_move(row, col)
        self.puzzle[self.maxRow][self.maxCol] = 0

    def convert_to_graph(self):
        if not self.puzzle:
            raise ValueError

        graph = Graph({})
        for row in range(self.n):
            for col in range(self.n):
                graph.add_vertex(self.coord_to_index(row,col))

        for vertex in graph.vertices():
            neighbors = self.neighbors(*self.index_to_coord(vertex))
            neighbors = list(filter(lambda n: n is not None, neighbors))
            for neighbor in neighbors:
                graph.add_edge((vertex, neighbor))

        graph.adj_list[self.goal] = []

        return graph

    def evaluate_puzzle(self):
        g = self.convert_to_graph()
        path_length = g.get_path_length(self.start)
        unreachables = [idx for idx, el in enumerate(path_length) if el == float("Inf")]
        if self.goal in unreachables:
            return -1 * len(unreachables)
        return path_length[self.goal]

    def heuristic(self, vertex):
        row, col = self.index_to_coord(vertex)
        return (self.maxRow - row) + (self.maxCol - col)

    def hill_climbing(self, iterations):
        for _ in range(iterations):
            while True:
                random_row = random.randint(0,self.maxRow)
                random_col = random.randint(0,self.maxCol)
                if random_row != self.maxRow:
                    break
                if random_col != self.maxCol:
                    break
            
            current_value = self.puzzle[random_row][random_col]
            current_evaluation = self.evaluate_puzzle()
            random_legal_move = current_value

            while random_legal_move == current_value:
                random_legal_move = self.random_legal_move(random_row,random_col)

            self.puzzle[random_row][random_col] = random_legal_move
            new_evaluation = self.evaluate_puzzle()

            if new_evaluation == float("Inf") or new_evaluation < current_evaluation:
                self.puzzle[random_row][random_col] = current_value

    def breed(self, mother, father):
        progeny = []
        for i in range(self.n):
            row = random.choice((mother.puzzle[i], father.puzzle[i]))
            progeny.append(row)
        return Puzzle(puzzle=progeny)

    def get_population(self, size):
        population = []
        for _ in range(size):
            population.append(Puzzle(self.n))
        return population

    def genetic_algorithm(self, population_size, survival_rate, secondary_survival_rate, mutate_rate, epochs):
        population = self.get_population(population_size)
        for _ in range(epochs):
            evals = []
            for el in population:
                evals.append(el.evaluate_puzzle())
            temp = [p for _, p in sorted(
                zip(evals, population),
                key=lambda t:t[0],
                reverse=True
            )]

            visited = [False] * population_size
            survival_length = math.floor(population_size * survival_rate)
            survive = temp[:survival_length]
            secondary_survival_length = math.floor(population_size * secondary_survival_rate)
            for _ in range(secondary_survival_length):
                while True:
                    rand = random.randrange(survival_length, population_size)
                    if not visited[rand]:
                        break
                survive.append(temp[rand])
                visited[rand] = True

            visited = [False] * len(survive)
            mutate_length = math.floor(len(survive) * mutate_rate)
            for _ in range(mutate_length):
                while True:
                    rand = random.randrange(0,len(survive))
                    if not visited[rand]:
                        break
                survive[rand] = Puzzle(self.n)
                visited[rand] = True

            parent_generation_length = len(survive)
            while len(survive) < population_size:
                while True:
                    mother = random.randrange(0, parent_generation_length)
                    father = random.randrange(0, parent_generation_length)
                    if mother != father:
                        break
                progeny = self.breed(survive[mother], survive[father])
                survive.append(progeny)
            population = survive

        evals = []
        for el in population:
            evals.append(el.evaluate_puzzle())
        _, puzzle = max(zip(evals, population), key=lambda t: t[0])
        self.puzzle = puzzle.puzzle
