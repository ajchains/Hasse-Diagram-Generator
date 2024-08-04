import matplotlib.pyplot as plt


def getDiagram(poset, relations, filename):
    floors = []
    numbers_checked = []

    # Assign each element to its floor
    for i in range(len(poset)):
        if len(numbers_checked) < len(poset):
            if len(floors) == 0:  # Logic for the first floor
                first_floor = []
                for i in range(len(poset)):
                    valid = True
                    for j in range(len(relations)):
                        if relations[j][1] == poset[i]:
                            valid = False
                            break
                    if valid:
                        first_floor.append(poset[i])
                        numbers_checked.append(poset[i])
                floors.append(first_floor)
            else:  # Logic for subsequent floors
                floor = []
                for i in range(len(poset)):
                    valid = True
                    if poset[i] not in numbers_checked:
                        for j in range(len(relations)):
                            if relations[j][1] == poset[i]:
                                if relations[j][0] not in numbers_checked:
                                    valid = False
                                    break
                        if valid:
                            floor.append(poset[i])
                numbers_checked.extend(floor)
                floors.append(floor)

    x = []
    y = []
    coords = {}
    label = []

    # Generate x and y values for plotting
    for i in range(len(floors)):
        for j in range(len(floors[i])):
            x.append(j)
            y.append(i)
            coords[str(floors[i][j])] = [j, i]
            label.append(" " + str(floors[i][j]))

    lines = []

    # Find lines connecting elements
    for i in range(len(poset)):
        floor_number = [floors.index(floor)
                        for floor in floors if poset[i] in floor][0]
        for j in range(len(relations)):
            if relations[j][0] == poset[i] and relations[j][1] in floors[floor_number + 1]:
                lines.append(relations[j])

    fig, ax = plt.subplots()
    ax.scatter(x, y, color='#FE9000')  # Plot elements

    for i, txt in enumerate(label):
        ax.annotate(txt, (x[i], y[i]), color='#FFFFFF')  # Label elements

    for line in lines:
        ax.plot([coords[str(line[0])][0], coords[str(line[1])][0]],
                [coords[str(line[0])][1], coords[str(line[1])][1]],
                color="#80FFEC")  # Plot lines

    fig.set_facecolor('#181c25')
    plt.axis('off')
    fig.savefig(filename)
