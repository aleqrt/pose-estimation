import datetime
import os
from flask import render_template, request, jsonify
import json
from pose_estimation.python import create_app, db
from pose_estimation.python.db_model.models import Pose, User
from pose_estimation.python.pose2d import smooth

app = create_app()


@app.before_first_request
def create_tables():
    db.create_all()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Pose': Pose}


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


@app.route("/")
def start_page():
    init_user()
    return render_template('index.html')


@app.route("/pose-ml5")
def pose_ml5():
    """
            TODO:
                - FLIP HORIZONTAL DELL'IMMAGINE IN MODO CHE DESTRA E SINISTRA COMBACINO
                - AGGIUNTA PLOT DEGLI ANGOLI IN 2D CALCOLATI
    """
    return render_template('pose_ml5.html')


@app.route("/pass_val", methods=["POST", "GET"])
def pass_val():
    """Smooth and save skeleton 2D
    """
    pose = request.values.get('value')
    # save_val(pose)  # Save pose (.json format) in directory test/script_test/keypoints
    if pose is not None:
        user = User.find_by_name("test")
        p = Pose(noisy_pose=json.dumps(pose), user_id=user.id, timestamp=datetime.datetime.now())
        p.save_to_db()
        kp, degree = smooth(pose, user)
        print(
            f"left_shoulder {degree['left_shoulder']}, left_elbow {degree['left_elbow']}, left_knee {degree['left_knee']}, right_shoulder {degree['right_shoulder']}, right_elbow {degree['right_elbow']}, right_knee {degree['right_knee']}")
        p.correct_pose = json.dumps(kp)
        p.degree = json.dumps(degree)
        p.update()
    return jsonify({'reply': 'success'})


def init_user():
    """
        TODO: - SingIn e SingUp for users. Al momento viene settato lo user 'test'
    """
    user = User(username='test')
    user_list = User.find_by_name("test")
    if user_list is None:
        user.save_to_db()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
