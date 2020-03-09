from django.db import models


class Auto(models.Model):
    year = models.IntegerField()
    color = models.CharField(max_length=128)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    general_rent_time = models.DateTimeField()


class Brand(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    country = models.CharField(max_length=128)


class Customer(models.Model):
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True, default="")
    dateOfBirth = models.DateTimeField()
    auto = models.ManyToManyField(Auto)
    rent_time = models.DateTimeField()

