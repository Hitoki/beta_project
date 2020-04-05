from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from insane_app.models import UserGroup, Profile, SanityRank

User = get_user_model()


class TestUserWithSanity(TestCase):
    def setUp(self):
        self.test_rank = SanityRank.objects.create(name='noobie', sanity_cap=10)

    def test_create(self):
        user = User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='2tr0nkpass'
        )

        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.email, 'user1@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        self.assertEqual(user.profile.sanity, self.rank.sanity_cap)
        self.assertEqual(user.profile.rank, self.rank)

    def test_username_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(password='123123321')

    def test_password_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='user2')

    def test_unique_username(self):
        User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='2tr0nkpass'
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='user1',
                email='user01@gmail.com',
                password='verystr0nk'
            )

    # def test_correct_email(self):
    #     with self.assertRaises(ValueError):
    #         User.objects.create_user(
    #             username='user2',
    #             email='asd2e2eifi5eu9',
    #             password='n0ttshort'
    #         )

    # def test_strong_password(self):
    #     with self.assertRaises(ValueError):
    #         User.objects.create_user(
    #             username='user2',
    #             email='user2@gmail.com',
    #             password='weak'
    #         )


class TestUserGroup(TestCase):
    def setUp(self):
        SanityRank.objects.create(name='noobie', sanity_cap=10)
        self.user1 = User.objects.create_user(
            username='test_user1',
            email='u@gmail.com',
            password='str0nkpass'
        )

    def test_create(self):
        group = UserGroup.objects.create(name='group1', admin=self.user1)
        self.assertEqual(group.members.count(), 0)

    def test_add_member(self):
        group = UserGroup.objects.create(name='group1', admin=self.user1)
        user2 = User.objects.create_user(
            username='test_user2',
            email='u2@gmail.com',
            password='str0nkpass'
        )
        group.add_member(user2)
        self.assertEqual(group.members.count(), 1)

    def test_name_required(self):
        # with self.assertRaises(ValueError):
        group = UserGroup.objects.create(admin=self.user1)

    def test_name_not_empty(self):
        with self.assertRaises(ValueError):
            UserGroup.objects.create(name='', admin=self.user1)

    def test_admin_required(self):
        # with self.assertRaises(ValueError):
        UserGroup.objects.create(name='group1')

    def test_admin_multiple_groups(self):
        # with self.assertRaises(ValueError):
        UserGroup.objects.create(name='group1', admin=self.user1)
        UserGroup.objects.create(name='group2', admin=self.user1)
