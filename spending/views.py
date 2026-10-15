from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User

# from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from spending.models import Expense
from spending.serializers import UserSerializer,ExpenseSerializer

from spending.ai_service import get_budget_plan
from spending.permissions import IsOwner
from datetime import datetime
from django.db.models import Sum
# Create your views here.

class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serilaizer_instance = UserSerializer(data=form_data)

        if serilaizer_instance.is_valid():

            cleaned_data = serilaizer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serilaizer_instance = UserSerializer(instance)

            return Response(data=serilaizer_instance.data)

        else:

            return Response(data=serilaizer_instance.errors)

class GetMeView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username = auth_user)

        serializer_instance = UserSerializer(instance)

        return Response(data = serializer_instance.data)

class ExpenseCreateListView(APIView):

    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    # permission_classes=[IsOwner]

    def get(self,request):

        instance = Expense.objects.filter(owner=request.user)

        serializer_instance = ExpenseSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = ExpenseSerializer(data = form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class ExpenseRetrieveUpdateDelete(APIView):

    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    # permission_classes=[permissions.IsAuthenticated]

    permission_classes=[IsOwner]

    def get(self,request,pk=None):

        # instance = Expense.objects.get(id=pk)

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = ExpenseSerializer(instance)

        return Response(data= serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = ExpenseSerializer(data = form_data,instance = instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"Expense deleted "})


class ExpenseSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes =[permissions.IsAuthenticated]

    def get(self,request):

        response_data = {

            "todays_total": 0
        }

        cur_date = datetime.now().date()

        cur_month = datetime.now().month

        cur_year = datetime.now().year

        todays_transaction = Expense.objects.filter(owner=request.user,created_at__date=cur_date)
        
        #monthly transaction
        monthly_transactions = Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transactions:

            monthly_total = monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            monthly_category_sum = monthly_transactions.values("category").annotate(total=Sum("amount"))

            response_data["monthly_total"]=monthly_total

            response_data["monthly_category_sum"]=monthly_category_sum


        if todays_transaction:

            todays_total = todays_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            category_sum = todays_transaction.values("category").annotate(total=Sum("amount"))

            response_data["todays_total"]=todays_total

            response_data["category_sum"]=category_sum

        return Response(data=response_data)


class BudgetPlanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data = {"monthly_total":0}

        cur_month = datetime.now().month

        cur_year=datetime.now().year

        monthly_trasaction  = Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_trasaction:

            monthly_total = monthly_trasaction.values("amount").aggregate(total = Sum("amount")).get("total")

            monthly_category_sum = monthly_trasaction.values("category").annotate(total=Sum("amount"))

            response_data["monthly_total"] = monthly_total

            response_data["category_summary"] = monthly_category_sum

            budget_plan = get_budget_plan(response_data)

            response_data["plan"] = budget_plan


        return Response(data=response_data)



    

        






