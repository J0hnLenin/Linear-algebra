import math
def cross_line_plane(line, plane, size):

    mtx = []
    for i in range(size):
        mtx.append([[- line[1][i], plane[1][i], plane[2][i]], [line[0][i] - plane[0][i]]])

    for i in range(size):
        print(mtx[i])
    print()

    mtx = Gauss(mtx, size)

    for i in range(size):
        print(mtx[i])
    print()

    C = []
    for i in range(size):
        C.append(line[0][i] + line[1][i] * mtx[0][1][0])

    return C
def cross_line_line(line1, line2, size):

    if parallel(line1, line2, size) == True:
        return 'прямые параллельны'

    mtx = []
    for i in range(size):
        mtx.append([[- line1[1][i], line2[1][i]], [line1[0][i] - line2[0][i]]])

    for i in range(size):
        print(mtx[i])
    print()
    mtx = Gauss(mtx, 2)

    for i in range(size):
        print(mtx[i])
    print()
    a = mtx[0][1][0]
    b = mtx[1][1][0]

    if (-a*line1[1][2] + b*line2[1][2]) == (line1[0][2] - line2[0][2]):
        C = []
        for i in range(size):
            C.append(line1[0][i] + a*line1[1][i])
        return C

    return 'прямые скрещивающиеся'
def do_zero(mtx_line1, mtx_line2, i):


    if mtx_line1[0][i] == 0:
        return mtx_line2
    x = (- mtx_line2[0][i])/mtx_line1[0][i]

    for j in range(len(mtx_line2[0])):
        mtx_line2[0][j] += mtx_line1[0][j] * x

    mtx_line2[1][0] += mtx_line1[1][0] * x
    return mtx_line2
def do_one(mtx_line1, i):
    if mtx_line1[0][i] == 0:
        return mtx_line1
    if mtx_line1[0][i] != 1:
        x = mtx_line1[0][i]

        for k in range(len(mtx_line1[0])):

            mtx_line1[0][k] *= 1/x

        mtx_line1[1][0] *= 1/x
    for j in range(len(mtx_line1[0])):
        if mtx_line1[0][j] == -0.0:
            mtx_line1[0][j] = 0

    return mtx_line1
def Gauss(mtx, size):
    for i in range(size - 1):
        for j in range(i + 1, size):
            mtx[j] = do_zero(mtx[i], mtx[j], i)

    for i in range(1, size):
        for j in range(size - i):
            mtx[j] = do_zero(mtx[-i], mtx[j], -i)


    for i in range(size):
        mtx[i] = do_one(mtx[i], i)


    return mtx
def parallel(line1, line2, size):
    if line1[1][0] == 0 and line2[1][0] != 0:
        return False
    if line1[1][0] != 0 and line2[1][0] == 0:
        return False
    if line1[1][0] == 0 and line2[1][0] == 0:
        if line1[1][1] == 0 and line2[1][1] != 0:
            return False
        if line1[1][1] != 0 and line2[1][1] == 0:
            return False
        if line1[1][1] == 0 and line2[1][1] == 0:
            return True
        else:
            x = abs(line1[1][1] / line2[1][1])
            if (x != abs(line1[1][2] / line2[1][2])):
                return False
            return True

    else:
        x = abs(line1[1][0] / line2[1][0])
        for i in range(1, size):
            if (x != abs(line1[1][i] / line2[1][i])):
                return False
        return True
def scalar_mult(v1, v2):
    x = 0
    for i in range(len(v1)):
        x += v1[i] * v2[i]
    return x
def vector_modul(v0):
    return scalar_mult(v0, v0) ** (1/2)
def perpend_line_line(line1, line2, size):
    if cross_line_line(line1, line2, size) != 'прямые скрещивающиеся' and cross_line_line(line1, line2, size) != 'прямые параллельны':
        if scalar_mult(line1[1], line2[1]) == 0:
            return True
    return False
def angle_radian_vector_vector(v1, v2):
    return math.acos(scalar_mult(v1, v2) / (vector_modul(v1) * vector_modul(v2)))


# size - кол-во измерений
# точку (A, B...) или вектор (v0, v1...) задаю массивом [x, y, z]
# Прямую задаю через точку и вектор, плоскость через точку и два вектора
# Gauss применяет метод Гаусса на матрицу
#





size = 3
A = [0, 0, 0]
B = [0, 0, 0]
v0 = [0, 0, 1]
v1 = [0, 3, 0]
v2 = [2, 0, -1]

line1 = [A, v0]
line2 = [B, v1]
plane = [B, v1, v2]


