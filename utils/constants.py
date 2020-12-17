PART_NAMES = [
    "nose", "leftEye", "rightEye", "leftEar", "rightEar", "leftShoulder",
    "rightShoulder", "leftElbow", "rightElbow", "leftWrist", "rightWrist",
    "leftHip", "rightHip", "leftKnee", "rightKnee", "leftAnkle", "rightAnkle"
]

NUM_KEYPOINTS = len(PART_NAMES)

PART_IDS = {pn: pid for pid, pn in enumerate(PART_NAMES)}

CONNECTED_PART_NAMES = [
    ("leftHip", "leftShoulder"), ("leftElbow", "leftShoulder"),
    ("leftElbow", "leftWrist"), ("leftHip", "leftKnee"),
    ("leftKnee", "leftAnkle"), ("rightHip", "rightShoulder"),
    ("rightElbow", "rightShoulder"), ("rightElbow", "rightWrist"),
    ("rightHip", "rightKnee"), ("rightKnee", "rightAnkle"),
    ("leftShoulder", "rightShoulder"), ("leftHip", "rightHip"),
    ("nose", "leftEye"), ("leftEye", "leftEar"),
    ("nose", "rightEye"), ("rightEye", "rightEar")
]

CONNECTED_PART_INDICES = [(PART_IDS[a], PART_IDS[b]) for a, b in CONNECTED_PART_NAMES]

"""
List of tuples indicating the indices of the pairs of points, in PART_NAMES, necessary for the calculation of the joint 
angles

Example:
    The tuple list [(11, 5), (7, 5)], indicates the following keypoints:  
        11: leftHip
        5: leftShoulder
        7: leftElbow
    Using this list of tuples I can calculate the internal angle of the shoulder. 
    
    Note:
    Refer to the skeleton returned by PoseNet to interpret the angles.
"""
ANGLE_PART_INDICES = [
    [(11, 5), (7, 5)],  # Left Shoulder Angle (Intern)
    [(7, 5), (7, 9)],  # Left Elbow Angle
    [(11, 13), (13, 15)],  # Left Knee Angle
    [],  # Left Hip Angle
    [(12, 6), (8, 6)],  # Right Shoulder Angle (Intern)
    [(8, 6), (8, 10)],  # Right Elbow Angle
    [(12, 14), (14, 16)],  # Right Knee Angle
    []   # Right Hip Angle
]
