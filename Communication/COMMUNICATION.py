# import re
from py_openshowvar import openshowvar
import time


# Establish connection to the KUKA robot controller
client = openshowvar('192.168.40.129', 7000)
print(client.can_connect)


if client.can_connect:
        print("Connected to KUKA robot controller successfully.")

        # Read the current value of MyPos
        start = time.time()
        mypos_initial = client.read('MyPos', debug=False)
        print(mypos_initial)                        

        Pos_X = 50
        Pos_Y = 50
        Pos_Z = 50
        Pos_A = 0
        Pos_B = 0
        Pos_C = 50


        basic_pos = "POS: X {:.2f}, Y {:.2f}, Z {:.2f}, A {:.2f}, B {:.2f}, C {:.2f}".format(Pos_X, Pos_Y,
                                                                                             Pos_Z, Pos_A,
                                                                                             Pos_B, Pos_C)
        pos = "{" + basic_pos + "}"
        update_pos = client.write('MyPos', pos, debug=True)



# Verify the new value of MyPos
        mypos_new = client.read('MyPos', debug=False)
        print(f"Updated MyPos: {mypos_new}")

client.close()
