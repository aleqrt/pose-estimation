import json
from datetime import datetime
import os

dir_path = os.getcwd()


def save_val(pose):
    """Save 2D pose in .json file into './keypoints' directory

    """
    now = datetime.now()
    outfile = now.strftime("%d-%b-%Y-%H-%M") + '.json'
    outfile = os.path.join(dir_path, "test", "script_test", "keypoints", outfile)
    # check if directory exist
    if not os.path.exists(os.path.join(dir_path, "test", "script_test", "keypoints")):
        os.makedirs(os.path.join(dir_path, "test", "script_test", "keypoints"))
    # check if file exist
    if not os.path.isfile(outfile):
        with open(outfile, 'w') as json_file:
            json.dump(pose, json_file, indent=4)
    else:
        with open(outfile, 'a') as json_file:
            json_file.write("\n")
            json_file.write(json.dumps(pose))
            json_file.close()
