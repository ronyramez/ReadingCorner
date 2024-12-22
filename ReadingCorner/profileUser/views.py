from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt

# user = get_user_model()



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @login_required(login_url='login')

@csrf_exempt
@jwt_required
def profileUser(request):
    if request.method == 'GET':
        # Get the user_id from the JWT token
        user_id = request.user["id"]

        # Raw SQL Query to fetch user details
        query = '''
            SELECT "FirstName", "LastName", "Email"
            FROM "Users"
            WHERE "User_id" = %s
        '''

        # Execute the query and fetch the result
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, [user_id])
                result = cursor.fetchone()
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        # Return the result as JSON
        if result:
            data = {
                "FirstName": result[0],
                "LastName": result[1],
                "Email": result[2],
            }
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"error": "User not found."}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method. Use GET."}, status=405)







# from django.contrib.auth.decorators import login_required

# @login_required
# def UserProfile(request):
#     user = request.user
#     return JsonResponse({
#         "email": user.Email,
#         "first_name": user.FirstName,
#         "last_name": user.LastName,
#     })
