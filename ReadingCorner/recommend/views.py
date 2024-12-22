from django.http import JsonResponse
from django.db import connection
from rest_framework.decorators import api_view
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@jwt_required
def recommend_books(request):
    query = """
        SELECT b."Book_name", b."Category"
        FROM "Books" b
        WHERE b."Category" = 'Horror'
        LIMIT 3;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Format the result into a list of dictionaries
    data = [
        {
            'Book Name': row[0],
            'Category': row[1]
        }
        for row in rows
    ]

    return JsonResponse({'Books': data})
