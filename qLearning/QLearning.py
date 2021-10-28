import itertools
import random
import numpy as np
from matplotlib import pyplot as plt


activity = ['stop', 'right', 'left', 'up', 'down']


def passable(maze, pos):  # 检查迷宫maze的位置pos是否可通行
    return maze[pos[0]][pos[1]] == 0


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


def plot_startandgoal():
    start = (1, 1)
    goal = (13, 13)
    plt.plot(start[1], start[0], "D", color="tab:red", markersize=10)
    plt.plot(goal[1], goal[0], "D", color="tab:green", markersize=10)


def random_search(maze, start, end):
    pos = start
    # print(start)
    repay = 0
    while pos != end:
        print((pos[1], pos[0]))
        select = random.randint(0, 4)
        print(select)
        if select == 0:
            pos = pos
        elif select == 1:
            # prePos = tuple(pos)
            pos[1] += 1
            if not passable(maze, pos):
                pos[1] -= 1
                repay -= -1
        elif select == 2:
            # prePos = tuple(pos)
            pos[1] -= 1
            if not passable(maze, pos):
                pos[1] += 1
                repay += -1
        elif select == 3:
            # prePos = tuple(pos)
            pos[0] -= 1
            if not passable(maze, pos):
                pos[0] += 1
                repay += -1
        else:
            # prePos = tuple(pos)
            pos[0] += 1
            if not passable(maze, pos):
                pos[0] -= 1
                repay += -1
        print(repay)

    print(end)
    repay += 10
    # print(repay)
    return repay

def create_qList(maze, start, end):
    # s, r, l, u, d
    QList = {tuple(start): [0, 0, 0, 0, 0]}
    pos = start
    # print(start)
    while pos != end:
        print(pos)
        select = random.randint(0, 4)
        print(select)
        if select == 0:
            pos = pos
            if tuple(pos) in QList:
                QList[tuple(pos)][0] = 0
            else:
                QList[tuple(pos)] = [0, 0, 0, 0, 0]
        elif select == 1:
            prePos = tuple(pos)
            pos[0] -= 1
            if pos == end:
                if prePos in QList:
                    QList[prePos][1] = 100
                else:
                    QList[prePos] = [0, 100, 0, 0, 0]
            if not passable(maze, pos):
                if prePos in QList:
                    QList[prePos][1] = -1
                else:
                    QList[prePos] = [0, -1, 0, 0, 0]
                pos[0] += 1
        elif select == 2:
            prePos = tuple(pos)
            pos[0] += 1
            if pos == end:
                if prePos in QList:
                    QList[prePos][2] = 100
                else:
                    QList[prePos] = [0, 0, 100, 0, 0]
            if not passable(maze, pos):
                if prePos in QList:
                    QList[prePos][2] = -1
                else:
                    QList[prePos] = [0, 0, -1, 0, 0]
                pos[0] -= 1
        elif select == 3:
            prePos = tuple(pos)
            pos[1] -= 1
            if pos == end:
                if prePos in QList:
                    QList[prePos][3] = 100
                else:
                    QList[prePos] = [0, 0, 0, 100, 0]
            if not passable(maze, pos):
                if prePos in QList:
                    QList[prePos][3] = -1
                else:
                    QList[prePos] = [0, 0, 0, -1, 0]
                pos[1] += 1
        else:
            prePos = tuple(pos)
            pos[1] += 1
            if pos == end:
                if prePos in QList:
                    QList[prePos][4] = 100
                else:
                    QList[prePos] = [0, 0, 0, 0, 100]
            if not passable(maze, pos):
                if prePos in QList:
                    QList[prePos][4] = -1
                else:
                    QList[prePos] = [0, 0, 0, 0, -1]
                pos[1] -= 1

    print(end)
    return QList


# def q_learing(QList, gama, )

if __name__ == "__main__":

    height = 15
    width = 15
    closelist = []
    start = (1, 1)
    end = (13, 13)
    while True:
        maze = make_maze(height, width)
        plot_maze(maze)
        plot_startandgoal()
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
    print(maze)
    start = [start[0], start[1]]
    end = [end[0], end[1]]
    plt.show()
    repay = random_search(maze, start, end)
    # print(repay)

