# import re
from py_openshowvar import openshowvar
import time

def connect(ip_address ='192.168.2.3', port = 7000)->tuple[bool, openshowvar]:

        print("connecting")

        # Establish connection to the KUKA robot controller
        client = openshowvar(ip_address, port)
        print(client.can_connect)

        if client.can_connect:
                print("Connected to KUKA robot controller successfully.")
                return (True, client)
        
        return False,None

def parse_position_string(pos_string)->list[float]:
        split = pos_string.split(",")
        pos_vals = []
        for thing in split:
                thing = thing.split(" ")[2]
                thing = thing.split("}")[0]
                pos_vals.append(float(thing))

        return pos_vals

def read_position(client)->str:

        # Read the current value of MyPos
        start = time.time()
        mypos_initial = client.read('POS_ACT_MES', debug=False)
        print(mypos_initial)

        return mypos_initial

def compare_position(pos_a, pos_b, tol):
        print("comparing positions")
        for a,b in zip(pos_a, pos_b):
                print(a,b)
                if a-b > tol: return False
        return True

def set_position(client, Pos_X, Pos_Y,Pos_Z, Pos_A, Pos_B, Pos_C)->bool:

        basic_pos = "POS: X {:.2f}, Y {:.2f}, Z {:.2f}, A {:.2f}, B {:.2f}, C {:.2f}".format(Pos_X, Pos_Y,Pos_Z, Pos_A, Pos_B, Pos_C)
        pos = "{" + basic_pos + "}"
        client.write('MyPos', pos, debug=True)

        # Verify the new value of MyPos
        mypos_new = client.read('MyPos', debug=False)
        print(f"Updated MyPos: {mypos_new}")

        # Wait until the robot gets there
        pos_val = parse_position_string(pos)
        
        while True:
                rob_val = parse_position_string(read_position())
                if compare_position(pos_val, rob_val): break
                time.sleep(0.1)
        return True

Pos_X, Pos_Y,Pos_Z, Pos_A, Pos_B, Pos_C = 1.23, 4.56, 1.23, 4.56, 1.23, 4.56
basic_pos = "POS: X {:.2f}, Y {:.2f}, Z {:.2f}, A {:.2f}, B {:.2f}, C {:.2f}".format(Pos_X, Pos_Y,Pos_Z, Pos_A, Pos_B, Pos_C)
pos = "{" + basic_pos + "}"
print(pos)
print(parse_position_string(pos))
