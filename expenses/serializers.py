from rest_framework import serializers
from expenses.models import Vendor, Employee, Expense


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "name",
            "code",
        )


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "name",
            "code",
        )


class ExpensesSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=0)
    date = serializers.DateTimeField()

    class Meta:
        model = Expense
        fields = (
            "vendor",
            "employee",
            "amount",
            "comment",
            "date",
        )


class ExpensesListSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    employee = EmployeeSerializer()
    amount = serializers.IntegerField(min_value=0)
    date = serializers.DateTimeField()

    class Meta:
        model = Expense
        fields = (
            "vendor",
            "employee",
            "amount",
            "comment",
            "date",
        )

    @staticmethod
    def get_date(self, obj):
        return obj.date.strftime("%d-b-%Y")
