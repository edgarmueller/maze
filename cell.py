from point import Point
from line import Line


class Cell:
    def __init__(self, p1, p2, col, row, window=None):
        self.__window = window
        self.p1 = p1
        self.p2 = p2
        self.col = col
        self.row = row
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.visited = False

    def neighbors(self, maze):
        neighbors = []
        if self.row > 0:
            neighbors.append(maze[self.col][self.row - 1])
        if self.col < len(maze) - 1:
            neighbors.append(maze[self.col + 1][self.row])
        if self.row < len(maze[0]) - 1:
            neighbors.append(maze[self.col][self.row + 1])
        if self.col > 0:
            neighbors.append(maze[self.col - 1][self.row])
        return neighbors

    def draw(self):
        if self.__window is None:
            return
        top_color = "black" if self.has_top_wall else "white"
        right_color = "black" if self.has_right_wall else "white"
        bottom_color = "black" if self.has_bottom_wall else "white"
        left_color = "black" if self.has_left_wall else "white"
        self.__window.draw_line(
            Line(Point(self.p1.x, self.p1.y), Point(self.p2.x, self.p1.y)), top_color
        )
        self.__window.draw_line(
            Line(Point(self.p2.x, self.p1.y), Point(self.p2.x, self.p2.y)), right_color
        )
        self.__window.draw_line(
            Line(Point(self.p2.x, self.p2.y), Point(self.p1.x, self.p2.y)), bottom_color
        )
        self.__window.draw_line(
            Line(Point(self.p1.x, self.p2.y), Point(self.p1.x, self.p1.y)), left_color
        )

    def draw_move(self, to_cell, undo=False):
        color = "red" if not undo else "white"
        w = max(self.p1.x, self.p2.x) - min(self.p1.x, self.p2.x)
        h = max(self.p1.y, self.p2.y) - min(self.p1.y, self.p2.y)
        center = Point(self.p1.x + (w / 2), self.p1.y + (h / 2))
        to_center = Point(to_cell.p1.x + (w / 2), to_cell.p1.y + (h / 2))
        self.__window.draw_line(Line(center, to_center), color)
