"""

Файл создан для решения стереометрических задач
через параметрические координаты.
SIZE - кол-во измерений (по умолчнию 3).
точка (point_a, point_b...) или
вектор (vector0, vector1...) задётся списком [x, y, z].
Прямая задётся через точку и вектор, плоскость через точку и два вектора.

"""


import math


SIZE = 3


def create_ok_list(matrix, matrix_size):
    """ Создаёт список - какая строка матрицы может встать на какое место. """
    ok_list = []
    for i in range(matrix_size):
        ok_list.append([])

    for i in range(matrix_size):
        for j in range(matrix_size):
            if matrix[j][0][i] != 0:
                ok_list[i].append(j)

    return ok_list


def distribution(ok_list, matrix_size, stack):
    """
    Выдаёт список с верной расстановкой строк
    или False, если нет решений.
    """
    line_number = len(stack)
    if not ok_list[line_number]:
        return False
    for i in ok_list[line_number]:
        if stack.count(i) == 0:
            stack.append(i)
            if line_number == matrix_size - 1:
                return stack
            answer = distribution(ok_list, matrix_size, stack)
            if answer is not False:
                return answer
            stack.remove(i)
    return False


def reverse(matrix, correct_list, matrix_size):
    """ Переставляет строки матрицы на места из correct_list."""
    new_matrix = []
    for i in range(matrix_size):
        new_matrix.append(matrix[correct_list[i]])
    return new_matrix


def do_zero(matrix_line1, matrix_line2, i):
    """Обнуляет i-ытй элемент строки matrix_line2. """
    if matrix_line1[0][i] == 0:
        return matrix_line2
    ratio = (- matrix_line2[0][i]) / matrix_line1[0][i]

    for j in range(len(matrix_line2[0])):
        matrix_line2[0][j] += matrix_line1[0][j] * ratio

    matrix_line2[1][0] += matrix_line1[1][0] * ratio
    return matrix_line2


def do_one(matrix_line1, i):
    """Превращает i-тый элемент строки matrix_line1 в 1"""
    if matrix_line1[0][i] == 0:
        return matrix_line1
    if matrix_line1[0][i] != 1:
        ratio = matrix_line1[0][i]

        for k in range(len(matrix_line1[0])):
            matrix_line1[0][k] *= 1 / ratio

        matrix_line1[1][0] *= 1 / ratio
    for j in range(len(matrix_line1[0])):
        if matrix_line1[0][j] == -0.0:
            matrix_line1[0][j] = 0

    return matrix_line1


def gauss(matrix: list, matrix_size):
    """ Применяет метод Гаусса к матрице. """
    ok_list = create_ok_list(matrix, matrix_size)
    stack = []
    correct_list = distribution(ok_list, matrix_size, stack)
    if correct_list is False:
        # решений нет
        return False
    matrix = reverse(matrix, correct_list, matrix_size)

    # теперь на диагонали matrix[i][0][i], i in range(SIZE) нет нулей

    for i in range(matrix_size - 1):
        for j in range(i + 1, matrix_size):
            matrix[j] = do_zero(matrix[i], matrix[j], i)

    for i in range(1, matrix_size):
        for j in range(matrix_size - i):
            matrix[j] = do_zero(matrix[-i], matrix[j], -i)

    for i in range(matrix_size):
        matrix[i] = do_one(matrix[i], i)

    return matrix


def create_vector(point_start, point_end):
    """
    Создаёт вектор, вычитая из координат точки конца вектора
    координаты точки начала.
    """
    created_vector = []
    for i in range(SIZE):
        created_vector.append(point_end[i] - point_start[i])
    return created_vector


def scalar_mult(first_vector, second_vector):
    """ Вычисляет скалярное произведение двух векторов. """
    composition = 0
    for i in range(SIZE):
        composition += first_vector[i] * second_vector[i]
    return composition


def vector_modul(vector):
    """ Вычисляет модуль вектора. """
    return scalar_mult(vector, vector) ** (1 / 2)


def angle_degrees_vector_vector(vector001, vector002):
    """ Вычисляет угол между двумя векторами в градусах. """
    return math.degrees(math.acos(scalar_mult(vector001, vector002) / (vector_modul(vector001)
                                                                       * vector_modul(vector002))))


def angle_degrees_line_plane(line, plane):
    """ Вычисляет угол между прямой и плоскостью в градусах. """
    new_point1 = proection_point_to_plane(line[0], plane)
    new_point2 = cross_line_plane(line, plane)

    new_vector = create_vector(new_point1, new_point2)
    return angle_degrees_vector_vector(new_vector, line[1])


def angle_degrees_plane_plane(plane001, plane002):
    """ Вычисляет угол между двумя плоскостями в градусах. """
    new_line = cross_plane_plane(plane001, plane002)

    new_point_1 = proection_point_to_line(plane001[0], new_line)
    new_point_2 = proection_point_to_line(plane002[0], new_line)

    new_vector1 = create_vector(plane001[0], new_point_1)
    new_vector2 = create_vector(plane002[0], new_point_2)

    return angle_degrees_vector_vector(new_vector1, new_vector2)


def is_line_line_parallel(line001, line002):
    """ Проверяет параллельность прямых. """
    if line001[0] == line002[0]:
        return False

    vector_mult = 0
    for i in range(SIZE):
        for j in range(i + 1, SIZE):
            vector_mult += line001[1][i] * line002[1][j] \
                           - line001[1][j] * line002[1][i]

    if not vector_mult:
        return True
    return False


def is_line_line_perpend(line01, line02):
    """ Проверяет парпендикулярность двух прямых. """
    if cross_line_line(line01, line02) != 'прямые скрещивающиеся' and \
            cross_line_line(line01, line02) != 'прямые параллельны':
        if scalar_mult(line01[1], line02[1]) == 0:
            return True
    return False


def cross_line_line(line__1, line__2):
    """
    Находит точку пересечения прямых
    или выводит сообщение о параллельности.
    """
    if is_line_line_parallel(line__1, line__2):
        return 'прямые параллельны'

    matrix = []
    for i in range(SIZE):
        matrix.append([[- line__1[1][i], line__2[1][i]], [line__1[0][i] - line__2[0][i]]])

    matrix = gauss(matrix, 2)

    coefficient_a = matrix[0][1][0]
    coefficient_b = matrix[1][1][0]

    if (-coefficient_a * line__1[1][2] + coefficient_b * line__2[1][2])\
            == (line__1[0][2] - line__2[0][2]):
        point__c = []
        for i in range(SIZE):
            point__c.append(line__1[0][i] + coefficient_a * line__1[1][i])
        return point__c

    return 'прямые скрещивающиеся'


def cross_line_plane(line, plane):
    """
    Находит точку пересечения прямой и плоскости
    или выводит сообщение о параллельности.
    """
    matrix0 = []
    for i in range(SIZE):
        matrix0.append([[- line[1][i], plane[1][i], plane[2][i]],
                        [line[0][i] - plane[0][i]]])

    matrix0 = gauss(matrix0, SIZE)

    if matrix0 is False:
        return 'Прямая параллельна плоскости'

    new_point_c = []
    for i in range(SIZE):
        new_point_c.append(line[0][i] + line[1][i] * matrix0[0][1][0])
    return new_point_c


def cross_plane_plane(plane01, plane02):
    """
    Находит прямую пересечения двух плоскостей
    или выводит сообщение о параллельности.
    """
    point_0a = plane01[0]
    vector11 = plane01[1]
    vector12 = plane01[2]

    if cross_line_plane((point_0a, vector11), plane02) \
            == 'Прямая параллельна плоскости':
        if cross_line_plane((point_0a, vector12), plane02) \
                == 'Прямая параллельна плоскости':
            return 'Плоскости параллельны'
        point_0c = []
        for i in range(SIZE):
            point_0c.append(point_0a[i] + vector11[i])

        new_point_1 = cross_line_plane((point_0a, vector12), plane02)
        new_point_2 = cross_line_plane((point_0c, vector12), plane02)
        new_vector = create_vector(new_point_1, new_point_2)
        return [new_point_1, new_vector]

    point_0c = []
    for i in range(SIZE):
        point_0c.append(point_0a[i] + vector12[i])

    new_point_1 = cross_line_plane((point_0a, vector11), plane02)
    new_point_2 = cross_line_plane((point_0c, vector11), plane02)
    new_vector = create_vector(new_point_1, new_point_2)
    return [new_point_1, new_vector]


def proection_point_to_line(start_point_a, line_0_):
    """ Проецирует точку на прямую. """
    vector_0 = line_0_[1]
    point__b = line_0_[0]
    summa_of_cube_of_vector0 = 0
    for i in vector_0:
        summa_of_cube_of_vector0 += i ** 2
    summa_other = 0
    for i in range(SIZE):
        summa_other += vector_0[i] * (start_point_a[i] - point__b[i])
    parametr = summa_other / summa_of_cube_of_vector0
    point___c = []
    for i in range(SIZE):
        point___c.append(point__b[i] + parametr * vector_0[i])
    return point___c


def proection_point_to_plane(point__f, plane__0):
    """ Проецирует точку на плоскость. """
    point__b = plane__0[0]
    vector__1 = plane__0[1]
    vector__2 = plane__0[2]

    #   [[point___c[0], point___c[1], point___c[2], parametr1, parametr2], [result]]

    matrix = [
        [[vector__1[0], vector__1[1], vector__1[2], 0, 0],
         [point__f[0] * vector__1[0] + point__f[1] * vector__1[1]
          + point__f[2] * vector__1[2]]],
        [[vector__2[0], vector__2[1], vector__2[2], 0, 0],
         [point__f[0] * vector__2[0] + point__f[1] * vector__2[1]
          + point__f[2] * vector__2[2]]],
        [[0, 0, 1, vector__1[2] * -1, vector__2[2] * -1], [point__b[2]]],
        [[0, 1, 0, vector__1[1] * -1, vector__2[1] * -1], [point__b[1]]],
        [[1, 0, 0, vector__1[0] * -1, vector__2[0] * -1], [point__b[0]]]
    ]

    matrix = gauss(matrix, 5)
    if matrix is False:
        return False

    point___c = []

    for i in range(3):
        point___c.append(matrix[i][1][0])
    return point___c


def distanse_from_point_to_point(start_point__a, end_point__b):
    """ Вычисляет расстояние между двумя точками. """
    vector__01 = create_vector(start_point__a, end_point__b)
    return vector_modul(vector__01)


def distanse_from_point_to_line(point_a_, line_1_):
    """ Вычисляет расстояние от точки до прямой. """
    point_c_ = proection_point_to_line(point_a_, line_1_)
    vector_0_ = create_vector(point_a_, point_c_)
    return vector_modul(vector_0_)


def distanse_from_point_to_plane(point_a__, plane__1):
    """ Вычисляет расстояние от точки до плоскости. """
    point_b_ = proection_point_to_plane(point_a__, plane__1)
    return distanse_from_point_to_point(point_a__, point_b_)


def distanse_from_line_to_line(line_1__, line_2__):
    """ Находит расстояние между двумя скрещивающимися прямыми. """
    point___1 = line_1__[0]
    point___2 = line_2__[0]
    vector___1 = line_1__[1]
    vector___2 = line_2__[1]

    # [[point___1[0], point___1[1], point___1[2], point___2[0], point___2[1],
    # point___2[2], parametr1, parametr2], [result]]

    matrix = [
        [[1, 0, 0, 0, 0, 0, vector___1[0] * -1, 0], [point___1[0]]],
        [[0, 1, 0, 0, 0, 0, vector___1[1] * -1, 0], [point___1[1]]],
        [[1, 0, 1, 0, 0, 0, vector___1[2] * -1, 0], [point___1[2]]],
        [[0, 0, 0, 1, 0, 0, 0, vector___2[0] * -1], [point___2[0]]],
        [[0, 0, 0, 0, 1, 0, 0, vector___2[1] * -1], [point___2[1]]],
        [[0, 0, 0, 0, 0, 1, 0, vector___2[2] * -1], [point___2[2]]],
        [[vector___1[0], vector___1[1], vector___1[2], vector___1[0] * -1,
          vector___1[1] * -1, vector___1[2] * -1, 0, 0], [0]],
        [[vector___2[0], vector___2[1], vector___2[2], vector___2[0] * -1,
          vector___2[1] * -1, vector___2[2] * -1, 0, 0], [0]]
    ]
    matrix = gauss(matrix, 8)
    point_aa = []
    point_bb = []
    for i in range(6):
        if i <= 2:
            point_aa.append(matrix[i][1][0])
        if i >= 3:
            point_bb.append(matrix[i][1][0])

    return vector_modul(create_vector(point_aa, point_bb))


point_a = [0, 0, 1]

vector1 = [0, 1, 0]
vector0 = [1, 0, 0]

line0 = [point_a, vector1]
plane0 = [point_a, vector0, vector1]
