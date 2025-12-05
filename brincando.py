#!/usr/bin/env python

from tello_sim_EDRA import Simulator

meu_Tello = Simulator()
treasures_colected = len(meu_Tello.visited_treasures)
total_treasures = len(meu_Tello.treasures)

while True:
    meu_Tello.takeoff()

    meu_Tello.right(170)    
    meu_Tello.forward(170)

    meu_Tello.left(375)
    meu_Tello.back(70)
    meu_Tello.right(335)

    meu_Tello.back(70)
    meu_Tello.left(335)

    meu_Tello.back(200)
    meu_Tello.right(70)
    meu_Tello.forward(165)
    meu_Tello.right(70)
    meu_Tello.back(165)
    meu_Tello.right(230)
    meu_Tello.forward(135)
    meu_Tello.left(70)
    meu_Tello.back(100)
    meu_Tello.left(85)
    meu_Tello.forward(135)
    meu_Tello.left(10)

    meu_Tello.land()