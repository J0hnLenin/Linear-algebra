import math


"""
Файл создан для решения стереометрических задач через параметрические координаты.
size - кол-во измерений или размер матрицы (по умолчнию 3).
точка (point_A, point_B...) или вектор (vector0, vector1...) задётся списком [x, y, z].
Прямая задётся через точку и вектор, плоскость через точку и два вектора.
"""


def gauss(matrix, size):
    """ Применяет метод Гаусса к матрице. """

    def create_ok_list(matrix, size):
        """ Создаёт список - какая строка матрицы может встать на какое место. """

        ok_list = []
        for i in range(size):
            ok_list.append([])

        for i in range(size):
            for j in range(size):
                if matrix[j][0][i] != 0:
                    ok_list[i].append(j)

        return ok_list

    def distribution(ok_list, size, stack):
        """ Выдаёт список с верной расстановкой строк или False, если нет решений. """
        line_number = len(stack)
        if ok_list[line_number] == []:
            return False
        for i in ok_list[line_number]:
            if stack.count(i) == 0:
                stack.append(i)
                if line_number == size - 1:
                    return stack
                answer = distribution(ok_list, size, stack)
                if answer != False:
                    return answer
                stack.remove(i)
        return False

    def reverse(matrix, correct_list, size):
        """ Переставляет строки матрицы на места из correct_list."""
        new_matrix = []
        for i in range(size):
            new_matrix.append(matrix[correct_list[i]])
        return new_matrix



    def do_zero(matrix_line1, matrix_line2, i):
        if matrix_line1[0][i] == 0:
            return matrix_line2
        x = (- matrix_line2[0][i]) / matrix_line1[0][i]

        for j in range(len(matrix_line2[0])):
            matrix_line2[0][j] += matrix_line1[0][j] * x

        matrix_line2[1][0] += matrix_line1[1][0] * x
        return matrix_line2

    def do_one(matrix_line1, i):
        if matrix_line1[0][i] == 0:
            return matrix_line1
        if matrix_line1[0][i] != 1:
            x = matrix_line1[0][i]

            for k in range(len(matrix_line1[0])):
                matrix_line1[0][k] *= 1 / x

            matrix_line1[1][0] *= 1 / x
        for j in range(len(matrix_line1[0])):
            if matrix_line1[0][j] == -0.0:
                matrix_line1[0][j] = 0

        return matrix_line1

    ok_list = create_ok_list(matrix, size)
    stack = []
    correct_list = distribution(ok_list, size, stack)
    if correct_list == False:
        #решений нет
        return False
    matrix = reverse(matrix, correct_list, size)

    # теперь на диагонали matrix[i][0][i], i in range(size) нет нулей

    for i in range(size - 1):
        for j in range(i + 1, size):
            matrix[j] = do_zero(matrix[i], matrix[j], i)

    for i in range(1, size):
        for j in range(size - i):
            matrix[j] = do_zero(matrix[-i], matrix[j], -i)

    for i in range(size):
        matrix[i] = do_one(matrix[i], i)

    return matrix


def create_vector(point_start, point_end):
    """ Создаёт вектор, вычитая из координат точки конца вектора координаты точки начала. """
    vector0 = []
    for i in range(len(point_start)):
        vector0.append(point_end[i] - point_start[i])
    return vector0


def scalar_mult(vector1, vector2):
    """ Вычисляет скалярное произведение двух векторов. """
    x = 0
    for i in range(len(vector1)):
        x += vector1[i] * vector2[i]
    return x


def vector_modul(vector0):
    """ Вычисляет модуль вектора. """

    return scalar_mult(vector0, vector0) ** (1 / 2)


def angle_degrees_vector_vector(vector1, vector2):
    """ Вычисляет угол между двумя векторами в градусах. """

    return math.degrees(math.acos(scalar_mult(vector1, vector2) / (vector_modul(vector1) * vector_modul(vector2))))


def angle_degrees_line_plane(line, plane):
    """ Вычисляет угол между прямой и плоскостью в градусах. """

    new_point1 = proection_point_to_plane(line[0], plane)
    new_point2 = cross_line_plane(line, plane, 3)

    new_vector = create_vector(new_point1, new_point2)
    return angle_degrees_vector_vector(new_vector, line[1])


def angle_degrees_plane_plane(plane1, plane2):
    """ Вычисляет угол между двумя плоскостями в градусах. """

    new_line = cross_plane_plane(plane1, plane2, 3)
    new_point_1 = proection_point_to_line(plane1[0], new_line)
    new_point_2 = proection_point_to_line(plane2[0], new_line)

    new_vector1 = create_vector(plane1[0], new_point_1)
    new_vector2 = create_vector(plane2[0], new_point_2)

    return angle_degrees_vector_vector(new_vector1, new_vector2)



def is_line_line_parallel(line1, line2, size):
    """ Проверяет параллельность прямых. """
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
            if x == abs(line1[1][2] / line2[1][2]):
                return True
            return False

    else:
        x = abs(line1[1][0] / line2[1][0])
        for i in range(1, size):
            if x == abs(line1[1][i] / line2[1][i]):
                return False
        return True


def is_line_line_perpend(line1, line2, size):
    """ Проверяет парпендикулярность двух прямых. """
    if cross_line_line(line1, line2, size) != 'прямые скрещивающиеся' and cross_line_line(line1, line2,
                                                                                          size) != 'прямые параллельны':
        if scalar_mult(line1[1], line2[1]) == 0:
            return True
    return False


def cross_line_line(line1, line2, size):
    """ Находит точку пересечения прямых или выводит сообщение о параллельности."""

    if is_line_line_parallel(line1, line2, size):
        return 'прямые параллельны'

    matrix = []
    for i in range(size):
        matrix.append([[- line1[1][i], line2[1][i]], [line1[0][i] - line2[0][i]]])

    matrix = gauss(matrix, 2)

    a = matrix[0][1][0]
    b = matrix[1][1][0]

    if (-a * line1[1][2] + b * line2[1][2]) == (line1[0][2] - line2[0][2]):
        point_C = []
        for i in range(size):
            point_C.append(line1[0][i] + a * line1[1][i])
        return point_C

    return 'прямые скрещивающиеся'


def cross_line_plane(line, plane, size):
    """ Находит точку пересечения прямой и плоскости или выводит сообщение о параллельности."""
    matrix0 = []
    for i in range(size):
        matrix0.append([[- line[1][i], plane[1][i], plane[2][i]], [line[0][i] - plane[0][i]]])

    matrix0 = gauss(matrix0, size)

    if matrix0 == False:
        return 'Прямая параллельна плоскости'

    point_C = []
    for i in range(size):
        point_C.append(line[0][i] + line[1][i] * matrix0[0][1][0])
    return point_C


def cross_plane_plane(plane1, plane2, size):
    """ Находит прямую пересечения двух плоскостей или выводит сообщение о параллельности. """

    point_A = plane1[0]
    vector11 = plane1[1]
    vector12 = plane1[2]

    if cross_line_plane((point_A, vector11), plane2) == 'Прямая параллельна плоскости':
        if cross_line_plane((point_A, vector12), plane2) == 'Прямая параллельна плоскости':
            return 'Плоскости параллельны'
        point_C = []
        for i in range(size):
            point_C.append(point_A[i] + vector11[i])

        new_point_1 = cross_line_plane((point_A, vector12), plane2)
        new_point_2 = cross_line_plane((point_C, vector12), plane2)
        new_vector = create_vector(new_point_1, new_point_2)
        return [new_point_1, new_vector]

    point_C = []
    for i in range(size):
        point_C.append(point_A[i] + vector12[i])

    new_point_1 = cross_line_plane((point_A, vector11), plane2)
    new_point_2 = cross_line_plane((point_C, vector11), plane2)
    new_vector = create_vector(new_point_1, new_point_2)
    return [new_point_1, new_vector]


def proection_point_to_line(point_A, line0):
    """ Проецирует точку на прямую. """

    vector0 = line0[1]
    point_B = line0[0]
    size = len(point_A)
    summa_of_cube_of_vector0 = 0
    for i in vector0:
        summa_of_cube_of_vector0 += i ** 2
    summa_other = 0
    for i in range(size):
        summa_other += vector0[i] * (point_A[i] - point_B[i])
    parametr = summa_other / summa_of_cube_of_vector0
    point_C = []
    for i in range(size):
        point_C.append(point_B[i] + parametr * vector0[i])
    return point_C


def proection_point_to_plane(point_A, plane0):
    """ Проецирует точку на плоскость. """

    point_B = plane0[0]
    vector1 = plane0[1]
    vector2 = plane0[2]

    #   [[point_C[0], point_C[1], point_C[2], parametr1, parametr2], [result]]

    matrix = [
        [[vector1[0], vector1[1], vector1[2], 0, 0], [point_A[0]*vector1[0] + point_A[1]*vector1[1] + point_A[2]*vector1[2]]],
        [[vector2[0], vector2[1], vector2[2], 0, 0], [point_A[0]*vector2[0] + point_A[1]*vector2[1] + point_A[2]*vector2[2]]],
        [[0, 0, 1, vector1[2] * -1, vector2[2] * -1], [point_B[2]]],
        [[0, 1, 0, vector1[1] * -1, vector2[1] * -1], [point_B[1]]],
        [[1, 0, 0, vector1[0] * -1, vector2[0] * -1], [point_B[0]]]
    ]

    matrix = gauss(matrix, 5)
    if matrix == False:
        return False

    point_C = []

    for i in range(3):
        point_C.append(matrix[i][1][0])
    return point_C


def distanse_from_point_to_point(point_A, point_B):
    """ Вычисляет расстояние между двумя точками. """

    vector0 = create_vector(point_A, point_B)
    return vector_modul(vector0)


def distanse_from_point_to_line(point_A, line1):
    """ Вычисляет расстояние от точки до прямой. """

    point_C = proection_point_to_line(point_A, line1)
    vector0 = create_vector(point_A, point_C)
    return vector_modul(vector0)


def distanse_from_point_to_plane(point_A, plane1):
    """ Вычисляет расстояние от точки до плоскости. """

    point_B = proection_point_to_plane(point_A, plane1)
    return distanse_from_point_to_point(point_A, point_B)


def distanse_from_line_to_line(line1, line2):
    """ Находит расстояние между двумя скрещивающимися прямыми. """

    P1 = line1[0]
    P2 = line2[0]
    v1 = line1[1]
    v2 = line2[1]

    # [[A[0], A[1], A[2], B[0], B[1], B[2], parametr1, parametr2], [result]]
    matrix = [
        [[1, 0, 0, 0, 0, 0, v1[0] * -1, 0], [P1[0]]],
        [[0, 1, 0, 0, 0, 0, v1[1] * -1, 0], [P1[1]]],
        [[1, 0, 1, 0, 0, 0, v1[2] * -1, 0], [P1[2]]],
        [[0, 0, 0, 1, 0, 0, 0, v2[0] * -1], [P2[0]]],
        [[0, 0, 0, 0, 1, 0, 0, v2[1] * -1], [P2[1]]],
        [[0, 0, 0, 0, 0, 1, 0, v2[2] * -1], [P2[2]]],
        [[v1[0], v1[1], v1[2], v1[0] * -1, v1[1] * -1, v1[2] * -1, 0, 0], [0]],
        [[v2[0], v2[1], v2[2], v2[0] * -1, v2[1] * -1, v2[2] * -1, 0, 0], [0]]
    ]
    matrix = gauss(matrix, 8)
    A = []
    B = []
    for i in range(6):
        if i <= 2:
            A.append(matrix[i][1][0])
        if i >= 3:
            B.append(matrix[i][1][0])

    return vector_modul(create_vector(A, B))


size = 3

point_A = [0, 0, 1]
point_B = [0, 0, 0]
point_C = [1, 0, 1]
point_D = [1, 0, 0]

vector1 = create_vector(point_B, point_C)
vector2 = create_vector(point_B, point_D)
vector3 = [0, 1, 0]
vector4 = [1, 0, 0]
vector0 = [1, 0, 0]

line1 = [point_A, vector0]
line2 = [point_B, vector1]

plane1 = [point_B, vector3, vector4]
plane2 = [point_B, vector3, vector4]

print(cross_line_plane(line1, plane1, size))

