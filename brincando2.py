from tello_sim_EDRA import Simulator

meu_Tello = Simulator()

radius_fov_Tello = meu_Tello.vision_range/2
# field

def move_and_check(drone, command, distance):
    command(distance)
    return len(drone.visited_treasures) - len(drone.treasures)

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

current_x = float(meu_Tello.cur_loc[0])
current_y = float(meu_Tello.cur_loc[1])
if current_x >=0 and current_y >=0:
    meu_Tello.back(current_y)
    meu_Tello.left(current_x)
elif current_x < 0 and current_y >=0:
    meu_Tello.back(current_y)
    meu_Tello.right(abs(current_x))
elif current_x < 0 and current_y < 0:
    meu_Tello.forward(abs(current_y))
    meu_Tello.right(abs(current_x))
elif current_x >= 0 and current_y < 0:
    meu_Tello.forward(abs(current_y))
    meu_Tello.left(abs(current_x))
meu_Tello.land()