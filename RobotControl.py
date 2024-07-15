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

def read_position(client):

        # Read the current value of MyPos
        start = time.time()
        mypos_initial = client.read('MyPos', debug=False)
        print(mypos_initial)       
        return mypos_initial     

def set_position(client, Pos_X, Pos_Y,Pos_Z, Pos_A, Pos_B, Pos_C)->bool:

        basic_pos = "POS: X {:.2f}, Y {:.2f}, Z {:.2f}, A {:.2f}, B {:.2f}, C {:.2f}".format(Pos_X, Pos_Y,Pos_Z, Pos_A, Pos_B, Pos_C)
        pos = "{" + basic_pos + "}"
        client.write('MyPos', pos, debug=True)

        # Verify the new value of MyPos
        mypos_new = client.read('MyPos', debug=False)
        print(f"Updated MyPos: {mypos_new}")
        return True


