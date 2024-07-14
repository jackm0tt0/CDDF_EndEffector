import cv2
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

def Register(capture, target)->bool:
    """Orient Camera toward the target and take base photo"""
    print("Registering Current Status")

    _ , prevframe = capture.read()

    cv2.imshow("Calibration Sequence", prevframe)
    cv2.waitKey(1)

    print("Registration Complete")
    return True

def Aim(target)->bool:
    print("Aiming Robot", end="")
    for i in range(5):
        time.sleep(0.05)
        print(".", flush= True, end="")
    print("Aiming Complete")
    return True

def Shoot()->bool:
    print("Shooting")
    input("press any key to continue")
    print("Shot Complete")
    return True

def Record(capture, target, result_df)->tuple[bool, pd.DataFrame]:
    print("Recording Shot")

    prevframe = target['frame']
    height, width, channels = prevframe.shape
    accumulator = cv2.Mat(np.zeros((height, width), dtype=np.float32))

    # check many frames until you find something
    num_frames = 20
    for i in range(num_frames):

        _ , postframe = capture.read()
        diff_a = cv2.subtract(postframe, prevframe) # light on dark
        diff_b = cv2.subtract(prevframe, postframe) # dark on light
        diff = cv2.add(diff_a,diff_b) # either

        # Convert to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, binary = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
        binary = binary.astype(np.float32)

        # add it to the sum_frame
        accumulator = cv2.accumulate(binary, accumulator)
        #accumulator = cv2.addWeighted(accumulator,1/num_frames, binary.astype(np.float32), 1-1/num_frames, 1)

    # To get the average, divide the accumulator by the number of images
    average_image = accumulator / num_frames
    average_image = cv2.convertScaleAbs(average_image)  
    _, detection = cv2.threshold(average_image, 200, 255, cv2.THRESH_BINARY)

    frame = detection

    # Find contours
    contours, _ = cv2.findContours(average_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
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

            cv2.imshow('Calibration Sequence', copy)
            cv2.waitKey(1)

            user_correct_detection = input("Is this the correct spot? y|n >>")
            if user_correct_detection == "y":
                #remapping image into domain [-1,1]
                newdata = pd.DataFrame([{
                    'x': 2*(cX/width)-1,
                    'y': -2*(cY/height)+1
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
# 1 Aim : directly at target
# 2 Register : state before shot
# 3 Aim : Apply Pitch and Yaw correction
# 4 Shoot : pew pew
# 5 Aim : directly at target
# 6 Record : position and calc error


# 3 for OBS studio
capture = cv2.VideoCapture(3)
isVideoConnected , testframe = capture.read()
if not isVideoConnected: raise Exception("The video is not setup correctly")
cv2.imshow("Calibration Sequence", testframe)
cv2.waitKey(1)

# setup for calibration sequence
# state = IDLE

target_df = pd.DataFrame(columns= ['x', 'y', 'z', 'pitch', 'yaw', 'distance', 'power'])

result_df = pd.DataFrame(columns= ['imx','imy'])

# begin calibration sequence
sample_count = 0
while sample_count < len(target_df):
    sample_count += 1
    print(f"\n--- Sample {sample_count} ---")

    # Aim Robot Directly at Target
    aimed = Aim(target_df.loc[sample_count-1])
    if not aimed: raise Exception("Aiming Failed")

    # Orient robot to target and take reference photo
    registered, target_df = Register(capture, target_df)
    if not aimed: raise Exception("Registration Failed")

    # Shoot 
    shot = Shoot()
    if not shot: raise Exception("Shooting Failed")

    # Return robot to reference location
    # Detect the shot and record data
    recorded = False
    while not recorded:
        recorded, result_df = Record(capture, target_df.loc[sample_count-1] , result_df)
        if not recorded:
            while(True):
                user_txt = input("Press s to shoot again\nPress r to record again\n>>")
                if user_txt == "s": 
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
plt.scatter(result_df['imx'], result_df['imy'])
plt.show(block = False)



input("Press any key to close >>")
capture.release()
cv2.destroyAllWindows()