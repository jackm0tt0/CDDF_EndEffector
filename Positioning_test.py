import os
import pandas as pd
import json
import RobotControl as rc
import time

connected, client = rc.connect()

if connected:

    ROOT = os.getcwd()
    target_path = ROOT + r"\Targets\targets_test.json"

    with open(target_path, 'r') as file:
        t_dict = json.loads(file.read())

    target_df = pd.DataFrame(t_dict["Targets"])

    print(target_df.head())

    for i in range(len(target_df)-1):
        target = target_df.loc[i]

        #aim at target
        rc.set_position(
            client,
            target["pos_x"],
            target["pos_y"],
            target["pos_z"],
            target["pos_a"],
            target["pos_b"],
            target["pos_c"]
            )
        
        time.sleep(1)
        #adjust pitch and yaw
        rc.set_position(
            client,
            target["pos_x"],
            target["pos_y"],
            target["pos_z"],
            target["target_a"],
            target["target_b"],
            target["target_c"]
        )
        
        time.sleep(1)
        #aim back at target
        rc.set_position(
            client,
            target["pos_x"],
            target["pos_y"],
            target["pos_z"],
            target["pos_a"],
            target["pos_b"],
            target["pos_c"]
            )

client.close()

