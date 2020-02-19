from django.db import models
from django.contrib.auth.models import AbstractUser


class SanityRank(models.Model):
    name = models.CharField(unique=True, max_length=20)
    sanity_cap = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class InsaneUser(AbstractUser):
    sanity = models.PositiveIntegerField(default=0)
    rank = models.ForeignKey(SanityRank, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['username']
        db_table = 'insane_user'

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    name = models.CharField(max_length=32)
    administrator = models.ForeignKey(
        InsaneUser,
        related_name='admined_group',
        on_delete=models.SET_NULL,
        null=True
    )
    members = models.ManyToManyField(
        InsaneUser,
        related_name='user_group',
        through='Membership',
        through_fields = ('user_group', 'user')
    )
    dt_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(InsaneUser, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'user_group'),)


class Story(models.Model):
    name = models.CharField(max_length=64)
    body = models.TextField(max_length=600)
    like_count = models.PositiveIntegerField()
    dt_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        InsaneUser,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class StoryImage(models.Model):
    src = models.CharField(max_length=128)
    product = models.ForeignKey(
        Story,
        related_name='image',
        on_delete=models.CASCADE
    )


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    story = models.ForeignKey(
        Story,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    dt_created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    src = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
