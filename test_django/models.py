from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django import forms


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

''''''
class Department(models.Model):
    address = models.TextField(verbose_name="Address", help_text="Enter an address",
                               null=False, blank=False)
    workload = IntegerRangeField(max_value=10, min_value=0, verbose_name="Workload(0 - none, 10 - full)",
                                 help_text="Choose an workload", null=False, blank=False)
    rating = IntegerRangeField(max_value=10, min_value=0, verbose_name="Rating(0 - puke, 10 - super)",
                               help_text="Choose a rating", null=False, blank=False)

    def __str__(self):
        return "Department address: " + self.address

    class Meta:
        db_table = "Department"


class Mechanic(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name", help_text="Enter a first name",
                                  null=False, blank=False)
    surname = models.CharField(max_length=50, verbose_name="Surname", help_text="Enter a surname",
                               null=False, blank=False)
    experience = IntegerRangeField(max_value=100, min_value=0, verbose_name="Experience",
                                   help_text="Choose an experience", null=False, blank=False)
    rating = IntegerRangeField(max_value=10, min_value=0, verbose_name="Rating(0 - puke, 10 - super)",
                               help_text="Choose a rating", null=False, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Department",
                                   help_text="Choose a department", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Id User", help_text="Choose an id user",
                                null=True, blank=True)

    def __str__(self):
        return "Mechanic: " + self.surname + " " + self.first_name + ". Rating: " + str(self.rating) + ". " \
               + self.department.__str__()

    class Meta:
        db_table = "Mechanic"


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name", help_text="Enter a first name",
                                  null=False, blank=False)
    surname = models.CharField(max_length=50, verbose_name="Surname", help_text="Enter a surname",
                               null=False, blank=False)
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number", help_text="Enter a phone number",
                                    null=False, blank=False)
    city = models.CharField(max_length=50, verbose_name="City", help_text="Enter a city",
                            null=False, blank=False, default="Moscow")
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Id User", help_text="Choose an id user",
                                null=True, blank=True)

    def __str__(self):
        return "Client: " + self.surname + " " + self.first_name

    class Meta:
        db_table = "Client"


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name="Message title", help_text="Enter a message title",
                                  null=False, blank=False)
    body = models.CharField(max_length=150, verbose_name="Message body", help_text="Enter a message body",
                                  null=False, blank=False)
    isAccepted = models.BooleanField(default=False, null=False, blank=False)
    main_mech = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return "Message: " + self.title

    class Meta:
        db_table = "Message"



class Car(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name", help_text="Enter a name",
                            null=False, blank=False)
    mileage = models.IntegerField(verbose_name="Mileage", help_text="Enter a mileage",
                                  null=False, blank=False)
    malfunction = models.TextField(verbose_name="Malfunction", help_text="Enter a malfunction",
                                   null=False, blank=False)
    mechanics = models.ManyToManyField(Mechanic, verbose_name="Mechanic(s)",
                                        help_text="Choose a mechanic(s)", null=True, blank=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Message",
                                        help_text="Choose a message", null=True, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client",
                               help_text="Choose a client", null=False, blank=False)
    repairIsDone = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return "Car: " + self.name

    class Meta:
        db_table = "Car"


#something like supertool
# Create your models here.
