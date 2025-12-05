from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

radius_fov_Tello = meu_Tello.vision_range/2
# field

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


while True:
    meu_Tello.takeoff()

    if (move_and_check(meu_Tello, meu_Tello.right, 170)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.forward, 170)) == 0: break

    if (move_and_check(meu_Tello, meu_Tello.left, 375)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.back, 70)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.right, 335)) == 0: break

    if (move_and_check(meu_Tello, meu_Tello.back, 70)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.left, 335)) == 0: break

    if (move_and_check(meu_Tello, meu_Tello.back, 200)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.right, 70)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.forward, 165)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.right, 70)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.back, 165)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.right, 230)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.forward, 135)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.left, 70)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.back, 100)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.left, 90)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.forward, 135)) == 0: break
    if (move_and_check(meu_Tello, meu_Tello.left, 10)) == 0: break

go_home()