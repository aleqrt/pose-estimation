import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import distance

from pose_estimation.python.utils.constants import NUM_KEYPOINTS, CONNECTED_PART_INDICES, ANGLE_PART_INDICES
from pose_estimation.python.utils.one_euro_filter import OneEuroFilter
from pose_estimation.python.utils.tictoc import tic, toc

dir_path = os.getcwd()


def angle_between(p0, p1, p2):
    """ Returns the angle in degree for [p0 p1 p2] corner
    """
    # v0 = np.array(p1) - np.array(p0)
    # v1 = np.array(p2) - np.array(p1)
    # return np.degrees(np.arccos(np.dot(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1))))
    v0 = np.array(p1) - np.array(p0)
    gamma = np.arctan2(v0[1], v0[0])
    v1 = np.array(p2) - np.array(p1)
    v1_t = np.array([v1[0]*np.cos(gamma) + v1[1]*np.sin(gamma), -(v1[0]*np.sin(gamma)) + v1[1]*np.cos(gamma)])
    angle = np.arctan2(v1_t[1], v1_t[0])
    return np.degrees(angle)


def skeleton_dist(sk1, sk2):
    """Euclidean Distance between coordinates of two skeletons

    Parameter
    ---------
    sk1: coordinates x,y of skeleton 1
    sk2: coordinates x,y of skeleton 2

    Return
    ---------
        Euclidean Distance
    """
    return distance.euclidean(sk1, sk2)


def load(path):
    """Load all .json files with coordinates of skeleton from '/keypoints' directory

    Parameters
    ---------
        path: directory with .json files

    Return
    ---------
        dictionary of keypoints
    """
    files = os.listdir(path)
    kp = []
    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            data = f.readlines()
        for i in range(len(data)):
            kp.append(json.loads(data[i]))
    return kp


def smooth():
    """Correct 2D pose.

       Check the distance of the keypoints between a frame and the previous one.
    """
    tic()
    cwd = os.path.join(dir_path, 'keypoints')
    kp_list = load(cwd)
    kp_corr = []
    kp_prc = None
    min_cutoff = 0.004
    beta = 0.7
    frames = len(kp_list)
    start = 0
    end = 4 * np.pi
    t = np.linspace(start, end, frames)
    count = 1
    one_euro_filter_list = []
    for n in range(NUM_KEYPOINTS):
        xy_noisy = json.loads(kp_list[0])
        # Inizializzo OneEuroFilter per la coordinata x
        one_euro_filter = OneEuroFilter(
            0, xy_noisy['keypoints'][n]['position']['x'],
            min_cutoff=min_cutoff,
            beta=beta
        )
        one_euro_filter_list.append(one_euro_filter)
        # Inizializzo OneEuroFilter per la coordinata  y
        one_euro_filter = OneEuroFilter(
            0, xy_noisy['keypoints'][n]['position']['y'],
            min_cutoff=min_cutoff,
            beta=beta
        )
        one_euro_filter_list.append(one_euro_filter)
    for kp_frame in kp_list:
        kp = json.loads(kp_frame)
        if kp_prc is None:
            kp_prc = kp
        else:
            # for n in range(NUM_KEYPOINTS):
            #     dist = skeleton_dist(np.array((kp.get('keypoints')[n].get("position").get("x"),
            #                                    kp.get('keypoints')[n].get("position").get("y"))),
            #                          np.array((kp_prc.get('keypoints')[n].get("position").get("x"),
            #                                    kp_prc.get('keypoints')[n].get("position").get("y"))))
            #     if dist > 10:
            #         kp['keypoints'][n]['position']['x'] = np.sum(np.array([0.75 * kp['keypoints'][n]['position']['x'],
            #                                                                0.25 * kp_prc.get('keypoints')[n].get(
            #                                                                    "position").get("x")]))
            #         kp['keypoints'][n]['position']['y'] = np.sum(np.array([0.75 * kp['keypoints'][n]['position']['y'],
            #                                                                0.25 * kp_prc.get('keypoints')[n].get(
            #                                                                    "position").get("y")]))
            '''Per ogni keypoints inizializzo il OneEuroFilter per la coordinata x e y'''
            if count < (len(t)):
                for n in range(NUM_KEYPOINTS):
                    one_euro_filter_x = one_euro_filter_list[2*n]
                    one_euro_filter_y = one_euro_filter_list[2*n + 1]
                    kp['keypoints'][n]['position']['x'] = one_euro_filter_x(t[count], kp['keypoints'][n]['position']['x'])
                    kp['keypoints'][n]['position']['y'] = one_euro_filter_y(t[count], kp['keypoints'][n]['position']['y'])
            kp_prc = kp
            count = count + 1
        kp_corr.append(kp)
    toc()
    return kp_corr


def animate(frame, min_part_confidence=0.1):
    """Animated 2D plot of keypoints for each frame
    """
    plt.cla()
    plt.title('2D Pose')
    plt.xlim([0, 640])
    plt.ylim([-480, 0])
    x = []
    y = []
    for n in range(NUM_KEYPOINTS):
        ks = frame['keypoints'][n].get('score')
        if ks >= min_part_confidence:
            x.append(frame['keypoints'][n].get('position').get('x'))
            y.append(frame['keypoints'][n].get('position').get('y'))
    for n in range(len(CONNECTED_PART_INDICES)):
        if CONNECTED_PART_INDICES[n][0] < len(x) and CONNECTED_PART_INDICES[n][1] < len(x):
            p0 = x[CONNECTED_PART_INDICES[n][0]], y[CONNECTED_PART_INDICES[n][0]]
            p1 = x[CONNECTED_PART_INDICES[n][1]], y[CONNECTED_PART_INDICES[n][1]]
            plt.plot(np.array([p0[0], p1[0]]), np.dot(-1, np.array([p0[1], p1[1]])), 'b-o')
            for i in range(n + 1, len(CONNECTED_PART_INDICES)):
                ANGLE_BETWEEN = [CONNECTED_PART_INDICES[n], CONNECTED_PART_INDICES[i]]
                if CONNECTED_PART_INDICES[i][0] < len(x) and CONNECTED_PART_INDICES[i][1] < len(x):
                    if CONNECTED_PART_INDICES[i][0] != CONNECTED_PART_INDICES[n][0] \
                            and CONNECTED_PART_INDICES[i][0] != CONNECTED_PART_INDICES[n][1]:
                        p2 = x[CONNECTED_PART_INDICES[i][0]], y[CONNECTED_PART_INDICES[i][0]]
                    else:
                        p2 = x[CONNECTED_PART_INDICES[i][1]], y[CONNECTED_PART_INDICES[i][1]]
                    if ANGLE_BETWEEN == ANGLE_PART_INDICES[0]:
                        left_shoulder.append(180 - angle_between(p0, p1, p2))
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[1]:
                        left_elbow.append(angle_between(p1, p0, p2))
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[2]:
                        left_knee.append(angle_between(p0, p1, p2))
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[4]:
                        right_shoulder.append(180 - angle_between(p0, p1, p2))
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[5]:
                        right_elbow.append(angle_between(p1, p0, p2))
                    elif ANGLE_BETWEEN == ANGLE_PART_INDICES[6]:
                        right_knee.append(angle_between(p0, p1, p2))


def plot_angles():
    """Plot trend of 2D pose's angles
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(321)
    ax1.set_title('Left Shoulder'), ax1.set_ylabel('Degree °')
    plt.plot(np.linspace(0, 1, num=len(left_shoulder)), left_shoulder, '-o')

    ax2 = fig.add_subplot(323)
    ax2.set_title('Left Elbow'), ax2.set_ylabel('Degree °')
    plt.plot(np.linspace(0, 1, num=len(left_elbow)), left_elbow, '-o')

    ax3 = fig.add_subplot(325)
    ax3.set_title('Left Knee'), ax3.set_ylabel('Degree °')
    plt.plot(np.linspace(0, 1, num=len(left_knee)), left_knee, '-o')

    ax4 = fig.add_subplot(322)
    ax4.set_title('Right Shoulder'), ax4.set_ylabel('Degree °')
    plt.plot(np.linspace(0, 1, num=len(right_shoulder)), right_shoulder, '-o')

    ax5 = fig.add_subplot(324)
    ax5.set_title('Right Elbow'), ax5.set_ylabel('Degree °')
    plt.plot(np.linspace(0, 1, num=len(right_elbow)), right_elbow, '-o')

    ax6 = fig.add_subplot(326)
    ax6.set_title('Right Knee'), ax6.set_ylabel('Degree °')
    ax6.plot(np.linspace(0, 1, num=len(right_knee)), right_knee, '-o')


def remove_noisy_angles():
    for i in range(len(left_shoulder)):
        if 1 < i < (len(left_shoulder) - 1) and (left_shoulder[i] > 2 * left_shoulder[i - 1] and left_shoulder[i] > 2 * left_shoulder[i + 1]):
            left_shoulder[i] = (left_shoulder[i-1] + left_shoulder[i+1])/2
    for i in range(len(left_elbow)):
        if 1 < i < (len(left_elbow) - 1) and (left_elbow[i] > 1.5 * left_elbow[i - 1] or left_elbow[i] > 1.5 * left_elbow[i + 1]):
            left_elbow[i] = (left_elbow[i-1] + left_elbow[i+1])/2
    for i in range(len(left_knee)):
        if 1 < i < (len(left_knee) - 1) and (left_knee[i] > 2 * left_knee[i - 1] and left_knee[i] > 2 * left_knee[i + 1]):
            left_knee[i] = (left_knee[i-1] + left_knee[i+1])/2
    for i in range(len(right_shoulder)):
        if 1 < i < (len(right_shoulder) - 1) and (right_shoulder[i] > 2 * right_shoulder[i - 1] and right_shoulder[i] > 2 * right_shoulder[i + 1]):
            right_shoulder[i] = (right_shoulder[i-1] + right_shoulder[i+1])/2
    for i in range(len(right_elbow)):
        if 1 < i < (len(right_elbow) - 1) and (right_elbow[i] > 1.5 * right_elbow[i - 1] or right_elbow[i] > 1.5 * right_elbow[i + 1]):
            right_elbow[i] = (right_elbow[i-1] + right_elbow[i+1])/2
    for i in range(len(left_shoulder)):
        if 1 < i < (len(right_knee) - 1) and (right_knee[i] > 2 * right_knee[i - 1] and right_knee[i] > 2 * right_knee[i + 1]):
            right_knee[i] = (right_knee[i-1] + right_knee[i+1])/2


if __name__ == '__main__':
    kp_frames = smooth()

# Init angles
left_shoulder = []
left_elbow = []
left_knee = []
left_hip = []
right_shoulder = []
right_elbow = []
right_knee = []
right_hip = []

ani = FuncAnimation(plt.gcf(), animate, frames=kp_frames, repeat=False, interval=10)

plt.show()
