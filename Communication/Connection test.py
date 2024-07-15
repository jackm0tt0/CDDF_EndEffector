import re
from py_openshowvar import openshowvar

# Establish connection to the KUKA robot controller
client = openshowvar('192.168.40.128', 7000)
print(client.can_connect)

if client.can_connect:
        print("Connected to KUKA robot controller successfully.")

        # Read the current value of MyPos
        mypos_initial = client.read('MyPos', debug=False)
        print(mypos_initial)
        Pos_Act = client.read('MyPos', debug=True)
        print(Pos_Act)

#         # Define a new position for MyPos
#         new_position = "{X 100, Y 200, Z 300, A 10, B 20, C 30}"
        
#         # Write the new position to MyPos
#         client.write('MyPos', new_position)
#         print(f"MyPos changed to: {new_position}")

#         # Verify the new value of MyPos
#         mypos_new = client.read('MyPos', debug=False)
#         print(f"Updated MyPos: {mypos_new}")

#         # Close the connection
#         # client.close()
#         # print("Connection closed.")
# else:
#         print("Failed to connect to KUKA robot controller.")

