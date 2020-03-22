from django.shortcuts import render
from rest_framework.generics import GenericAPIView 
from expenses.serializers import EmployeeSerializer,VendorSerializer,ExpensesSerializer,ExpensesListSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from expenses.models import *
from datetime import datetime

import json

class EmployeeView(GenericAPIView):
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        employee_code = request.query_params.get("employee_code")
        
        if not employee_code:
            return Response({'message': 'employee_code not passed.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee.objects.get(code=employee_code)
        except Employee.DoesNotExist:
            return Response({'message': 'invalid employee code passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        serialize = self.get_serializer(instance = employee)
        employee_details=serialize.data

        return Response(employee_details,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get("name")
        employee_code = data.get("employee_code")
        if not name:
            return Response({'message': 'name not passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        if not employee_code:
            return Response({'message': 'employee_code not passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data = {"name":name,"code":employee_code})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        return Response({"message": "employee created."},status=status.HTTP_201_CREATED)


class VendorView(GenericAPIView):
    serializer_class = VendorSerializer

    def get(self, request, *args, **kwargs):
        vendor_code = request.query_params.get("vendor_code")

        if not vendor_code:
            return Response({'message': 'vendor_code not passed.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            vendor = Vendor.objects.get(code=vendor_code)
        except Vendor.DoesNotExist:
            return Response({'message': 'invalid vendor code passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        serialize = self.get_serializer(instance = vendor)
        vendor_details=serialize.data

        return Response({vendor_details},status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get("name")
        vendor_code = data.get("vendor_code")
        
        if not name:
            return Response({'message': 'name not passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        if not vendor_code:
            return Response({'message': 'vendor_code not passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data = {"name":name,"code":vendor_code})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        return Response({"message": "vendor created."},status=status.HTTP_201_CREATED)
         
    
class ExpensesView(GenericAPIView):
    serializer_class = ExpensesSerializer
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        vendor_code = request.query_params.get("vendor_code")
        employee_code = request.query_params.get("employee_code")
        
        if not(vendor_code or employee_code):
            return Response({"Details": "Provide Vendor Code or Employee code"}
                            ,status=status.HTTP_400_BAD_REQUEST)
        if vendor_code:
            expenses = self.queryset.filter(vendor=vendor_code)
            if not expenses.exists():
                return Response({"Details": "Doesnot Exist"},status=status.HTTP_400_BAD_REQUEST)

        elif employee_code:
            expenses = self.queryset.filter(employee=employee_code)
            if not expenses.exists():
                return Response({"Details": "Doesnot Exist"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance=expenses, many=True)
        expenses_data = serializer.data
        
        return Response(expenses_data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        
        vendor_code = data.get("vendor_code")
        employee_code = data.get("employee_code")
        expense_comment = data.get("expense_comment")
        expense_done_on = data.get("expense_done_on")
        expense_amount = data.get("expense_amount")
        
        if not vendor_code:
            return Response({'message': 'vendor code not passed.'},status=status.HTTP_400_BAD_REQUEST)
        if not employee_code:
            return Response({'message': 'employee code not passed.'},status=status.HTTP_400_BAD_REQUEST)
        if not expense_comment:
            return Response({'message': 'expense comment not passed.'},status=status.HTTP_400_BAD_REQUEST)
        if not expense_done_on:
            return Response({'message': 'expense_done_on not passed.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            expense_done_on=datetime.strptime(expense_done_on, '%d-%b-%Y')
        except ValueError:
            return Response({'message': 'expense done on is not in valid format.'},status=status.HTTP_400_BAD_REQUEST)
        
        if not expense_amount:
            return Response( {'message': 'expense amount not passed.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            expense_amount = int(expense_amount)
        except ValueError:
            return Response({'message': 'expense amount is not in valid format.'},status=status.HTTP_400_BAD_REQUEST)
        
        seralizer_data={"vendor":vendor_code,"employee":employee_code,
                        "comment":expense_comment,"date":expense_done_on,
                        "amount":expense_amount}
        
        serializer = self.get_serializer(data=seralizer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "expense created."},status=status.HTTP_201_CREATED)


class VendorExpensesView(GenericAPIView):
    serializer_class = ExpensesListSerializer
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        vendor_code = request.query_params.get("vendor_code") 
        if not vendor_code :
            return Response({'message': 'vendor_code not passed.'}
                            ,status=status.HTTP_400_BAD_REQUEST)
        
        if vendor_code:
            expenses = self.queryset.filter(vendor=vendor_code)
            if not expenses.exists():
                return Response({'message': 'invalid vendor code passed.'},status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=expenses, many=True)
        expenses_data = serializer.data
        
        return Response(expenses_data,status=status.HTTP_200_OK)


class EmployeeExpensesView(GenericAPIView):
    serializer_class = ExpensesListSerializer
    queryset = Expense.objects.all()

    def get(request, *args, **kwargs):
        employee_code = request.query_params.get("employee_code")
        
        if not employee_code :
            return Response({'message': 'employee_code not passed.'}
                            ,status=status.HTTP_400_BAD_REQUEST)
        
        if employee_code:
            expenses = self.queryset.filter(employee=employee_code)
            if not expenses.exists():
                return Response({'message': 'invalid employee code passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance=expenses, many=True)
        expenses_data = serializer.data
        
        return Response(expenses_data,status=status.HTTP_200_OK)


class ExpensesListView(GenericAPIView):
    serializer_class = ExpensesListSerializer
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        vendor_code = request.query_params.get("vendor_code")
        employee_code = request.query_params.get("employee_code")
        
        if not vendor_code :
            return Response({'message': 'vendor_code not passed.'}
                            ,status=status.HTTP_400_BAD_REQUEST)
        
        if vendor_code:
            expenses = self.queryset.filter(vendor=vendor_code)
            if not expenses.exists():
                return Response({'message': 'invalid vendor code passed.'},status=status.HTTP_400_BAD_REQUEST)

        elif employee_code:
            expenses = self.queryset.filter(employee=employee_code)
            if not expenses.exists():
                return Response({'message': 'invalid employee code passed.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance=expenses, many=True)
        expenses_data = serializer.data
        
        return Response(expenses_data,status=status.HTTP_200_OK)

