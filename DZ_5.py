import random
import time

"""
    -------BATTLESHIPS-------
 Легенда:
 1. "." = вода или пустое пространство
 2. "О" = часть судна
 3. "X" = часть корабля, в которую попал снаряд
 4. "#" = вода, в которую попал снаряд, промах, потому что он не попал ни в один корабль
"""


grid = [[]]
grid_size = 10
num_of_ships = 2
bullets_left = 50
game_over = False
num_of_ships_sunk = 0
ship_positions = [[]]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_grid_and_place_ship(start_row, end_row, start_col, end_col):
    global grid
    global ship_positions

    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "O"
    return all_valid


def try_to_place_ship_on_grid(row, col, direction, length):
    global grid_size

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1

    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length

    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length

    return validate_grid_and_place_ship(start_row, end_row, start_col, end_col)


def create_grid():
    global grid
    global grid_size
    global num_of_ships
    global ship_positions

    random.seed(time.time())

    rows, cols = (grid_size, grid_size)

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid.append(row)

    num_of_ships_placed = 0

    ship_positions = []

    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1


def print_grid():
    global grid
    global alphabet

    debug_mode = True

    alphabet = alphabet[0: len(grid) + 1]

    for row in range(len(grid)):
        print(alphabet[row], end=") ")
        for col in range(len(grid[row])):
            if grid[row][col] == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_bullet_placement():
    global alphabet
    global grid

    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        placement = input("Введите строку (A-J) и столбец (0-9), например A3: ")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            print("Ошибка: Пожалуйста, введите только одну строку и столбец, например A3")
            continue
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            print("Ошибка: Пожалуйста, введите букву (A-J) для строки и (0-9) для столбца")
            continue
        row = alphabet.find(row)
        if not (-1 < row < grid_size):
            print("Ошибка: Пожалуйста, введите букву (A-J) для строки и (0-9) для столбца")
            continue
        col = int(col)
        if not (-1 < col < grid_size):
            print("Ошибка: Пожалуйста, введите букву (A-J) для строки и (0-9) для столбца")
            continue
        if grid[row][col] == "#" or grid[row][col] == "X":
            print("Вы уже стреляли здесь, выберите другие координаты")
            continue
        if grid[row][col] == "." or grid[row][col] == "O":
            is_valid_placement = True

    return row, col


def check_for_ship_sunk(row, col):
    global ship_positions
    global grid

    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:

            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True


def shoot_bullet():
    global grid
    global num_of_ships_sunk
    global bullets_left

    row, col = accept_valid_bullet_placement()
    print("")
    print("----------------------------")

    if grid[row][col] == ".":
        print("Вы промахнулись, ни один корабль не был обстрелян")
        grid[row][col] = "#"
    elif grid[row][col] == "O":
        print("Ты попал!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("Корабль был полностью потоплен!")
            num_of_ships_sunk += 1
        else:
            print("Корабль был расстрелян")

    bullets_left -= 1


def check_for_game_over():
    global num_of_ships_sunk
    global num_of_ships
    global bullets_left
    global game_over

    if num_of_ships == num_of_ships_sunk:
        print("Поздравляю, вы выиграли!")
        game_over = True
    elif bullets_left <= 0:
        print("Извините, вы проиграли! У тебя закончились патроны, попробуй еще в следующий раз!")
        game_over = True


def main():

    global game_over

    print("-----Добро пожаловать в Battleships-----")
    print("У вас есть 50 снарядов, чтобы уничтожить 8 кораблей, да начнется битва!")

    create_grid()

    while game_over is False:
        print_grid()
        print("Количество оставшихся судов: " + str(num_of_ships - num_of_ships_sunk))
        print("Количество оставшихся снарядов: " + str(bullets_left))
        shoot_bullet()
        print("----------------------------")
        print("")
        check_for_game_over()


if __name__ == '__main__':
    """Will only be called when program is run from terminal or an IDE like PyCharms"""
    main()