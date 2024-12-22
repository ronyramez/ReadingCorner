from django.db import connection
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from datetime import datetime, timedelta
from django.conf import settings  # Assuming the JWT secret is stored in settings
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
import json
from django.http import JsonResponse


# @permission_classes([IsAuthenticated])
# @JWT_required
# @api_view(['POST'])

@csrf_exempt
def user_Login(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            Email = data.get('Email')
            Password = data.get('Password')

            # Validate required fields
            if not Email or not Password:
                return JsonResponse({"error": "Email and Password are required."}, status=400)

            # SQL query to fetch the user based on the email
            query = '''SELECT "Password", "User_id", "Email", "FirstName" FROM "Users" WHERE "Email" = %s'''
            values = (Email,)

            with connection.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()

            # Handle invalid email or password
            if result is None:
                return JsonResponse({"error": "Invalid email or password."}, status=401)

            # Retrieve the stored password, user_id, and other info
            stored_password = result[0]
            User_id = result[1]
            Email = result[2]
            FirstName = result[3]

            # Check if the provided password matches the stored password
            if check_password(Password, stored_password):
                # Password matched, generate JWT token
                payload = {
                    "user_id": User_id,
                    "email": Email,
                    "exp": datetime.utcnow() + timedelta(days=1),  # Token expiration time (1 day)
                }

                # Encode the JWT token using the secret from settings
                token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")

                # Return the token in the response
                return JsonResponse({"token": token}, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password."}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
