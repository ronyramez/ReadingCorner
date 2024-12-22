from django.http import JsonResponse
from django.db import connection
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ReadingCorner.decorators import jwt_required


@jwt_required
@csrf_exempt
def top_rated_books(request):
    query = """
        SELECT b."Book_id", b."Book_name", r."Rating"
        FROM "Books" b
        JOIN "Review" r ON b."Book_id" = r."Book_id"
        WHERE r."Rating" IN (
            SELECT DISTINCT "Rating"
            FROM "Review"
            ORDER BY "Rating" DESC
            LIMIT 7
        )
        ORDER BY r."Rating" DESC
        LIMIT 3;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Format the result into a list of dictionaries
    data = [
        {'id': row[0], 'Name': row[1], 'Rating': row[2]}
        for row in rows
    ]

    return JsonResponse({'Trending books': data})
