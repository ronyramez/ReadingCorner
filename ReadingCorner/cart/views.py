from django.shortcuts import render
from django.db import connection  # To execute raw SQL queries
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required  # To ensure the user is authenticated
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt
import json

# Add to Cart Function
@csrf_exempt
@jwt_required
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        quantity = data.get('quantity', 1)  # Default quantity to 1 if not provided
        total_price = data.get('total_price')  # Total price should be provided
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    if not book_id or not total_price:
        return JsonResponse({'error': 'Book ID and Total price are required'}, status=400)

    user_id = request.user["id"]
    if not user_id:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    # Check if the book is already in the cart
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM "Cart" 
                WHERE "User_id" = %s AND "Book_id" = %s
            """, [user_id, book_id])
            count = cursor.fetchone()[0]

            if count > 0:
                # Update quantity if the book already exists in the cart
                cursor.execute("""
                    UPDATE "Cart" 
                    SET "Quantity" = "Quantity" + %s, "Total_price" = "Total_price" + %s
                    WHERE "User_id" = %s AND "Book_id" = %s
                """, [quantity, total_price, user_id, book_id])
                return JsonResponse({'message': 'Book quantity updated in the cart'}, status=200)

            # Insert the new cart item if it doesn't exist
            cursor.execute("""
                INSERT INTO "Cart" ("User_id", "Book_id", "Quantity", "Total_price")
                VALUES (%s, %s, %s, %s)
            """, [user_id, book_id, quantity, total_price])
            return JsonResponse({'message': 'Book added to cart'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Remove from Cart Function
@csrf_exempt
@jwt_required
def remove_from_cart(request):
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
                DELETE FROM "Cart"
                WHERE "User_id" = %s AND "Book_id" = %s
            """, [user_id, book_id])
            return JsonResponse({'message': 'Book removed from cart'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# List Cart Function
@csrf_exempt
@jwt_required
def list_cart(request): 
    user_id = request.user["id"]
    if not user_id:
        return JsonResponse({'error': 'Invalid user'}, status=400)
    
    # Execute the SQL query to fetch cart contents for the specific user
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
                    b."Publishing_year", 
                    c."Quantity", 
                    c."Total_price"
                FROM "Cart" c
                INNER JOIN "Books" b ON c."Book_id" = b."Book_id"
                WHERE c."User_id" = %s
            """, [user_id])
            results = cursor.fetchall()

            # Format the results as a list of dictionaries
            cart_items = [
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
                    "quantity": row[9],
                    "total_price": row[10],
                }
                for row in results
            ]
            return JsonResponse({'cart_items': cart_items}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
