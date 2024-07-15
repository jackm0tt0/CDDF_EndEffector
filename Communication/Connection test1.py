import re
from py_openshowvar import openshowvar
import time
# import serial


# Establish connection to the KUKA robot controller
client = openshowvar('192.168.40.128', 7000)
print(client.can_connect)


if client.can_connect:
        print("Connected to KUKA robot controller successfully.")

        # Read the current value of MyPos
        start = time.time()
        mypos_initial = client.read('MyPos', debug=False)
        print(mypos_initial)

                        
        # data_str = mypos_initial.decode('utf-8')

        #         # Use regular expression to extract values
        # pattern = re.compile(r'(\w+) ([+-]?\d+\.\d+E?[+-]?\d*|[+-]?\d+\.?\d*)')
        # matches = pattern.findall(data_str)

        #         # Convert the matches to a dictionary
        # result = {key: float(value) for key, value in matches}

        #         # Print the result
        # print(result)
        # print("*" * 20)
        # print(time.time() - start)
        # print("*" * 20)

        Pos_X = 0
        Pos_Y = 0
        Pos_Z = 0
        Pos_A = 0
        Pos_B = 0
        Pos_C = 0


        basic_pos = "POS: X {:.2f}, Y {:.2f}, Z {:.2f}, A {:.2f}, B {:.2f}, C {:.2f}".format(Pos_X, Pos_Y,
                                                                                             Pos_Z, Pos_A,
                                                                                             Pos_B, Pos_C)
        pos = "{" + basic_pos + "}"
        update_pos = client.write('MyPos', pos, debug=True)



# Verify the new value of MyPos
        mypos_new = client.read('MyPos', debug=False)
        print(f"Updated MyPos: {mypos_new}")




# # Configure the serial port (adjust 'COM3' to your port and 9600 to match the baud rate in Arduino sketch)
# ser = serial.Serial('COM3', 9600, timeout=1) 

# def send_steps(steps):
#     try:
#         # Convert steps to string and send to Arduino
#         ser.write(f"{steps}\n".encode())
#         time.sleep(1)  # Adjust timing as needed
#     except Exception as e:
#         print(f"Error sending steps: {e}")

# def main():
#     while True:
#         try:
#             # Example: sending 100 steps forward
#             send_steps(100)
#             time.sleep(2)  # Wait for 2 seconds
            
#             # Example: sending -100 steps backward
#             send_steps(-100)
#             time.sleep(2)  # Wait for 2 seconds
#         except KeyboardInterrupt:
#             print("Program interrupted")
#             break

# if __name__ == "__main__":
#     main()

# # Close the serial connection
# ser.close()
