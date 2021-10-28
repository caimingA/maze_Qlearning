import itertools
import random
import numpy as np
from matplotlib import pyplot as plt


# draw the arrow
def plot_path(closelist):
    # p -> q の矢印をプロットする
    for i in range(len(closelist) - 1):
        p = [closelist[i][0], closelist[i][1]]
        q = [closelist[i + 1][0], closelist[i + 1][1]]
        print(p)
        print(q)
        plt.quiver(p[1], p[0], (q[1] - p[1]), (q[0] - p[0]), angles='xy', scale_units='xy', scale=1)
        # plt.quiver(i + 1, 1, 1, 0, angles='xy', scale_units='xy', scale=1)

    plt.show()


# change to np array
def getpath(closelist):
    x = 2
    for i in range(len(closelist)):
        closelist[i] = np.array(closelist[i])


dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 当前位置四个方向的偏移量
path_maze = []  # 存找到的路径


class Stack:
    def __init__(self):
        self.values = []

    def push(self, value):
        self.values.append(value)

    def pop(self):
        return self.values.pop()

    def is_empty(self):
        return self.size() == 0

    def size(self):
        return len(self.values)

    def peak(self):
        return self.values[self.size() - 1]


def mark(maze, pos):  # 给迷宫maze的位置pos标"2"表示“倒过了”
    maze[pos[0]][pos[1]] = 2


def passable(maze, pos):  # 检查迷宫maze的位置pos是否可通行
    return maze[pos[0]][pos[1]] == 0


def dfs(maze, start, end):
    if start == end:  # 若开始位置即为结束位置时，打印位置信息并返回
        print(start)
        return
    openlist = Stack()  # 申请一个栈对象,栈的实现请查看https://blog.csdn.net/weixin_39781462/article/details/82290886
    path = Stack()
    # closelist = []
    mark(maze, start)  # 标记开始位置
    openlist.push((start, 0))  # 开始位置入栈
    while not openlist.is_empty():  # 直到栈内元素为空才出循环
        pos, nxt = openlist.pop()  # 取出栈中元素
        for i in range(nxt, 4):  # 取
            nextp = (pos[0] + dirs[i][0],  # 下一个要处理的位置
                     pos[1] + dirs[i][1])
            if passable(maze, nextp):  # 位置元素满足通过要求
                openlist.push((pos, i + 1))  # 位置入栈--存入栈的是序对(pos.nxt)，其中分支点位置用pos(行列坐标对)表示，nxt是正数表示回溯到该位置后需要探索的下一位置方向
                mark(maze, nextp)  # 标记位置
                ##### chenge #####
                plt.quiver(pos[1], pos[0], (nextp[1] - pos[1]), (nextp[0] - pos[0]), angles='xy', scale_units='xy', scale=1)
                ##### chenge #####
                # plt.quiver(p[1], p[0], (q[1] - p[1]), (q[0] - p[0]), angles='xy', scale_units='xy', scale=1)
                openlist.push((nextp, 0))  # 位置入栈
                if nextp == end:  # 位置为end时，输出栈内元素，即为寻找的路径
                    while not openlist.is_empty():
                        path.push(openlist.peak())
                        openlist.pop()
                    break  # 退出内层循环，下次迭代将以新栈顶为当前位置继续
    while not path.is_empty():
        # print(closelist.pop()[0])
        closelist.append(tuple(path.pop()[0]))

    return


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
    dfs(maze, start, end)

    print(closelist)

    getpath(closelist)

    # plot_path(closelist)

    plt.show()
    # plot_path(closelist)