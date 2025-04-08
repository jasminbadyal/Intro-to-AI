trainingimages = "digitdata/trainingimages"

lines = []

with open(trainingimages, 'r') as file:
    for line in file:
        lines.append(line)

print(len(lines[19]))

