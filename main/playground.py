import os

import util

MAP = [
    "#####----",
    "#H--#----",
    "#-BB#-###",
    "#-B-#-#T#",
    "###-###T#",
    "-##----T#",
    "-#---#--#",
    "-#---####",
    "-#####---"
]

print([["-"] * 12 for _ in range(12)])

result = [(i, j) for i, row in enumerate(MAP) for j, char in enumerate(row) if char == "B"]
for (i, j) in result:
    MAP[i] = MAP[i][:j] + "-" + MAP[i][j + 1:]


print(result)
print(MAP)
result2 = result[0] if len(result) > 0 else None
print(result2)

map_file = open('map/demo.txt', 'r')
print(map_file.read().splitlines())

print(util.get_resource_path('map'))

print([["-"] * 3 for _ in range(3)])

from datetime import datetime

current_time = datetime.now()
print(current_time.strftime("%Y%m%d%H%M"))

all_files = []

# 获取文件夹下的所有文件和文件夹名称
file_list = os.listdir(util.get_resource_path('map'))

# 遍历文件夹下的所有文件和文件夹
for file_name in file_list:
    # 获取文件（或文件夹）的完整路径
    full_path = os.path.join(util.get_resource_path('map'), file_name)

    # 如果是文件则加入all_files列表
    if os.path.isfile(full_path):
        all_files.append(full_path)

full_path = util.get_resource_path(all_files[0])
map_file = open(full_path, 'r')
print(map_file.name)


