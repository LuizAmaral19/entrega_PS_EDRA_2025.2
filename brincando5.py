from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

radius_fov_Tello = meu_Tello.vision_range/2
field_length = meu_Tello.field_limit
overlap = 5

movements = [
    (meu_Tello.right, 170),
    (meu_Tello.forward, 170),
    (meu_Tello.left, 375),
    (meu_Tello.back, 70),
    (meu_Tello.right, 335),
    (meu_Tello.back, 70),
    (meu_Tello.left, 335),
    (meu_Tello.back, 200),
    (meu_Tello.right, 70),
    (meu_Tello.forward, 165),
    (meu_Tello.right, 70),
    (meu_Tello.back, 165),
    (meu_Tello.right, 230),
    (meu_Tello.forward, 135),
    (meu_Tello.left, 70),
    (meu_Tello.back, 100),
    (meu_Tello.left, 90),
    (meu_Tello.forward, 135),
    (meu_Tello.left, 10),
]

def move_and_check(drone, command, distance):
    command(distance)
    return len(drone.visited_treasures) - len(drone.treasures)


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