from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, null=True)
    age = models.IntegerField()
    auto = models.ForeignKey("Auto", on_delete=models.SET_NULL, blank=True, null=True)
    rent_time = models.DateTimeField()


class Auto(models.Model):
    year = models.IntegerField()
    color = models.CharField(max_length=128)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    general_rent_time = models.DateTimeField()


class Brand(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
