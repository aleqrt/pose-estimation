import datetime
from pose_estimation.python import db


class User(db.Model):
    """Data model of user.

    Columns:
        id: int, sequence
        username: string
        poses: all 2D poses of one user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    poses = db.relationship('Pose', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<User: id {}, username {}>'.format(self.id, self.username)

    def save_to_db(self):
        """Commit a new row to db

        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, username):
        """Returns all users

        Param
        -----
            username : string

        Returns
        -------
         User
             user by username
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        """Returns a json-formatted output of the current state

        Returns
        -------
        dict
            with a list of username dictionaries
        """

        def to_json(x):
            return {
                'username': x.username
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        """Deletes all entries of data-model

        Returns
        -------
        dict
            with number of rows deleted, if completed, or with standard message otherwise
        """
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


class Pose(db.Model):
    """Data model of 2D pose from PoseNet.

    Columns:
        id: int, sequence
        noisy_pose: string, 2D pose
        correct_pose: string, 2D pose
        degree: string, dictionary of degrees of joint's angles
        user_id: int, define which user do the 2D pose
        time: date, timestamp of pose used in OneEuroFilter
    """
    id = db.Column(db.Integer, primary_key=True)
    noisy_pose = db.Column(db.String(255), index=True)
    correct_pose = db.Column(db.String(255), index=True)
    degree = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<correct_pose {}>'.format(self.correct_pose)

    def save_to_db(self):
        """Commit a new row to db

        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls):
        """Upgrade row into db

        """
        db.session.commit()

    @classmethod
    def delete_all(cls):
        """Deletes all entries of data-model

        Returns
        -------
        dict
            with number of rows deleted, if completed, or with standard message otherwise
        """
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def first_pose_per_user(cls, user_id):
        """Returns the 2D pose

        Param
        -----
            user_id : integer

        Returns
        -------
        dict
            first pose by user_id
        """
        try:
            p = cls.query.filter_by(user_id=user_id).order_by(Pose.id).first()
            return p
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def last_pose_per_user(cls, user_id):
        """Returns the 2D pose

        Param
        -----
            user_id : integer

        Returns
        -------
        dict
            Last pose by user_id
        """
        try:
            p = cls.query.filter_by(user_id=user_id).order_by(Pose.id.desc()).first()
            return p
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def last_three_pose_per_user(cls, user_id):
        """Returns the 2D pose

        Param
        -----
            user_id : integer

        Returns
        -------
        dict
            Last five pose by user_id
        """
        try:
            p = cls.query.filter_by(user_id=user_id).order_by(Pose.id.desc())
            p = p[-3:]
            return p
        except:
            return {'message': 'Something went wrong'}
