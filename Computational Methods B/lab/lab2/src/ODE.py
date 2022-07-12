import argparse
import enum
import matplotlib.pyplot as plt
import numpy as np


def euler():
    parser = argparse.ArgumentParser(
        description="Euler's formula for solving ordinary differential equations")
    parser.add_argument("-f", "--forward")
    args = parser.parse_args()


def forward_euler(start, end, step_length, init_value):
    # x = np.arange(start, end + step_length, step_length)
    x = np.asarray([start + i * step_length for i in range(int((end - start) / step_length) + 1)])
    y = np.zeros(len(x))
    y[0] = init_value
    for i in range(0, len(x) - 1):
        y[i + 1] = y[i] + step_length * (-100 * y[i])
    return x, y


def backward_euler(start, end, step_length, init_value):
    # x = np.arange(start, end + step_length, step_length)
    x = np.asarray([start + i * step_length for i in range(int((end - start) / step_length) + 1)])
    y = np.zeros(len(x))
    y[0] = init_value
    for i in range(0, len(x) - 1):
        # 预估校正
        # y_bar = y[i] + step_length * (-100 * y[i])
        # y[i + 1] = y[i] + step_length * (-100 * y_bar)
        # y[i + 1] = y[i] + step_length * ((-100 * y_bar) + (-100) * y[i]) / 2
        y[i+1] = y[i] / (100 * step_length + 1)
    return x, y


def central_difference(start, end, step_length, init_value):
    # x = np.arange(start, end + step_length, step_length)
    x = np.asarray([start + i * step_length for i in range(int((end - start) / step_length) + 1)])
    y = np.zeros(len(x))
    # forward Euler for y1
    y[0] = init_value
    y[1] = y[0] + step_length * (-100 * y[0])
    for i in range(1, len(x) - 1):
        y[i + 1] = y[i - 1] + 2 * step_length * (-100 * y[i])
    return x, y


if __name__ == "__main__":
    # fig, ax = plt.subplots()
    # x = np.arange(0, 0.2, 0.0001)
    # y = np.exp(-100 * x)
    # ax.plot(x, y, label="Accurte Result")

    start = 0
    end = 0.2
    # h = 1 / 80
    y0 = 1
    y_true = np.exp(-100 * 0.2)
    error = np.zeros(4)
    order = np.zeros(3)
    # for h in [1 / 10, 1 / 20, 1 / 40, 1 / 80]:
    # for h in [1 / 80]:
    for i, h in enumerate([1 / 10, 1 / 20, 1 / 40, 1 / 80]):

        # forward Euler
        # x, y = forward_euler(start, end, h, y0)
        # ax.plot(x, y, label=f"Forward Euler Result(h = {h})")

        # backward Euler
        x, y = backward_euler(start, end, h, y0)
        # ax.plot(x, y, label=f"Backward Euler Result(h = {h})")

        # central difference
        # x, y = central_difference(start, end, h, y0)
        # ax.plot(x, y, label=f"Central Difference(h = {h})")

        error[i] = (np.abs(y_true - y[-1]))
    print(error)
    for i in range(3):
        order[i] = np.log2(error[i] / error[i + 1])
    print(order)

    # ax.legend()
    # plt.savefig("./forward_euler.jpg")
    # plt.savefig(f"../fig/forward_euler_h_{h}.jpg")
    # plt.savefig("./backward_euler.jpg")
    # plt.savefig("./central_difference.jpg")
    # plt.savefig(f"../fig/central_difference_h_{h}.jpg")
    # plt.show()
