from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

fov_Tello = meu_Tello.vision_range
fov_by_2 = meu_Tello.vision_range/2 # Raio do Field Of Vision 
overlap = 5                         # Overlap para garantir que todo o campo seja varrido

# Coordenadas Globais
global_rsl = meu_Tello.field_limit   # Global Right Side Limit
global_usl = meu_Tello.field_limit   # Global Left Side Limit
global_lsl = -meu_Tello.field_limit  # Global Upper Side Limit
global_dsl = -meu_Tello.field_limit  # Global Down Side Limit

# Coordenadas úteis de cada célula
cell1_rsl = meu_Tello.field_limit - fov_Tello   # Cell 1 Right Side Limit
cell1_dsl = -fov_by_2                           # Cell 1 Down Side Limit

cell2_rsl = -fov_by_2                           # Cell 2 Right Side Limit
cell2_usl = fov_by_2                            # Cell 2 Upper Side Limit
cell2_lsl = -meu_Tello.field_limit + fov_Tello  # Cell 2 Left Side Limit

cell3_usl = -fov_by_2                           # Cell 3 Upper Side Limit
cell3_lsl = -fov_by_2                           # Cell 3 Left Side Limit
cell3_dsl = meu_Tello.field_limit - fov_Tello   # Cell 3 Down Side Limit

def sweeping_cell1 ():
    conditional_cell1_movements = []
    qntty_sweeps_cell1 = (global_usl - cell1_dsl)/fov_Tello
    
    if (qntty_sweeps_cell1 % 1) != 0:
        if(qntty_sweeps_cell1 // 1) % 2 == 0:
            for c in range (0, int(qntty_sweeps_cell1 // 1) - 1):
                conditional_cell1_movements.extend([
                    (meu_Tello.back, lambda: fov_Tello),
                    (meu_Tello.right, lambda: (abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
                    (meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
                ])
        else:
            for c in range (0, int(qntty_sweeps_cell1 // 1) - 1):
                conditional_cell1_movements.extend([
                    (meu_Tello.back, lambda: fov_Tello),
                    (meu_Tello.right, lambda: (abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
                    (meu_Tello.back, lambda: fov_Tello),
                    (meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
                ])
    elif qntty_sweeps_cell1 == 1:
        conditional_cell1_movements.append((meu_Tello.back, lambda: (abs(global_dsl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)))
    elif (qntty_sweeps_cell1 % 2) == 0:
        for c in range (0, qntty_sweeps_cell1 - 1):
            conditional_cell1_movements.extend([
                (meu_Tello.back, lambda: fov_Tello),
                (meu_Tello.right, lambda: (abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
                (meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
            ])
        conditional_cell1_movements.append((meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap))) 
            
            # Fazer ir de uma vez só, sem dar os passos
    elif (qntty_sweeps_cell1 % 2) != 0:
        for c in range (0, qntty_sweeps_cell1 - 1):
            conditional_cell1_movements.extend([
                (meu_Tello.back, lambda: fov_Tello),
                (meu_Tello.right, lambda: (abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
                (meu_Tello.back, lambda: fov_Tello),
                (meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
            ])
    return conditional_cell1_movements


movements_cell1 = [
    (meu_Tello.right, lambda: (abs(global_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.forward, lambda: (abs(global_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.left, lambda: (abs(global_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
]
movements_cell1.extend(sweeping_cell1())

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


area_coverage()
go_home()