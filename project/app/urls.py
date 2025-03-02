from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, AddLoanView, ListLoansView, LoanForeclosureView, DeleteLoanView, AdminUserLoanDetailsView, AdminAllLoansView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
       
        path('', RegisterView.as_view(), name='register'),
        path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
        path('login/', LoginView.as_view(), name='login'),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('loans/', AddLoanView.as_view(), name='add-loan'),
        path('loans/list/', ListLoansView.as_view(), name='list-loans'),
        path('loans/<str:loan_id>/foreclose/', LoanForeclosureView.as_view(), name='foreclose-loan'),
       path('api/admin/loans/all/', AdminAllLoansView.as_view(), name='admin-all-loans'),
       path('api/admin/loans/user-details/', AdminUserLoanDetailsView.as_view(), name='admin-user-loan-details'),       
       path('api/admin/loans/<str:loan_id>/delete/', DeleteLoanView.as_view(), name='delete-loan'),
        
        

]
