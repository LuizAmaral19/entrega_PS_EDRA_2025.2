from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

fov_Tello = meu_Tello.vision_range
fov_by_2 = meu_Tello.vision_range/2 # Raio do Field Of Vision 
overlap = 5                         # Overlap para garantir que todo o campo seja varrido

# Coordenadas úteis de cada célula
cell1_rsl = meu_Tello.field_limit   # Cell 1 Right Side Limit
cell1_usl = meu_Tello.field_limit   # Cell 1 Upper Side Limit
cell1_lsl = -meu_Tello.field_limit  # Cell 1 Left Side Limit

cell2_dsl = -meu_Tello.field_limit  # Cell 2 Down Side Limit
cell2_usl = meu_Tello.field_limit   # Cell 2 Upper Side Limit

cell3_rsl = meu_Tello.field_limit   # Cell 3 Right Side Limit
cell3_usl = meu_Tello.field_limit   # Cell 3 Upper Side Limit

movements = [
    (meu_Tello.right, lambda: (abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.forward, lambda: (abs(cell1_usl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.left, lambda: (abs(cell1_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.back, lambda: fov_Tello),
    (meu_Tello.right, lambda: (abs(cell1_rsl - meu_Tello.cur_loc[0]) - fov_by_2 - fov_by_2 + overlap)),
    (meu_Tello.back, lambda: fov_Tello),
    (meu_Tello.left, lambda: (abs(cell1_lsl - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.back, lambda: (abs(cell2_dsl - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.right, lambda: fov_Tello),
    (meu_Tello.forward, 165),
    (meu_Tello.right, lambda: fov_Tello),
    (meu_Tello.back, 165),
    (meu_Tello.right, 230),
    (meu_Tello.forward, 135),
    (meu_Tello.left, lambda: fov_Tello),
    (meu_Tello.back, 100),
    (meu_Tello.left, 90),
    (meu_Tello.forward, 135),
    (meu_Tello.left, 10),
]

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
        for command, distance in movements:
            if move_and_check(meu_Tello, command, distance) == 0: 
                stop_and_go_home = True
                break
        if stop_and_go_home == True:
            break


area_coverage()
go_home()