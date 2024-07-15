import cv2
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import os
import json
from Regression import *
from Serialcom import *
import RobotControl as rc

def GetSensorDistance()->float:
    read_timeout = 0.1 # seconds
    num_dist_samples = 10
    num_dist_errors = 0
    tot_dist = 0
    for i in range(num_dist_samples):      
        distance_data = connection.read_distance(read_timeout)
        if distance_data is not None:
            tot_dist += float(distance_data)
        else:
            num_dist_errors+=1
    try:
        avg_dist = tot_dist/(num_dist_samples-num_dist_errors)
    except:
        print(f"Distance was not sensed")
        return -1
    
    return avg_dist

def LoadCartridge()->bool:
    return False
    connection.send_string("insert")
    if connection.contains_string("insert", read_timeout):
        return True
    else:
        return False

def Register(capture)->tuple[bool, np.ndarray]:
    """take reference photo"""
    print("Registering Current Status")

    _ , prevframe = capture.read()

    cv2.imshow("Reference", prevframe)
    cv2.waitKey(1)

    print("Registration Complete")
    return (True,prevframe)

def Position(x,y,z,a,b,c)->bool:
    print(f"Positioning Robot", end="")

    rc.set_position(a,y,z,a,b,c)
    
    print("Positioning Complete")
    return True

def Shoot()->bool:
    input("Press Enter to Fire")
    shoot_time = 1
    print("Shooting")
    #send command to arduino
    connection.send_string("shoot")

    #listen for response when complete
    string_found = connection.contains_string("shoot", shoot_time)
    print(string_found)
    if string_found == "shoot":
        print("Shot Complete")
        return True
    else:
        return True #NOTE this should be false once its working

def Record(capture, prevframe, result_df)->tuple[bool, pd.DataFrame]:
    print("Recording Shot")
    height, width, channels = prevframe.shape
    accumulator = cv2.Mat(np.zeros((height, width), dtype=np.float32))

    # check many frames until you find something
    num_frames = 20
    for i in range(num_frames):

        if i == 0:
            for i in range(5): capture.read() # for some reason it takes a few frames to catch up

        _ , postframe = capture.read()
        diff_a = cv2.subtract(postframe, prevframe) # light on dark
        diff_b = cv2.subtract(prevframe, postframe) # dark on light
        diff = cv2.add(diff_a,diff_b) # either

        # Convert to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        binary = binary.astype(np.float32)

        # add it to the sum_frame
        accumulator = cv2.accumulate(gray.astype(np.float32), accumulator)
        #accumulator = cv2.addWeighted(accumulator,1/num_frames, binary.astype(np.float32), 1-1/num_frames, 1)

    # To get the average, divide the accumulator by the number of images
    average_image = accumulator / num_frames
    average_image = cv2.convertScaleAbs(average_image)  
    _, detection = cv2.threshold(average_image, 40, 255, cv2.THRESH_BINARY)

    cv2.imshow("Detection", detection)
    cv2.waitKey(1)

    # Find contours
    contours, _ = cv2.findContours(detection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:

        #sort contours by size
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for contour in contours:

            #no reason to look at very small contours
            if cv2.contourArea(contour) < 50: break

            copy = postframe.copy()

            # Calculate moments of the contour
            M = cv2.moments(contour)

            # Calculate the centroid (center of the object)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            # Draw the contour and center on the original image
            cv2.drawContours(copy, [contour], -1, (0, 255, 0), 2)
            #cv2.circle(copy, (cX, cY), 8, (0, 255, 0), 2)

            cv2.imshow('Reference', copy)
            cv2.waitKey(1)

            user_correct_detection = input("Is this the correct spot? y|n >>")
            if user_correct_detection == "y":
                #remapping image into domain [-1,1]
                newdata = pd.DataFrame([{
                    'imx': 2*(cX/width)-1,
                    'imy': -2*(cY/height)+1,
                    'dist': GetSensorDistance()
                }])
                result_df = pd.concat([result_df, newdata], ignore_index= True) 

                print("Record Complete")
                print(result_df.head())
                return True, result_df

        print("No Other Shots Detected")
        return False, result_df
    
    print("No Shot Detected")
    return False, result_df

# Calibration Process
# 1 Postion : directly at target
# 2 Register : state before shot
# 3 Aim : Apply Pitch and Yaw correction
# 4 Shoot : pew pew
# 5 Position : directly at target
# 6 Record : position and calc error

#establish Serial Connection with Arduino
port = 'COM9'
baudrate = 9600
connection = SerialConnection(port, baudrate)
connection.open()
connection.send_string("Hello, Serial Port!")

#confirm that it is connected
connection_max_attempts = 3
connection_attempts = 0
while connection_attempts< connection_max_attempts:
    if connection.read_string(1):
        #load the cartridge
        input("Press Enter to Insert the Cartridge")
        if LoadCartridge(): break
    connection_attempts+=1

#connect to robot
rob_connected, robot_client = rc.connect(ip_address = "'192.168.2.3'", port = 7000)
if not rob_connected: raise Exception("Not connected to Robot")


# 3 for OBS studio
capture = cv2.VideoCapture(2)
isVideoConnected , testframe = capture.read()
if not isVideoConnected: raise Exception("The video is not setup correctly")
cv2.imshow("Reference", testframe)
cv2.waitKey(1)

# setup for calibration sequence
# state = IDLE

ROOT = os.getcwd()
target_path = ROOT + r"\Targets\targets_test.json"

with open(target_path, 'r') as file:
    t_dict = json.loads(file.read())

# #only do one shot #NOTE comment this out!!!!
# t_dict["Targets"] = [t_dict["Targets"][0]]

target_df = pd.DataFrame(t_dict["Targets"])

result_df = pd.DataFrame(columns= ['imx','imy'])

# begin calibration sequence
sample_count = 0
print(len(target_df))
while sample_count < len(target_df):

    # sample count
    sample_count += 1
    print(f"\n--- Sample {sample_count} ---")

    # 1 Position : aimed directly at target
    target = target_df.loc[sample_count-1]

    positioned = Position(
        target["pos_x"],
        target["pos_y"],
        target["pos_z"],
        target["target_a"],
        target["target_b"],
        target["target_c"],
    )
    if not positioned: raise Exception("Positioning Failed")

    # 2 Register : state before shot
    registered, prevframe =  Register(capture)
    if not registered: raise Exception("Registration Failed")

    # 3 Aim : Apply Pitch and Yaw correction
    aimed = Position(
        target["pos_x"],
        target["pos_y"],
        target["pos_z"],
        target["pos_a"],
        target["pos_b"],
        target["pos_c"],
    )
    if not aimed: raise Exception("Aiming Failed")

    # 4 Shoot : pew pew
    if not Shoot(): raise Exception("Shooting Failed")
    
    # 5 Aim : directly at target
    repositioned = Position(
        target["pos_x"],
        target["pos_y"],
        target["pos_z"],
        target["target_a"],
        target["target_b"],
        target["target_c"],
    )
    if not repositioned: raise Exception("Repositioning Failed")

    # 6 Record : position and calc error
    recorded = False
    while not recorded:
        recorded, result_df = Record(capture, prevframe, result_df)
        if not recorded:
            while(True):
                user_txt = input("Press s to shoot again\nPress r to record again\nPress q to abort program\n>>")
                if user_txt == "s": 
                    positioned = Position(
                        target["pos_x"],
                        target["pos_y"],
                        target["pos_z"],
                        target["target_a"],
                        target["target_b"],
                        target["target_c"],
                    )
                    if not positioned: raise Exception("Positioning Failed")

                    # 2 Register : state before shot
                    registered, prevframe =  Register(capture)
                    if not registered: raise Exception("Registration Failed")

                    # 3 Aim : Apply Pitch and Yaw correction
                    aimed = Position(
                        target["pos_x"],
                        target["pos_y"],
                        target["pos_z"],
                        target["pos_a"],
                        target["pos_b"],
                        target["pos_c"],
                    )
                    if not aimed: raise Exception("Aiming Failed")

                    print("Shooting Again")
                    shot = Shoot()
                    if not shot: raise Exception("Shooting Failed")
                    break
                elif user_txt == "r":
                    print("Recording Again")
                    break
                    

print(result_df.head())
plt.xlim((-1,1))
plt.ylim((-1,1))
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.scatter(result_df['imx'], result_df['imy'])
plt.show(block = False)

model_dir = ROOT + r"\Models/"
FitCalibrationFunction(target_df, result_df, model_dir, mode = "polynomial")

input("Press any key to close >>")
capture.release()
cv2.destroyAllWindows()
connection.close()
robot_client.close()