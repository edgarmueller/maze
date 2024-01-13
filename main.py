from window import Window
from maze import Maze


def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 10, 10, 50, 50, 0, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
