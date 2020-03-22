from django.urls import path
from expenses.views import (
    EmployeeView,
    VendorView,
    ExpensesView,
    ExpensesListView,
    VendorExpensesView,
    EmployeeExpensesView,
)

urlpatterns = [
    path("employee/", EmployeeView.as_view()),
    path("vendor/", VendorView.as_view()),
    path("expenses/", ExpensesView.as_view()),
    path("expenses-list/", ExpensesListView.as_view()),
    #    according to the test scripts
    path("add-employee/", EmployeeView.as_view()),
    path("get-employee/", EmployeeView.as_view()),
    path("add-vendor/", VendorView.as_view()),
    path("get-vendor/", VendorView.as_view()),
    path("add-expense/", ExpensesView.as_view()),
    path("get-expense-for-vendor/", VendorExpensesView.as_view()),
    path("get-expense-for-employee/", EmployeeExpensesView.as_view()),
]
