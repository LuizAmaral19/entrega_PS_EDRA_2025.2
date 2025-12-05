from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

fov_by_2 = meu_Tello.vision_range/2
right_side_limit_x = meu_Tello.field_limit
upper_side_limit_y = meu_Tello.field_limit
left_side_limit_x = -meu_Tello.field_limit
down_side_limit_y = -meu_Tello.field_limit
overlap = 5

movements = [
    (meu_Tello.right, lambda: (abs(right_side_limit_x - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.forward, lambda: (abs(upper_side_limit_y - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.left, lambda: (abs(left_side_limit_x - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.back, lambda: fov_by_2 * 2),
    (meu_Tello.right, lambda: (abs(right_side_limit_x - meu_Tello.cur_loc[0]) - fov_by_2 - fov_by_2 + overlap)),
    (meu_Tello.back, lambda: fov_by_2 * 2),
    (meu_Tello.left, lambda: (abs(left_side_limit_x - meu_Tello.cur_loc[0]) - fov_by_2 + overlap)),
    (meu_Tello.back, lambda: (abs(down_side_limit_y - meu_Tello.cur_loc[1]) - fov_by_2 + overlap)),
    (meu_Tello.right, lambda: fov_by_2 * 2),
    (meu_Tello.forward, 165),
    (meu_Tello.right, lambda: fov_by_2 * 2),
    (meu_Tello.back, 165),
    (meu_Tello.right, 230),
    (meu_Tello.forward, 135),
    (meu_Tello.left, lambda: fov_by_2 * 2),
    (meu_Tello.back, 100),
    (meu_Tello.left, 90),
    (meu_Tello.forward, 135),
    (meu_Tello.left, 10),
]

def move_and_check(drone, command, distance):

    if callable(distance):
        distance = distance()
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