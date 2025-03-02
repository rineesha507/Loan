# Loan Management System

A **Django-based Loan Management System** with **role-based authentication**, **OTP verification**, and **automated loan interest calculations**.

---

## 🚀 Features

✅ **User Registration & OTP Verification** (via email using SMTP) ✅ **JWT Authentication** (for Users & Admins) ✅ **Role-Based Access**:

- **Users**: Add loans, view loans, and foreclose loans.
- **Admins**: View all loans, access user loan details, and delete loan records. ✅ **Loan Management**: Loan addition, listing, foreclosure, and admin controls. ✅ **Database**: PostgreSQL (**MongoDB optional**) ✅ **Deployment**: Hosted on **Render**

---

## 📌 Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Token)
- **Email (OTP Verification)**: SMTP via Gmail
- **Database**: PostgreSQL
- **Deployment**: Render

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/rineesha507/Loan.git
cd Loan
```

### 2️⃣ Create a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Database (PostgreSQL)

Edit **settings.py** and update the database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5️⃣ Apply Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Configure Email (SMTP - Gmail)

Update **settings.py** with Gmail SMTP credentials:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not your real password
```

🔹 **For Gmail**: Enable "Less Secure Apps" or create an **App Password** [here](https://myaccount.google.com/apppasswords).

### 7️⃣ Run the Server

```sh
python manage.py runserver
```

---

## 📡 API Endpoints

### 🔹 Authentication & User Management

```sh
# User Registration (OTP sent)
POST /api/register/

# Verify OTP
POST /api/verify-otp/

# Login (JWT authentication)
POST /api/login/

# Obtain access & refresh tokens
POST /api/token/

# Refresh access token
POST /api/token/refresh/
```

### 🔹 Loan Management (Users)

```sh
# Add a new loan
POST /api/loans/

# View user-specific loans
GET /api/loans/list/

# Foreclose a loan
POST /api/loans/<loan_id>/foreclose/
```

### 🔹 Admin Controls

```sh
# View all loans
GET /api/admin/loans/all/

# View details of a user's loan
GET /api/admin/loans/user-details/

# Delete a loan record
DELETE /api/admin/loans/<loan_id>/delete/
```

---

## 🔑 Authentication & JWT

- After logging in, you'll receive an **access token** and a **refresh token**.
- Use the **access token** in the Authorization header for secured endpoints:

```sh
Authorization: Bearer your_access_token
```

- When the **access token** expires, refresh it using `/api/token/refresh/`.

---

## 📤 Deployment (Render)

1. Push your code to **GitHub**.
2. Create a **Render** account and add a new **Django Web Service**.
3. Set environment variables for PostgreSQL and email credentials.
4. Deploy and start using the system! 🎉

---

## 📌 Future Enhancements

✅ Add **Loan Interest Rate Customization** ✅ Improve **User Dashboard UI** ✅ Implement **Loan Payment History Tracking** ✅ Add **Automated Loan Approval Process**



