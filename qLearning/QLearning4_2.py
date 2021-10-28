import itertools
import random
import numpy as np
from matplotlib import pyplot as plt


activity = ['stop', 'right', 'left', 'up', 'down']
QTable = dict()
RTable = dict()


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
    goal = (7, 7)
    plt.plot(start[1], start[0], "D", color="tab:red", markersize=10)
    plt.plot(goal[1], goal[0], "D", color="tab:green", markersize=10)


def random_search(maze, start, end):
    pos = start
    # print(start)
    repay = 0
    while pos != end:
        print(pos)
        select = random.randint(0, 4)
        print(select)
        if select == 0:
            pos = pos
        elif select == 1:
            # prePos = tuple(pos)
            pos[0] -= 1
            if not passable(maze, pos):
                pos[0] += 1
                repay += -1
        elif select == 2:
            # prePos = tuple(pos)
            pos[0] += 1
            if not passable(maze, pos):
                pos[0] -= 1
                repay += -1
        elif select == 3:
            # prePos = tuple(pos)
            pos[1] -= 1
            if not passable(maze, pos):
                pos[1] += 1
                repay += -1
        else:
            # prePos = tuple(pos)
            pos[1] += 1
            if not passable(maze, pos):
                pos[1] -= 1
                repay += -1

    print(end)
    repay += 10
    return repay


# 初始化Q值表和R值表
def QTable_init(maze, end):
    for i in range(len(maze)):
        for j in range(len(maze)):
            if passable(maze, (i, j)):
                QTable[(i, j)] = [0, 0, 0, 0, 0]
                RTable[(i, j)] = [0, 0, 0, 0, 0]
                for k in range(4):
                    if k == 0:  # right
                        if not passable(maze, (i, j + 1)):
                            RTable[(i, j)][1] = -1
                        if [i, j + 1] == end:
                            RTable[(i, j)][1] = 10
                    elif k == 1:  # left
                        if not passable(maze, (i, j - 1)):
                            RTable[(i, j)][2] = -1
                        if [i, j - 1] == end:
                            RTable[(i, j)][2] = 10
                    elif k == 2:  # up
                        if not passable(maze, (i - 1, j)):
                            RTable[(i, j)][3] = -1
                        if [i - 1, j] == end:
                            RTable[(i, j)][3] = 10
                    else:
                        if not passable(maze, (i + 1, j)):
                            RTable[(i, j)][4] = -1
                        if [i + 1, j] == end:
                            RTable[(i, j)][4] = 10


def get_index(lst=None, item=''):
    return [index for (index, value) in enumerate(lst) if value == item]


def q_learning(maze, gamma, alpha, start, end, N):
    V = list()
    pos = start  # pos is list()
    act = random.randint(0, 4)
    print(act)
    while pos != end:
        print((pos[1], pos[0]), "|", act, "|", QTable[tuple(pos)], "|", RTable[tuple(pos)])
        V.append(max(QTable[tuple(pos)]))
        if act == 0:  # stop
            posNext = tuple(pos)
            posNow = tuple(pos)
            indexList = get_index(QTable[posNext], max(QTable[posNext]))
            index = indexList[random.randint(0, len(indexList) - 1)]
            # print(QTable[posNext])
            R = RTable[posNow][act]
            reality = gamma * QTable[posNow][index]
            estimation = QTable[posNow][act]
            QTable[posNow][act] = estimation + alpha * (R + reality - estimation)

            act = index
        elif act == 1:  # right
            posNext = tuple([pos[0], pos[1] + 1])
            posNow = tuple(pos)
            if passable(maze, posNext):
                indexList = get_index(QTable[posNext], max(QTable[posNext]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                # print(QTable[posNext])
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
            else:
                posNext = posNow
                indexList = get_index(QTable[posNow], max(QTable[posNow]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
        elif act == 2:  # left
            posNext = tuple([pos[0], pos[1] - 1])
            posNow = tuple(pos)
            if passable(maze, posNext):
                indexList = get_index(QTable[posNext], max(QTable[posNext]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                # print(QTable[posNext])
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
            else:
                posNext = posNow
                indexList = get_index(QTable[posNow], max(QTable[posNow]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
        elif act == 3:
            posNext = tuple([pos[0] - 1, pos[1]])
            posNow = tuple(pos)
            if passable(maze, posNext):
                indexList = get_index(QTable[posNext], max(QTable[posNext]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                # print(QTable[posNext])
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
            else:
                posNext = posNow
                indexList = get_index(QTable[posNow], max(QTable[posNow]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
            # index = QTable[posNext].index(max(QTable[posNext]))
        else:
            posNext = tuple([pos[0] + 1, pos[1]])
            posNow = tuple(pos)
            if passable(maze, posNext):
                indexList = get_index(QTable[posNext], max(QTable[posNext]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                # print(QTable[posNext])
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
            else:
                posNext = posNow
                indexList = get_index(QTable[posNow], max(QTable[posNow]))
                index = indexList[random.randint(0, len(indexList) - 1)]
                R = RTable[posNow][act]
                reality = gamma * QTable[posNext][index]
                estimation = QTable[posNow][act]
                QTable[posNow][act] = estimation + alpha * (R + reality - estimation)
                pos = list(posNext)
                act = index
    print((pos[1], pos[0]))
    # V.append(max(QTable[tuple(pos)]))
    x = [i + 1 for i in range(len(V))]
    plt.plot(x, V)
    x_axis = "移動回数"
    y_axis = "評価値"
    title = "第" + str(N + 1) + "回"
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    plt.show()



if __name__ == "__main__":

    height = 9
    width = 9
    closelist = []
    start = (1, 1)
    end = (7, 7)
    maze = make_maze(height, width)
    plot_maze(maze)
    plot_startandgoal()
    print(maze)
    start = [start[0], start[1]]
    end = [end[0], end[1]]
    # repay = random_search(maze, start, end)
    # print(repay)
    QTable_init(maze, end)
    plt.show()
    L = 100
    for i in range(L):
        q_learning(maze, 0.9, 0.1, start, end, i)
    # plt.show()

