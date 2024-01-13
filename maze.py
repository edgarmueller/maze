import random
from point import Point
from cell import Cell
import time


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, seed=None, win=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for col in range(self._num_cols):
            curr_col = []
            for row in range(self._num_rows):
                p1 = Point(
                    self._x1 + col * self._cell_size_x,
                    self._y1 + row * self._cell_size_y,
                )
                p2 = Point(p1.x + self._cell_size_x, p1.y + self._cell_size_y)
                cell = Cell(p1, p2, col, row, self._win)
                curr_col.append(cell)
            self._cells.append(curr_col)
        for row in self._cells:
            for cell in row:
                cell.draw()

    def _animate(self):
        for row in self._cells:
            for cell in row:
                cell.draw()
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left = self._cells[0][0]
        top_left.has_top_wall = False
        top_left.has_left_wall = False

        bottom_right = self._cells[-1][-1]
        bottom_right.has_right_wall = False
        bottom_right.has_bottom_wall = False

        self._animate()

    def _break_walls_r(self, i, j):
        curr_cell = self._cells[i][j]
        curr_cell.visited = True
        while True:
            neighbors = curr_cell.neighbors(self._cells)
            non_visited_neighbors = [
                neighbor for neighbor in neighbors if not neighbor.visited
            ]
            if len(non_visited_neighbors) == 0:
                curr_cell.draw()
                break
            random_dir = random.randrange(len(non_visited_neighbors))
            next_cell = non_visited_neighbors[random_dir]
            # knock down walls
            if next_cell.col > curr_cell.col:
                curr_cell.has_right_wall = False
                next_cell.has_left_wall = False
            elif next_cell.col < curr_cell.col:
                curr_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif next_cell.row > curr_cell.row:
                curr_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            elif next_cell.row < curr_cell.row:
                curr_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            self._break_walls_r(next_cell.col, next_cell.row)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        self._solve_r(self._cells[0][0])

    def _solve_r(self, cell):
        self._animate()
        cell.visited = True
        if cell.col == len(self._cells) - 1 and cell.row == len(self._cells[0]) - 1:
            return True
        neighbors = cell.neighbors(self._cells)
        non_visited_neighbors = [
            neighbor for neighbor in neighbors if not neighbor.visited
        ]
        for n in non_visited_neighbors:
            cell.draw_move(n)
            can_go_up = n.row > cell.row and not cell.has_bottom_wall
            can_go_right = n.col > cell.col and not cell.has_right_wall
            can_go_down = n.row < cell.row and not cell.has_top_wall
            can_go_left = n.col < cell.col and not cell.has_left_wall

            if can_go_up or can_go_right or can_go_down or can_go_left:
                if self._solve_r(n):
                    return True
                else:
                    cell.draw_move(n, undo=True)
            else:
                cell.draw_move(n, undo=True)
        return False
