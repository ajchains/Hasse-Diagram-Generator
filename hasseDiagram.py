import matplotlib.pyplot as plt


def find_floor(element, floors):
    return [floors.index(floor) for floor in floors if element in floor][0]


def find_sup(subset, relations, floors):
    # upper bound
    temp = []
    ub = []
    sup = False
    for i in subset:
        rel = []
        rel.append(i)
        for j in rel:
            for k in relations:
                if k[0] == j:
                    rel.append(k[1])
        temp.extend(rel)

    for i in range(len(temp)):
        count = 0
        for j in range(len(temp)):
            if temp[i] == temp[j]:
                count += 1
        if count >= len(subset):
            if temp[i] not in ub:
                ub.append(temp[i])

    for i in ub:
        count = 0
        floorI = find_floor(i, floors)
        for j in ub:
            if floorI < find_floor(j, floors):
                count += 1
        if count == (len(ub)-1):
            sup = i
    return sup


def find_inf(subset, relations, floors):
    lb = []
    temp = []
    inf = False

    for i in subset:
        rel = []
        rel.append(i)
        for j in rel:
            for k in relations:
                if k[1] == j:
                    if k[0] not in rel:
                        rel.append(k[0])

        temp.extend(rel)
    for i in range(len(temp)):
        count = 0
        for j in range(len(temp)):
            if temp[i] == temp[j]:
                count += 1
        if count >= len(subset):
            if temp[i] not in lb:
                lb.append(temp[i])
    for i in lb:
        count = 0
        for j in lb:
            if find_floor(i, floors) > find_floor(j, floors):
                count += 1
        if count == (len(lb)-1):
            inf = i
    return inf


def getDiagram(poset, relations, filename):
    try:
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
                label.append("  " + str(floors[i][j]))

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

        # Lattice Checker
        problem = []
        for i in poset:
            lattice = True
            for j in poset:
                subset = [i, j]
                if find_inf(subset, relations, floors) and find_sup(subset, relations, floors):
                    continue
                else:
                    problem = [
                        [i, j], [find_inf(subset, relations), find_sup(subset, relations, floors)]]
                    lattice = False
            if lattice == True:
                continue
            else:
                print("not a lattice", problem)
                break
        if lattice == True:
            print("It is a Lattice")

        return lattice

    except Exception as e:
        print(f"An error occured{e}")
        print("error")
        return "Error"
