import argparse

parser = argparse.ArgumentParser()

parser.add_argument("input", help = "input .csv file")
parser.add_argument("output", help = "output .md file")
parser.add_argument("--separator", "-s", default = ";", help = "separator")

args = parser.parse_args()

input = open(args.input, "r")
output = open(args.output, "w")

lines = input.readlines()
cells = []

for i, line in enumerate(lines):
    line = line.rstrip()
    cells.append(line.split(args.separator))
    if i == 0:
        ncols = len(cells[0])
        colsize = [3 for j in range(ncols)]
    
    colsize = [max(colsize[j], len(cells[i][j])) for j in range(ncols)]

for i, row in enumerate(cells):
    for j in range(ncols):
        output.write("| " + row[j] + " " * (1+colsize[j]-len(row[j])))
    output.write("|\n")
    if i == 0:
        for s in colsize:
            output.write("| " + "-"*s + " ")
        output.write("|\n")
    

input.close()
output.close()