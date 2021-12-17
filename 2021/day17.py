
def get_vx_values(_min, _max):
    values = []
    for x in range(_max+1):
        t = x
        sum = x
        # print(sum)
        while sum <= _max and x > 0:
            if _min <= sum <= _max:
                values.append(t)
                break
            x -= 1
            sum += x
    return values


def get_vy_values(_min, _max):
    values = set()

    for y in range(_min, 1):
        values.add(-(y+1))
        k = y
        sum = y
        while _min <= sum and y >= _min:
            if _min <= sum <= _max:
                values.add(k)
                break
            y -= 1
            sum += y
    return list(values)


def is_valid(vX, vY, _minX, _maxX, _minY, _maxY):
    currX = 0
    currY = 0

    while _minY <= vY:
        currX += vX
        currY += vY
        if _minX <= currX <= _maxX and _minY <= currY <= _maxY:
            return True

        vY -= 1
        if vX != 0:
            vX -= 1

    return False


if __name__ == "__main__":
    (minX, maxX) = (179, 201)
    (minY, maxY) = (-109, -63)
    total_vXs = get_vx_values(minX, maxX)
    total_vYs = get_vy_values(minY, maxY)
    valid = []
    for x in total_vXs:
        for y in total_vYs:
            if is_valid(x, y, minX, maxX, minY, maxY):
                valid.append((x, y))

    print(len(valid))
