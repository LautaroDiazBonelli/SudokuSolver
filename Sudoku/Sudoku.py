from random import randint

# la forma que tienen los tableros
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


tableroSeleccionado = None


def seleccionarTablero(num=None):
    '''
    Selecciona un tablero al azar de los 46 disponibles.
    :param num: Opcionalmente si le asignas un numero(num)
    te selecciona el tablero de mismo numero
    :return: None
    '''
    if not num:
        random = randint(1, 46)
    else:
        random = num
    global tableroSeleccionado
    tableroSeleccionado = random
    archivo = open('Tableros/' + str(random) + '.txt', 'r')
    lineas = archivo.readlines()
    bo = []
    row = 0  # Por que si no, los sudokus tenian una fila vacia de más ([])
    for i in lineas:

        row += 1
        if row <= 9:
            lineas = i.split()
            bo.append(lineas)
        else:
            break

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            bo[i][j] = int(bo[i][j])

    archivo.close()
    return bo


def solve(bo):
    '''
    Resuelve el tablero siempre y cuando este tenga solucion.
    Utiliza el algoritmo de "Backtracking".
    Es una funcion recursiva
    :param bo: Tablero
    :return: None
    '''
    find = finds_empty(bo)
    if not find:
        return True
    else:
        row, col = find   #si no encuentra ningun espacio 'vacio' el agoritma termina

    for i in range(1, 10):
        if valid(bo, (row, col), i):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, pos, num):
    '''
    Checkea si el numero dado es legal en esa posicion
    :param bo: Tablero
    :param pos: coords
    :param num:
    :return: Bool
    '''
    #row
    for i in range(0, len(bo)):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    #col
    for i in range(0, len(bo)):
        if bo[i][pos[1]] == num and pos[1] != i:
            return False

    #cuadrante
    box_x = pos[1] // 3  #cuadrantes posibles son (0,0) --> (2,2)
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def finds_empty(bo):
    '''
    Busca por el primer espacio vacio empezando por arriba a la izquierda
    :param bo: Tablero
    :return: las coords de donde esta, en caso de no existir return None
    '''
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j

    return None


def print_board(bo):
    #Solo util para la "version de consola"
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end='')
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + ' ', end='')


board = seleccionarTablero()
bo_copy = seleccionarTablero(tableroSeleccionado)
bo_updated = seleccionarTablero(tableroSeleccionado)
