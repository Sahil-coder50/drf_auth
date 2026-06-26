# auth-drf

A Django REST Framework package that provides JWT Authentication and Role-Based Access Control (RBAC).

---

# Features

* JWT Authentication
* User Registration
* User Login
* User Logout
* Refresh Token Rotation
* Role-Based Access Control (RBAC)
* Role CRUD APIs
* Django Permission Integration

---

# Requirements

* Python 3.12+
* Django 5.x / 6.x
* Django REST Framework
* djangorestframework-simplejwt

---

# Installation

## Install from PyPI

```bash
pip install auth-drf
```


---

# Project Setup

## Step 1: Add the package to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...

    "rest_framework",
    "auth_drf",
]
```

---

## Step 2: Create a Custom User Model

```python
from auth_drf.models.user_model import BaseUser

class Customer(BaseUser):
    class Meta:
        abstract = False
```

> **Note**
>
> `Customer` is only an example. Your custom user model can have any name.

---

## Step 3: Configure `AUTH_USER_MODEL`

```python
AUTH_USER_MODEL = "user_test.Customer"
```

---

## Step 4: Configure DRF Authentication

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
```

---

## Step 5: Include Package URLs

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auth_drf.urls")),
]
```

---

## Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Authentication

After login, use the Access Token for all protected endpoints.

```http
Authorization: Bearer <access_token>
```

---

# API Endpoints

| Method | Endpoint               |
| ------ | ---------------------- |
| POST   | `/auth/register/`      |
| POST   | `/auth/login/`         |
| POST   | `/auth/logout/`        |
| POST   | `/auth/token_refresh/` |
| POST   | `/roles/`              |
| PATCH  | `/roles/<id>/`         |
| GET    | `/roles/`              |
| GET    | `/roles/<id>/`         |

---

# Authentication APIs

## Register User

### Endpoint

```http
POST /auth/register/
```

### Request Payload

```json
{
    "first_name": "Vinnie",
    "last_name": "Sheoran",
    "email": "vinnie@yopmail.com",
    "username": "vinnie",
    "password": "vinnie"
}
```

### Response

```json
{
    "success": "Registration Successful",
    "detail": {
        "user": "vinnie@yopmail.com"
    }
}
```

---

## Login User

### Endpoint

```http
POST /auth/login/
```

### Request Payload

```json
{
    "email": "vinnie@yopmail.com",
    "username": "vinnie",
    "password": "vinnie"
}
```

### Response

```json
{
    "id": 1,
    "email": "vinnie@yopmail.com",
    "username": "vinnie",
    "permissions": [
        {
            "module": "customer",
            "actions": [
                "add_customer",
                "change_customer",
                "delete_customer",
                "view_customer"
            ]
        }
    ],
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

---

## Logout User

### Endpoint

```http
POST /auth/logout/
```

### Request Payload

```json
{
    "refresh": "<refresh_token>"
}
```

### Response

```json
{
    "success": "Logout Successful"
}
```

---

## Refresh Token

### Endpoint

```http
POST /auth/token_refresh/
```

### Request Payload

```json
{
    "refresh": "<refresh_token>"
}
```

### Response

```json
{
    "access": "<new_access_token>",
    "refresh": "<new_refresh_token>"
}
```

---

# Role APIs

## Create Role

### Endpoint

```http
POST /roles/
```

### Authentication

Requires a valid Access Token.

### Request Payload

```json
{
    "name": "Interns",
    "permissions": [
        {
            "module": "customer",
            "actions": [
                "add_customer",
                "change_customer",
                "delete_customer",
                "view_customer"
            ]
        }
    ]
}
```

### Response

```json
{
    "id": 5,
    "name": "Interns",
    "permissions": [
        {
            "module": "customer",
            "actions": [
                "add_customer",
                "change_customer",
                "delete_customer",
                "view_customer"
            ]
        }
    ]
}
```

---

## Update Role

### Endpoint

```http
PATCH /roles/<id>/
```

### Authentication

Requires a valid Access Token.

### Request Payload

```json
{
    "name": "Manager",
    "permissions": [
        {
            "module": "customer",
            "actions": [
                "add_customer",
                "change_customer",
                "delete_customer",
                "view_customer"
            ]
        }
    ]
}
```

### Response

```json
{
    "success": "Role is Updated",
    "data": {
        "id": 3,
        "name": "Manager",
        "permissions": [
            {
                "module": "customer",
                "actions": [
                    "add_customer",
                    "change_customer",
                    "delete_customer",
                    "view_customer"
                ]
            }
        ]
    }
}
```

---

## List Roles

### Endpoint

```http
GET /roles/
```

### Authentication

Requires a valid Access Token.

### Response

```json
[
    {
        "id": 2,
        "name": "Administrator",
        "permissions": [
            {
                "module": "customer",
                "actions": [
                    "add_customer",
                    "change_customer",
                    "delete_customer",
                    "view_customer"
                ]
            }
        ]
    },
    {
        "id": 3,
        "name": "Manager",
        "permissions": [
            {
                "module": "customer",
                "actions": [
                    "add_customer",
                    "change_customer",
                    "delete_customer",
                    "view_customer"
                ]
            }
        ]
    }
]
```

---

## Retrieve Role

### Endpoint

```http
GET /roles/<id>/
```

### Authentication

Requires a valid Access Token.

### Response

```json
{
    "name": "Manager",
    "permissions": [
        {
            "module": "customer",
            "actions": [
                "add_customer",
                "change_customer",
                "delete_customer",
                "view_customer"
            ]
        }
    ]
}
```

---

# License

This project is licensed under the MIT License.
