from django.shortcuts import render, redirect
from testapp.models import Book  # Correct import for Book model
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import connection


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@login_required(login_url='login')
def home(request):
    # if request.user.is_authenticated:
        query = '''SELECT "BookName", "Language" FROM "Books"'''
        with connection.cursor() as cursor:
            cursor.execute(query)
            books = cursor.fetchall()
            print (books)
        # Pass the query results to the template
        return render(request, 'home.html', {'books': books})    # else:
    #     return redirect('login')  # Redirect to login if user is not authenticated
