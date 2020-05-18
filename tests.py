from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Credential
from config import Config

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

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_Credentials(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

        # create 3 credentials
        now = datetime.utcnow()
        c1 = Credential(username='u1@gmail.com', password='test123', comments='c1',  user_id=u1.id,
                  established=now + timedelta(seconds=1))
        c2 = Credential(username='u2@gmail.com', password='test456', comments='c2',  user_id=u2.id,
                  established=now + timedelta(seconds=2))
        c3 = Credential(username='u3@gmail.com', password='test789', comments='c3',  user_id=u3.id,
                  established=now + timedelta(seconds=3))
        c4 = Credential(username='u4@gmail.com', password='test012', comments='c4',  user_id=u4.id,
                  established=now + timedelta(seconds=4))
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity=2)