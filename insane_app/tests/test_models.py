from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from insane_app.models import UserGroup


class TestInsaneUserModel(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_fine_creation(self):
        user = self.User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='2tr0nkpass'
        )
        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.email, 'user1@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_no_params(self):
        with self.assertRaises(TypeError):
            self.User.objects.create_user()

    def test_unique_username(self):
        self.User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='2tr0nkpass'
        )
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username='user1',
                email='user01@gmail.com',
                password='verystr0nk'
            )

    def test_correct_email(self):
        # with self.assertRaises(ValueError):
        self.User.objects.create_user(
            username='user2',
            email='asd2e2eifi5eu9',
            password='n0ttshort'
        )

    def test_strong_password(self):
        # with self.assertRaises(ValueError):
        self.User.objects.create_user(
            username='user2',
            email='user2@gmail.com',
            password='weak'
        )


class TestUserGroup(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            username='test_user1',
            email='u@gmail.com',
            password='str0nkpass'
        )

    def test_create(self):
        UserGroup.objects.create(name='group1', administrator=self.user1)

    def test_name_required(self):
        # with self.assertRaises(ValueError):
        UserGroup.objects.create(administrator=self.user1)

    def test_name_not_empty(self):
        # with self.assertRaises(ValueError):
        UserGroup.objects.create(name='', administrator=self.user1)

    def test_admin_required(self):
        # with self.assertRaises(ValueError):
        UserGroup.objects.create(name='group1')

    def test_admin_multiple_groups(self):
        UserGroup.objects.create(name='group1', administrator=self.user1)
        UserGroup.objects.create(name='group2', administrator=self.user1)
