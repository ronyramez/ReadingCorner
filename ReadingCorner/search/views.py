from django.shortcuts import render
from django.db import connection  # To execute raw SQL queries
from rest_framework.decorators import api_view
from ReadingCorner.decorators import jwt_required
from django.views.decorators.csrf import csrf_exempt

@jwt_required
@csrf_exempt
def search(request):
    context = {}
    if request.method == 'GET':
        search_query = request.GET.get('querySearch', '').strip()  # Get the search query (can be empty)
        language_filter = request.GET.get('language', '').strip()  # Get the language filter (can be empty)

        # Base SQL query
        query = """
            SELECT "Book_name", "Author", "Language" 
            FROM "Books"
            WHERE 1 = 1
        """
        params = []

        # Add search query condition if provided
        if search_query:
            query += ' AND "BookName" ILIKE %s'
            params.append(f'%{search_query}%')

        # Add language filter condition if provided and not empty
        if language_filter:
            query += ' AND "Language" = %s'
            params.append(language_filter)

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        # Add results to the context
        context['results'] = [
            {
                'BookName': row[0],
                'Author': row[1],
                'Language': row[2],
                'Content': row[3],
            } for row in results
        ]

    return render(request, 'search.html', context)
