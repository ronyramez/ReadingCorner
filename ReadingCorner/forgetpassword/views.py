from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.db import connection
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
import json
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@jwt_required
def forget_password_view(request):
    if request.method == "POST":
        try:
            # Parse JSON from the request body
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required."}, status=400)

            # Check if the email exists in the database
            with connection.cursor() as cursor:
                cursor.execute('SELECT "User_id" FROM "Users" WHERE "Email" = %s', [email])
                user = cursor.fetchone()

            if user:
                # User_id = user[0]  # Extract User_id from the tuple
                # token_generator = PasswordResetTokenGenerator()
                # uidb64 = urlsafe_base64_encode(force_bytes(User_id))
                # token = token_generator.make_token(User_id)  # Use User_id here directly

                # Send password reset email
                reset_link = f"http://example.com/reset-password/"
                send_mail(
                    "Password Reset Request",
                    f"Click the link below to reset your password:\n\n{reset_link}",
                    "admin@yourapp.com",
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({"message": "An email has been sent."}, status=200)

            else:
                return JsonResponse({"error": "Email does not exist."}, status=404)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
