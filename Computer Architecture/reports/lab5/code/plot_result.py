import matplotlib.pyplot as plt
import re
from matplotlib import font_manager

fontP = font_manager.FontProperties()
fontP.set_family('SongTi SC')


result = []
tmp_result = []
with open("cpu_result.txt", "r") as f:
    for line in f:
        if "testing" in line:
            result.append(tmp_result)
            tmp_result = []
            continue
        tmp_result.append(float(re.search(r'Time cost: (.*?)s\n', line).group()[11:-2]))
result.append(tmp_result)
result = result[1:]

# n = list(range(11))
n = list(range(7))
plt.plot(n, result[0][:-4], label="基础矩阵乘法")
plt.plot(n, result[1][:-4], label="AVX矩阵乘法")
plt.plot(n, result[2][:-4], label="AVX分块矩阵乘法")
# plt.plot(n, result[0])
# plt.plot(n, result[1])
# plt.plot(n, result[2])
plt.legend(prop=fontP)
# plt.show()
plt.savefig("cpu.jpg")
