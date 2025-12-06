#   -----------------------------------------------------------------------------
#   Projeto:        Projeto Trainee - Processo Seletivo EDRA 2025.2
#   Descrição:      O projeto do PS tem como objetivo a programação de um drone de treinamento simulado 
#                   que deve percorrer um mapa de 400x400cm e coletar 5 tesouros distribuídos
#                   aleatoriamente no mapa a cada execução do código e retornar ao ponto de início
#                   após coletar todos os tesouros. Foi usada uma biblioteca TelloSim adaptada para
#                   o PS, disponível no link: https://github.com/fabinsz/tello_sim_EDRA. Para mais
#                   informações olhar os PDFs de edital presentes nesta pasta "tello_sim_EDRA-main".
#   Autor:          Luiz Henrique da Silva Amaral
#   Data:           05/12/2025
#   Contato:        luizhsamaral@gmail.com
#   GitHub:         https://github.com/LuizAmaral19 
#   -----------------------------------------------------------------------------

from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

fov_Tello = meu_Tello.vision_range  # Diâmetro do Field Of Vision
fov_by_2 = meu_Tello.vision_range/2 # Raio do Field Of Vision 
overlap = 5                         # Overlap para garantir que todo o campo seja varrido

# Coordenadas Globais
global_rsl = meu_Tello.field_limit   # Global Right Side Limit
global_usl = meu_Tello.field_limit   # Global Left Side Limit
global_lsl = -meu_Tello.field_limit  # Global Upper Side Limit
global_dsl = -meu_Tello.field_limit  # Global Down Side Limit

# Coordenadas úteis de cada célula
cell1_rsl = meu_Tello.field_limit - fov_Tello   # Cell 1 Right Side Limit
cell1_usl = meu_Tello.field_limit - fov_Tello   # Cell 1 Upper Side Limit
cell1_dsl = fov_by_2                            # Cell 1 Down Side Limit

cell2_rsl = -fov_by_2                           # Cell 2 Right Side Limit
cell2_usl = fov_by_2                            # Cell 2 Upper Side Limit
cell2_lsl = -meu_Tello.field_limit + fov_Tello  # Cell 2 Left Side Limit

cell3_rsl = global_rsl - fov_Tello              # Cell 3 Right Side Limit
cell3_usl = -fov_by_2                           # Cell 3 Upper Side Limit
cell3_lsl = fov_by_2                            # Cell 3 Left Side Limit
cell3_dsl = -meu_Tello.field_limit + fov_Tello  # Cell 3 Down Side Limit


# Movimentos para a varredura da Célula I
def sweeping_cell1():
    conditional_cell1_movements = []

    height_cell1 = cell1_usl - cell1_dsl
    step = fov_Tello

    full_sweeps = int(height_cell1 // step)
    remainder = height_cell1 - (full_sweeps * step)
    
    def go_right():
        return max(0.0, abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)
    

    def go_left():
        return max(0.0, abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)


    def go_cell2():
        return max(0.0, abs(global_dsl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)


    for c in range(full_sweeps):
        if (c % 2) == 0:
            conditional_cell1_movements.append((meu_Tello.back, step)) 
            conditional_cell1_movements.append((meu_Tello.right, go_right)) 
        else:
            conditional_cell1_movements.append((meu_Tello.back, step))
            conditional_cell1_movements.append((meu_Tello.left, go_left))
    
    if remainder > 0:
        conditional_cell1_movements.append((meu_Tello.back, remainder + overlap))
        if (full_sweeps % 2) == 0:
            conditional_cell1_movements.append((meu_Tello.right, go_right))
            conditional_cell1_movements.append((meu_Tello.left, go_left))
        else:
            conditional_cell1_movements.append((meu_Tello.left, go_left))

    conditional_cell1_movements.append((meu_Tello.back, go_cell2))

    return conditional_cell1_movements


movements_cell1 = [
    (meu_Tello.right, lambda: (abs(global_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.forward, lambda: (abs(global_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
]
movements_cell1.extend(sweeping_cell1())

# Movimentos para a varredura da Célula II
def sweeping_cell2():
    conditional_cell2_movements = []

    length_cell2 = abs(cell2_lsl) - abs(cell2_rsl)
    step = fov_Tello

    full_sweeps = int(length_cell2 // step)
    remainder = length_cell2 - (full_sweeps * step)

    def go_up():
        return max(0.0, abs(cell2_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)
    

    def go_down():
        return max(0.0, abs(global_dsl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)
    

    def go_cell3():
        return max(0.0, abs(global_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)
    
    
    for c in range(full_sweeps):
        conditional_cell2_movements.append((meu_Tello.right, step))
        if (c % 2) == 0:
            conditional_cell2_movements.append((meu_Tello.forward, go_up))
        else:
            conditional_cell2_movements.append((meu_Tello.back, go_down))

    if remainder > 0:
        conditional_cell2_movements.append((meu_Tello.right, remainder + overlap))
        if (full_sweeps % 2) == 0:
            conditional_cell2_movements.append((meu_Tello.forward, go_up))
            conditional_cell2_movements.append((meu_Tello.back, go_down))
        else:
            conditional_cell2_movements.append((meu_Tello.back, go_down))
    
    conditional_cell2_movements.append((meu_Tello.right, go_cell3))

    return conditional_cell2_movements


movements_cell2 = []
movements_cell2.extend(sweeping_cell2())

# Movimentos para a varredura da Célula III
def sweeping_cell3():
    conditional_cell3_movements = []

    length_cell3 = abs(global_rsl) + abs(cell3_lsl)
    step = fov_Tello

    full_sweeps = int(length_cell3 // step)
    remainder = length_cell3 - (full_sweeps * step)

    def go_up():
        return max(0.0, abs(cell3_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)
    

    def go_down():
        return max(0.0, abs(cell3_dsl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)
    

    def go_center_x():
        return max(0.0, abs(0 - meu_Tello.cur_loc[0]))


    def go_center_y():
        return max(0.0, abs(0 - meu_Tello.cur_loc[1]))
    

    for c in range(full_sweeps):
        conditional_cell3_movements.append((meu_Tello.left, step))
        if (c % 2) == 0:
            conditional_cell3_movements.append((meu_Tello.back, go_down))
        else:
            conditional_cell3_movements.append((meu_Tello.forward, go_up))
    
    if remainder > 0:
        conditional_cell3_movements.append((meu_Tello.left, remainder + overlap))
        if (full_sweeps % 2) == 0:
            conditional_cell3_movements.append((meu_Tello.back, go_down))
            conditional_cell3_movements.append((meu_Tello.forward, go_up))
        else:
            conditional_cell3_movements.append((meu_Tello.forward, go_up))

    conditional_cell3_movements.append((meu_Tello.forward, go_center_y))
    conditional_cell3_movements.append((meu_Tello.left, go_center_x))

    return conditional_cell3_movements


movements_cell3 = [
    (meu_Tello.forward, lambda: abs(cell3_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)
]
movements_cell3.extend(sweeping_cell3())


def move_and_check(drone, command, distance):

    if callable(distance):
        distance = distance()
    qntty_steps = distance/fov_Tello
    for c in range (0, int(qntty_steps)):
        command(fov_Tello)
        if (len(drone.visited_treasures) - len(drone.treasures)) == 0:
            return 0
    command((qntty_steps % 1) * fov_Tello)
    if (len(drone.visited_treasures) - len(drone.treasures)) == 0:
        return 0
    

def go_home():
    current_x, current_y = meu_Tello.cur_loc
    if current_x >=0:
        meu_Tello.left(current_x)
    else:
        meu_Tello.right(-current_x)
    if current_y >= 0:
        meu_Tello.back(current_y)
    else:
        meu_Tello.forward(-current_y)
    meu_Tello.land()


def area_coverage():

    meu_Tello.takeoff()

    while True:
        stop_and_go_home = False
        for command, distance in movements_cell1:
            if move_and_check(meu_Tello, command, distance) == 0: 
                stop_and_go_home = True
                break
        if stop_and_go_home == True:
            break

        for command, distance in movements_cell2:
            if move_and_check(meu_Tello, command, distance) == 0:
                stop_and_go_home = True
                break
        if stop_and_go_home == True:
            break

        for command, distance in movements_cell3:
            if move_and_check(meu_Tello, command, distance) == 0:
                stop_and_go_home = True
                break
        if stop_and_go_home == True:
            break

area_coverage()
go_home()