from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Loan, LoanPaymentSchedule



User = get_user_model()

# 1️⃣ User Registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_verified=False)
        user.generate_otp()

        # Send OTP via Email
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {user.otp}',
            'pythondjango293@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user

# 2️⃣ OTP Verification
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_verified = True  # Mark as verified
                user.otp = None  # Remove OTP after successful verification
                user.save()
                return {'message': 'OTP verified successfully. You can now log in.'}
            else:
                raise serializers.ValidationError("Invalid OTP.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")


# 3️⃣ Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                raise serializers.ValidationError("Account not verified. Please verify OTP first.")

            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

            # Generate JWT Token
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
            }
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")




class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["loan_id", "amount", "tenure", "interest_rate", "monthly_installment", "total_interest", "total_amount"]

class LoanPaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPaymentSchedule
        fields = ['installment_no', 'due_date', 'amount']
