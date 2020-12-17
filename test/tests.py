import unittest
from pose_estimation.python import Config, create_app, db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main(verbosity=2)


# def utils_links(app):
#     @app.route("/allUser")
#     def get_all_user():
#         users = User.return_all()
#         return jsonify(users)
#
#     @app.route("/deleteAllUser")
#     def delete_users():
#         message = User.delete_all()
#         return jsonify(message)
