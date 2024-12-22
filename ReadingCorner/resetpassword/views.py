from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from ReadingCorner.decorators import jwt_required


@csrf_exempt
@jwt_required
def reset_password_view(request, uidb64, token):
    if request.method == "POST":
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user and default_token_generator.check_token(user, token):
            new_password = request.POST.get("password")
            if not new_password:
                return JsonResponse({"error": "Password is required."}, status=400)
            
            form = SetPasswordForm(user, data={"new_password1": new_password, "new_password2": new_password})
            if form.is_valid():
                form.save()
                return JsonResponse({"message": "Password has been reset successfully."}, status=200)
            else:
                return JsonResponse({"error": "Invalid password format."}, status=400)
        else:
            return JsonResponse({"error": "Invalid or expired token."}, status=400)
    return JsonResponse({"error": "Only POST method is allowed."}, status=405)