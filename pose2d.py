import json
import numpy as np
from scipy.spatial import distance
from pose_estimation.python.db_model.models import Pose
from pose_estimation.python.utils.one_euro_filter import OneEuroFilter
from .utils.constants import NUM_KEYPOINTS, CONNECTED_PART_INDICES, ANGLE_PART_INDICES


def angle_between(p0, p1, p2):
    """ Returns the angle in degree for [p0 p1 p2] corner
    """
    v0 = np.array(p1) - np.array(p0)
    gamma = np.arctan2(v0[1], v0[0])
    v1 = np.array(p2) - np.array(p1)
    v1_t = np.array([v1[0] * np.cos(gamma) + v1[1] * np.sin(gamma), -(v1[0] * np.sin(gamma)) + v1[1] * np.cos(gamma)])
    angle = np.arctan2(v1_t[1], v1_t[0])
    return np.degrees(angle)


def skeleton_dist(skl1, skl2):
    """Euclidean Distance between coordinates of two skeletons

    Parameters
    ---------
    skl1: coordinates x,y of skeleton 1
    skl2: coordinates x,y of skeleton 2

    Return
    ---------
    Euclidean Distance
    """
    return distance.euclidean(skl1, skl2)


def smooth(pose, user):
    """ Function to correct 2D pose.

    Param:
        - pose: Pose object
        - user: User object

    Return:
        - kp: 2D pose corrected by filtering
        - degree: Degree angles of joint
    """
    kp = json.loads(pose)
    pose_prc = Pose.last_pose_per_user(1)
    if pose_prc.correct_pose is not None:
        kp_prc = json.loads(pose_prc.correct_pose)
        for n in range(NUM_KEYPOINTS):
            dist = skeleton_dist(np.array((kp.get('keypoints')[n].get("position").get("x"),
                                           kp.get('keypoints')[n].get("position").get("y"))),
                                 np.array((kp_prc.get('keypoints')[n].get("position").get("x"),
                                           kp_prc.get('keypoints')[n].get("position").get("y"))))
            if dist > 10:
                kp['keypoints'][n]['position']['x'] = np.sum(np.array([0.75 * kp['keypoints'][n]['position']['x'],
                                                                       0.25 * kp_prc.get('keypoints')[n].get(
                                                                           "position").get("x")]))
                kp['keypoints'][n]['position']['y'] = np.sum(np.array([0.75 * kp['keypoints'][n]['position']['y'],
                                                                       0.25 * kp_prc.get('keypoints')[n].get(
                                                                           "position").get("y")]))
    degree = compute_degree(kp)
    return kp, degree


def compute_degree(kp, min_part_confidence=0.15):
    """Compute joint's angles of 2D pose
    """
    x = []
    y = []
    left_shoulder = 0
    left_elbow = 0
    left_knee = 0
    right_shoulder = 0
    right_elbow = 0
    right_knee = 0
    for n in range(NUM_KEYPOINTS):
        ks = kp['keypoints'][n].get('score')
        if ks >= min_part_confidence:
            x.append(kp['keypoints'][n].get('position').get('x'))
            y.append(kp['keypoints'][n].get('position').get('y'))
    for n in range(len(CONNECTED_PART_INDICES)):
        if CONNECTED_PART_INDICES[n][0] < len(x) and CONNECTED_PART_INDICES[n][1] < len(x):
            p0 = x[CONNECTED_PART_INDICES[n][0]], y[CONNECTED_PART_INDICES[n][0]]
            p1 = x[CONNECTED_PART_INDICES[n][1]], y[CONNECTED_PART_INDICES[n][1]]
            for i in range(n + 1, len(CONNECTED_PART_INDICES)):
                if CONNECTED_PART_INDICES[i][0] < len(x) and CONNECTED_PART_INDICES[i][1] < len(x):
                    ANGLE_BETWEEN = [CONNECTED_PART_INDICES[n], CONNECTED_PART_INDICES[i]]
                    if CONNECTED_PART_INDICES[i][0] != CONNECTED_PART_INDICES[n][0] \
                            and CONNECTED_PART_INDICES[i][0] != CONNECTED_PART_INDICES[n][1]:
                        p2 = x[CONNECTED_PART_INDICES[i][0]], y[CONNECTED_PART_INDICES[i][0]]
                    else:
                        p2 = x[CONNECTED_PART_INDICES[i][1]], y[CONNECTED_PART_INDICES[i][1]]
                    if ANGLE_BETWEEN == ANGLE_PART_INDICES[0]:
                        left_shoulder = 180 - angle_between(p0, p1, p2)
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[1]:
                        left_elbow = angle_between(p1, p0, p2)
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[2]:
                        left_knee = angle_between(p0, p1, p2)
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[4]:
                        right_shoulder = 180 - angle_between(p0, p1, p2)
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[5]:
                        right_elbow = angle_between(p1, p0, p2)
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[6]:
                        right_knee = angle_between(p0, p1, p2)
    return dict([('left_shoulder', left_shoulder), ('left_elbow', left_elbow),
                 ('left_knee', left_knee), ('right_shoulder', right_shoulder),
                 ('right_elbow', right_elbow), ('right_knee', right_knee)])
