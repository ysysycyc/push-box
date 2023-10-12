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

print(util.get_resource_path('map/demo.txt'))

print([["-"] * 3 for _ in range(3)])
