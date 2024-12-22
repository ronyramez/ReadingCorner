from django.shortcuts import render
from django.db import connection  # To execute raw SQL queries
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required  # To ensure the user is authenticated
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt

# @login_required(login_url='login')
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

@csrf_exempt
@jwt_required
def add_to_favorites(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    if not book_id:
        return JsonResponse({'error': 'Book ID is required'}, status=400)

    user_id = request.user["id"]
    if not user_id:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    # Check if the record already exists
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM "Favorites" 
                WHERE "User_id" = %s AND "Book_id" = %s
            """, [user_id, book_id])
            count = cursor.fetchone()[0]

            if count > 0:
                return JsonResponse({'error': 'Book is already in favorites'}, status=400)

            # Insert the new favorite
            cursor.execute("""
                INSERT INTO "Favorites" ("User_id", "Book_id")
                VALUES (%s, %s)
            """, [user_id, book_id])
            return JsonResponse({'message': 'Book added to favorites'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@jwt_required
def remove_from_favorites(request):
    # Ensure the request method is DELETE
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method. Use DELETE.'}, status=405)

    # Parse the JSON payload
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    # Check for missing required fields
    if not book_id:
        return JsonResponse({'error': 'Book ID is required'}, status=400)

    # Retrieve user ID from the JWT token
    user_id = request.user["id"]
    if not user_id:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    # Execute the SQL query to delete the record
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                DELETE FROM "Favorites"
                WHERE "User_id" = %s AND "Book_id" = %s
            """, [user_id, book_id])
            return JsonResponse({'message': 'Book removed from favorites'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
@jwt_required
def list_favorites(request): 
    # user_id = getattr(request, 'user_id', None)  # Extract user_id from request
    
    user_id = request.user["id"]
    if not user_id:
        return JsonResponse({'error': 'Invalid user'}, status=400)
    
    # Execute the SQL query to fetch records for the specific user
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT 
                    b."Author", 
                    b."Language", 
                    b."ISBN", 
                    b."Description", 
                    b."Book_name", 
                    b."Category", 
                    b."Publisher", 
                    b."Publishing_number", 
                    b."Publishing_year"
                FROM "Favorites" f
                INNER JOIN "Books" b ON f."Book_id" = b."Book_id"
                WHERE "User_id" = %s
            """, [user_id])
            results = cursor.fetchall()

            # Format the results as a list of dictionaries
            favorites = [
                {
                    "author": row[0],
                    "language": row[1],
                    "isbn": row[2],
                    "description": row[3],
                    "book_name": row[4],
                    "category": row[5],
                    "publisher": row[6],
                    "publishing_number": row[7],
                    "publishing_year": row[8],
                }
                for row in results
            ]
            return JsonResponse({'favorites': favorites}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)