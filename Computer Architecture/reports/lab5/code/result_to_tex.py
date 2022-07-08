import re


result = []
tmp_result = []
with open("cpu_result.txt", "r") as f:
    for line in f:
        if "testing" in line:
            result.append(tmp_result)
            tmp_result = []
            continue
        tmp_result.append(re.search(r'Time cost: (.*?)s\n', line).group()[11:-2])
result.append(tmp_result)
result = result[1:]

tex_table = """\hline
n & 基础矩阵乘法/s & AVX矩阵乘法/s & AVX分块矩阵乘法/s \\\\
\hline
"""
for n in range(11):
    tex_table += f"{n} & {result[0][n]} & {result[1][n]} & {result[2][n]} \\\\\n"
tex_table += "\hline"
print(tex_table)
