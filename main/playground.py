import copy

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
result = [(i, j) for i, row in enumerate(MAP) for j, char in enumerate(row) if char == "B"]

print(result)

map_file = open('map/demo.txt', 'r')
print(map_file.read().splitlines())
