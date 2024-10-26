from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)



class Category(models.Model):
    name = models.CharField(max_length=100)


class Agency(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class User(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post = models.CharField(max_length=100)

class Feedback(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    AGENCY = models.ForeignKey(Agency, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

class Complaints(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    date = models.CharField(max_length=100)


class Scrap(models.Model):
    AGENCY = models.ForeignKey(Agency, on_delete=models.CASCADE)
    CATEGORY = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=1000)


class Request(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    SCRAP = models.ForeignKey(Scrap, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    qty = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    # description = models.CharField(max_length=100)
