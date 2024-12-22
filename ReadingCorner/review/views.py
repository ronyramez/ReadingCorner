from django.shortcuts import render
from django.db import connection  # To execute raw SQL queries
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ReadingCorner.decorators import jwt_required
import json
from datetime import datetime


@csrf_exempt
@jwt_required
def add_review(request):
    try:
        data = json.loads(request.body)
        book_name = data.get('book_name')
        review_text = data.get('review_text')
        rating = data.get('rating')
        
        user_id = request.user["id"]
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    # Validate required fields
    if not book_name or not review_text or not rating or not user_id:
        return JsonResponse({'error': 'Book name, review text, user id, and rating are required'}, status=400)

    # Ensure the rating is valid (e.g., between 1 and 5)
    if not (1 <= rating <= 10):
        return JsonResponse({'error': 'Rating must be between 1 and 10'}, status=400)
    try:
        # Ensure the rating is an integer between 1 and 5
        rating = int(rating)
        if rating < 1 or rating > 10:
            raise ValueError("Rating must be between 1 and 10")
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    review_date = datetime.now().strftime('%Y-%m-%d')

    # Execute SQL query to insert a new review
    try:
        # Check if the book exists in the Books table
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM "Books" WHERE "Book_name" = %s LIMIT 1;
            """, [book_name])
            book_exists = cursor.fetchone()

        if not book_exists:
            return JsonResponse({'error': 'The book does not exist in the database'}, status=400)

        # Query to insert the review into the Reviews table, including the date
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "Review" ("Book_id", "Review_text", "Rating", "User_id", "Review_date")
                SELECT b."Book_id", %s, %s, %s, %s
                FROM "Books" b
                WHERE b."Book_name" = %s;
            """, [review_text, rating, user_id, review_date, book_name])

        return JsonResponse({'message': 'Review submitted successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@jwt_required
def list_reviews_for_book(request, id):
    # Check if the book with the given id exists in the database
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM "Books" WHERE "Book_id" = %s LIMIT 1;
            """, [id])
            book_exists = cursor.fetchone()

        if not book_exists:
            return JsonResponse({'error': 'The book does not exist in the database'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Execute SQL query to fetch reviews for the book
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b."Book_name", r."Review_text", r."Rating", r."Review_date"
                FROM "Review" r
                JOIN "Books" b ON r."Book_id" = b."Book_id"
                WHERE b."Book_id" = %s
            """, [id])
            results = cursor.fetchall()

            # Format the results
            reviews = [
                {
                    'book_name': row[0],
                    'review_text': row[1],
                    'rating': row[2],
                    'date': row[3],
                }
                for row in results
            ]
            
            if not reviews:
                return JsonResponse({'message': 'No reviews found for this book'}, status=200)

            return JsonResponse({'book_id': id, 'reviews': reviews}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
@jwt_required
def delete_review(request):
    # Extract data from the request
    book_name = request.data.get('book_name')
    review_text = request.data.get('review_text')

    # Check for missing required fields
    if not all([book_name, review_text]):
        return JsonResponse({'error': 'book_name and review_text are required'}, status=400)

    # Execute SQL query to delete the review
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                DELETE FROM "Reviews"
                WHERE "book_name" = %s AND "review_text" = %s
            """, [book_name, review_text])
            return JsonResponse({'message': 'Review deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




@csrf_exempt
@jwt_required
def list_reviews_for_user(request):
    # Extract the user ID from the JWT token
    user_id = request.user["id"]

    if not user_id:
        return JsonResponse({'error': 'User not authenticated'}, status=400)

    # Execute SQL query to fetch reviews written by the user
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b."Book_name", r."Review_text", r."Rating", r."Review_date"
                FROM "Review" r
                JOIN "Books" b ON r."Book_id" = b."Book_id"
                WHERE r."User_id" = %s
            """, [user_id])
            results = cursor.fetchall()

            # Format the results
            reviews = [
                {
                    'book_name': row[0],
                    'review_text': row[1],
                    'rating': row[2],
                    'date': row[3],
                }
                for row in results
            ]

            if not reviews:
                return JsonResponse({'message': 'No reviews found for this user'}, status=200)

            return JsonResponse({'user_id': user_id, 'reviews': reviews}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)