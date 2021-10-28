import itertools
import random
import numpy as np
from matplotlib import pyplot as plt
from queue import Queue

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 当前位置四个方向的偏移量


def mark(maze, pos):  # 给迷宫maze的位置pos标"2"表示“倒过了”
    maze[pos[0]][pos[1]] = 2


def passable(maze, pos):  # 检查迷宫maze的位置pos是否可通行
    return maze[pos[0]][pos[1]] == 0


def bfs(maze, start, end):
    if start == end:  # 若开始位置即为结束位置时，打印位置信息并返回
        print(start)
        return
    openlist = Queue()  # 申请一个队列
    path = list()
    parents = dict()
    mark(maze, start)  # 标记开始位置
    openlist.put(start)
    while not openlist.empty():
        pos = openlist.get()
        for i in range(0, 4):
            nextPos = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
            if passable(maze, nextPos):
                openlist.put(nextPos)
                mark(maze, nextPos)
                plt.quiver(pos[1], pos[0], (nextPos[1] - pos[1]), (nextPos[0] - pos[0]), angles='xy', scale_units='xy', scale=1)
                # print(pos, "->", nextPos)
                parents[nextPos] = pos
                if nextPos == end:
                    path.insert(0, end)
                    pointer = parents[end]
                    while pointer != start:
                        # print(pointer)
                        path.insert(0, pointer)
                        pointer = parents[pointer]

                    return path
        closelist.append(pos)
    return path

def make_maze(height, width):
    maze = np.zeros((height, width), dtype=int)

    # 上下左右の壁を設定
    maze[0, :] = 1
    maze[-1, :] = 1
    maze[:, 0] = 1
    maze[:, -1] = 1

    all_points = list(itertools.product(range(2, height - 2, 2), range(2, width - 2, 2)))

    while all_points:  # while all_points have element
        point = random.choice(all_points)
        wall_points = extend_wall(maze, point)
        for wp in wall_points:
            all_points.remove(wp)

    return maze


def extend_wall(maze, start):
    # left, right, up, down
    d_mat = np.array([[0, -2], [0, 2], [-2, 0], [2, 0]])
    wall_points = [start, ]
    wall_points_stack = [start, ]
    maze[start] = -1
    current = np.array(start)
    while True:
        next_v = np.array([maze[tuple(p)] for p in (current + d_mat)])
        if np.all(next_v == -1):
            current = np.array(wall_points_stack.pop())
            continue
        else:
            d_idx = random.choice(np.where(next_v != -1)[0])
            maze[tuple(current + (d_mat[d_idx] // 2))] = -1
            p = tuple(current + d_mat[d_idx])
            if maze[p] == 1:
                break
            maze[p] = -1
            wall_points.append(p)
            wall_points_stack.append(p)
            current = current + d_mat[d_idx]

    maze[maze == -1] = 1
    return wall_points


def plot_maze(maze_map, save_file=None):
    height, width = maze_map.shape
    plt.imshow(maze_map, cmap="binary")
    plt.xticks(rotation=90)
    plt.xticks(np.arange(width), np.arange(width))
    plt.yticks(np.arange(height), np.arange(height))

    plt.gca().set_aspect('equal')
    if save_file is not None:
        plt.savefig(save_file)
    else:
        # plt.show()
        pass


def plot_startandgoal(maze_map):
    start = (1, 1)
    goal = (13, 13)
    plt.plot(start[1], start[0], "D", color="tab:red", markersize=10)
    plt.plot(goal[1], goal[0], "D", color="tab:green", markersize=10)


if __name__ == "__main__":

    height = 15
    width = 15
    closelist = []
    start = (1, 1)
    end = (13, 13)
    while True:
        maze = make_maze(height, width)
        plot_maze(maze)
        plot_startandgoal(maze)
        if input("この迷路を保存しますか？ (y/n) >> ") == "y":
            name = input("迷路の名前(.txtを除く) >> ")
            np.savetxt(f"{name}.txt", maze, fmt="%d")
            plot_maze(maze, save_file=f"{name}.png")
            print(f"作成した迷路を{name}.pngと{name}.txtに保存しました．")
        print()
        if input("同じ条件でもう一度迷路を生成しますか？ (y/n) >> ") == "y":
            continue
        else:
            break

    # plt.show()
    path = bfs(maze, start, end)
    # print(path)
    for i in range(len(path)):
        if i == len(path) - 1:
            print(path[i])
        else:
            print(path[i], end="->")

    plt.show()