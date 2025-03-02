from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, VerifyOTPSerializer, LoginSerializer, LoanSerializer, LoanPaymentScheduleSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from datetime import timedelta
from .models import Loan, LoanPaymentSchedule
from django.shortcuts import get_object_or_404
import math
from decimal import Decimal



User = get_user_model()

# 1️⃣ Register API
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered. OTP sent to email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2️⃣ Verify OTP API
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3️⃣ Login API
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
# Utility function to calculate loan details
def calculate_loan(amount, tenure, interest_rate):
    """
    Calculates EMI, total interest, and total payment.

    :param amount: Principal loan amount
    :param tenure: Loan tenure in months
    :param interest_rate: Annual interest rate in percentage
    :return: (emi, total_interest, total_amount)
    """
    monthly_rate = interest_rate / (12 * 100)  # Convert yearly interest to monthly decimal
    if monthly_rate == 0:  # Handling zero-interest case
        emi = amount / tenure
    else:
        emi = (amount * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)

    total_amount = emi * tenure
    total_interest = total_amount - amount

    print(f"🔍 Loan Calculation Debug: Amount={amount}, Tenure={tenure}, Interest={interest_rate}%")
    print(f"📌 Monthly EMI: {emi}, Total Interest: {total_interest}, Total Amount: {total_amount}")


    return round(emi, 2), round(total_interest, 2), round(total_amount, 2)

# 1️⃣ User: Add a Loan
class AddLoanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        amount = float(data['amount'])
        tenure = int(data['tenure'])
        interest_rate = float(data['interest_rate'])

        # Validate loan amount and tenure
        if amount < 1000 or amount > 100000:
            return Response({"error": "Amount must be between ₹1,000 and ₹100,000."}, status=400)
        if tenure < 3 or tenure > 24:
            return Response({"error": "Tenure must be between 3 and 24 months."}, status=400)

        # Calculate EMI, Total Interest, and Total Amount
        emi, total_interest, total_amount = calculate_loan(amount, tenure, interest_rate)
        print(f"🚀 After Calculation - EMI: {emi}, Total Interest: {total_interest}, Total Amount: {total_amount}")

        print(f"📝 Creating Loan Record -> EMI: {emi}, Total Interest: {total_interest}, Total Amount: {total_amount}")

        # Create Loan Record
        loan = Loan.objects.create(
            loan_id=f"LOAN{Loan.objects.count() + 1:03}",
            user=user,
            amount=amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_installment=emi,
            total_interest=total_interest,
            total_amount=total_amount,
            amount_remaining=total_amount  # ✅ Fix: Ensure this field is not NULL
        )


        # Generate Payment Schedule (Each installment every 1 month from today)
        start_date = now().date()
        payment_schedule = []
        for i in range(1, tenure + 1):
            due_date = start_date + timedelta(days=30 * i)
            payment = LoanPaymentSchedule.objects.create(
                loan=loan,
                installment_no=i,
                due_date=due_date,
                amount=emi
            )
            payment_schedule.append(LoanPaymentScheduleSerializer(payment).data)

        # Custom API Response
        response_data = {
            "status": "success",
            "data": {
                "loan_id": loan.loan_id,
                "amount": loan.amount,
                "tenure": loan.tenure,
                "interest_rate": f"{loan.interest_rate}% yearly",
                "monthly_installment": loan.monthly_installment,
                "total_interest": loan.total_interest,
                "total_amount": loan.total_amount,
                "payment_schedule": payment_schedule
            }
        }
        
        return Response(response_data)
    
# 2️⃣ User: List Loans
class ListLoansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        loans = Loan.objects.filter(user=user)
        return Response({"status": "success", "data": {"loans": LoanSerializer(loans, many=True).data}})

# 3️⃣ User: Foreclose Loan
class LoanForeclosureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        # Fetch loan and handle 404 errors
        try:
            loan = Loan.objects.get(loan_id=loan_id, user=request.user)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found or does not belong to user."}, status=404)

        # Check if loan is already closed
        if loan.status == "CLOSED":
            return Response({"error": "Loan is already closed."}, status=400)

        # Calculate foreclosure discount & final settlement amount
        foreclosure_discount = loan.total_interest * Decimal("0.05")
        final_settlement_amount = max(loan.amount_remaining - foreclosure_discount, 0)

        # Update loan details
        loan.amount_paid = loan.total_amount
        loan.amount_remaining = 0
        loan.status = "CLOSED"
        loan.save()

        # Return foreclosure details
        return Response({
            "status": "success",
            "message": "Loan foreclosed successfully.",
            "data": {
                "loan_id": loan.loan_id,
                "amount_paid": f"{loan.total_amount:.2f}",
                "foreclosure_discount": f"{foreclosure_discount:.2f}",
                "final_settlement_amount": f"{final_settlement_amount:.2f}",
                "status": "CLOSED"
            }
        }, status=200)
    
# 4️⃣ Admin: View All Loans
class AdminAllLoansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if getattr(request.user, 'role', None) != "admin":
            return Response({"error": "Unauthorized access"}, status=403)

        loans = Loan.objects.all()  # Fetch all loans
        loan_data = [
            {
                "loan_id": loan.loan_id,
                "amount": loan.amount,
                "tenure": loan.tenure,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "total_interest": loan.total_interest,
                "total_amount": loan.total_amount
            }
            for loan in loans
        ]

        return Response({
            "status": "success",
            "data": {"loans": loan_data}
        })

class AdminUserLoanDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if getattr(request.user, 'role', None) != "admin":
            return Response({"error": "Unauthorized access"}, status=403)

        loans = Loan.objects.select_related('user').all()  # Fetch loans + user data
        loan_data = [
            {
                "loan_id": loan.loan_id,
                "amount": loan.amount,
                "tenure": loan.tenure,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "total_interest": loan.total_interest,
                "total_amount": loan.total_amount,
                "user": {
                    "id": loan.user.id,
                    "name": loan.user.username,
                    "email": loan.user.email
                }
            }
            for loan in loans
        ]

        return Response({
            "status": "success",
            "data": {"loans": loan_data}
        })


# 5️⃣ Admin: Delete Loan
class DeleteLoanView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, loan_id):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized access"}, status=403)

        loan = get_object_or_404(Loan, loan_id=loan_id)
        loan.delete()
        return Response({"message": "Loan deleted successfully."}, status=200)