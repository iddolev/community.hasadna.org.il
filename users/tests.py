from django.db import IntegrityError, transaction
from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError


class UsersTest(TestCase):
    def test_create_user(self):
        self.assertEquals(0, User.objects.count())
        u = User.objects.create_user('foo', 'foo@gmail.com', 'secret')
        self.assertEquals(1, User.objects.count())

        self.assertRaisesRegexp(ValidationError, 'Nick', User.objects.create_user, 'Foo', 'bar@gmail.com', 'secret')

        with transaction.atomic():
            self.assertRaisesRegexp(IntegrityError, 'email', User.objects.create_user, 'bar', 'foo@gmail.com', 'secret')

        u = User.objects.create_user('bar', 'bar@gmail.com', 'secret')
        self.assertEquals(2, User.objects.count())

