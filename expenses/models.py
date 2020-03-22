from django.db import models
from employee_vendor import settings

class Vendor(models.Model):
    name = models.CharField(max_length=20,null=False)
    code = models.TextField(null=False,primary_key=True)

class Employee(models.Model):
    code = models.TextField(null=False, primary_key=True)
    name = models.CharField(max_length=30,null=False)

class Expense(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=False,
                                related_name="expenses")
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=False,
                                related_name="expenses")
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=False)
