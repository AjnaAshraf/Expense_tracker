from django.urls import path

from spending.views import SignUpView,GetMeView,ExpenseCreateListView,ExpenseRetrieveUpdateDelete,ExpenseSummaryView,BudgetPlanView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[

    path("register/",SignUpView.as_view()),
    path("me/",GetMeView.as_view()),
    path("expenses/",ExpenseCreateListView.as_view()),
    path("expenses/<int:pk>/",ExpenseRetrieveUpdateDelete.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    path('expenses/summary/',ExpenseSummaryView.as_view()),
    path('budget_plan/',BudgetPlanView.as_view()),

]