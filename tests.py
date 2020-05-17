from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Credential

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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

        # create four posts
        now = datetime.utcnow()
        c1 = Credential(Credential='u1@google.com', password='test123', comments='test1', owner=u1,
                  established=now + timedelta(seconds=1))
        c2 = Credential(Credential='u2@google.com', password='test456', comments='test2', owner=u2,
                  established=now + timedelta(seconds=1))
        c3 = Credential(Credential='u3@google.com', password='test789', comments='test3', owner=u3,
                  established=now + timedelta(seconds=1))
        db.session.add_all([c1, c2, c3])
        db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity=2)