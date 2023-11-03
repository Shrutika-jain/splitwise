from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from users.models import User, SplitAmoungUsers
from .utils import split_bill, passbook_data
from .serilizers import SplitBillSerializer
from django.db.models import Q

# Create your views here.

# API for spliting bill among the users
class SplitBillApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SplitBillSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # print("line no 20")
        if serializer.is_valid(raise_exception=True):
            print("serilizers are valid")
            try:
                amount_paid_by = User.objects.get(userid=serializer.validated_data["amount_paid_by"])
            except User.DoesNotExist:
                return Response({"message": "Amount paid by user does not exists.", "success": False}, status=status.HTTP_404_NOT_FOUND)
            total_amount = serializer.validated_data["total_amount"]
            split_type = serializer.validated_data["split_type"]
            split_to = serializer.validated_data["split_to"]
            if split_type == "EQUAL":
                amount = total_amount / len(split_to)

                for user in split_to:
                    if user["userid"] != amount_paid_by.userid:
                        owe_by = User.objects.filter(userid=user["userid"]).first()
                        result = split_bill(amount_paid_by=amount_paid_by, owe_by=owe_by, amount=amount)

            if split_type == "EXACT":

                for user in split_to:
                    if user["userid"] != amount_paid_by.userid:
                        owe_by = User.objects.filter(userid=user["userid"]).first()
                        result = split_bill(amount_paid_by=amount_paid_by, owe_by=owe_by, amount=user["amount"])

            if split_type == "PERCENT":

                for user in split_to:
                    if user["userid"] != amount_paid_by.userid:
                        # print("line no 47")
                        amount = float(user["percent"] * total_amount) * (1 / 100)
                        # print("line number 49")
                        owe_by = User.objects.filter(userid=user["userid"]).first()
                        result = split_bill(amount_paid_by=amount_paid_by, owe_by=owe_by, amount=amount)

            if result:
                return Response({"message": "Expense splited successfully.", "success": True}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)
    

class UserPassbookView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, userid):
        print("userid", userid)
        try:
            user = User.objects.get(userid=userid)
        except User.DoesNotExist:
            return Response({"message": "Userid does not exists.", "success": False}, status=status.HTTP_404_NOT_FOUND)
        
        response = passbook_data(user)
            
        return Response(response, status=status.HTTP_200_OK)
