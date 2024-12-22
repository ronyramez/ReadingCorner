from django.http import JsonResponse
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt


##
# @authentication_classes([JWTAuthentication])  # Ensure JWT authentication is used
# @permission_classes([IsAuthenticated])  # Ensure the user is authenticated
# @api_view(['GET'])
@csrf_exempt
@jwt_required
def get_all_books(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
    search_query = request.GET.get('booksearch', '').strip()  # Get the search query from the request (can be empty)
    
    # if not search_query:
    #     return JsonResponse({'error': 'Search query is required'}, status=400)

    # Base SQL query
    query = """
        SELECT "Author", "Language", "ISBN", "Description", "Book_name",
               "Category", "Publisher", "Publishing_number", "Publishing_year"
        FROM "Books"
        WHERE 1 = 1
    """
    params = []

    # Add search query condition if provided
    if search_query:
        query += ' AND "Book_name" ILIKE %s'
        params.append(f'%{search_query}%')

    try:
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        # Check if results are empty
        if not results:
            return JsonResponse({'message': 'No books found matching your search.'}, status=404)

        # Prepare the result data
        books_data = [
            {
                'Author': row[0],
                'Language': row[1],
                'ISBN': row[2],
                'Description': row[3],
                'BookName': row[4],
                'Category': row[5],
                'Publisher': row[6],
                'PublishingNumber': row[7],
                'PublishingYear': row[8],
            } for row in results
        ]

        # Return the data as JSON response
        return JsonResponse({'books': books_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
@jwt_required
def get_book(request, id):
    # SQL query to fetch a single book by ID
    query = """
        SELECT 
            "Author", 
            "Language", 
            "ISBN", 
            "Description", 
            "Book_name", 
            "Category", 
            "Publisher", 
            "Publishing_number", 
            "Publishing_year"
        FROM "Books"
        WHERE "Book_id" = %s
    """

    # Execute the query
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, [id])
            result = cursor.fetchone()

            if not result:
                return JsonResponse({"error": "Book not found"}, status=404)

            # Format the result as a dictionary
            book = {
                "author": result[0],
                "language": result[1],
                "isbn": result[2],
                "description": result[3],
                "book_name": result[4],
                "category": result[5],
                "publisher": result[6],
                "publishing_number": result[7],
                "publishing_year": result[8],
            }
            return JsonResponse({"book": book}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
