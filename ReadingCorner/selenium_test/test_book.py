import requests
import pytest

# JWT token for authentication
JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJlbWFpbCI6InRlc3RAbWFpbC5jb20iLCJleHAiOjE3MzQ4NzM2NDl9.-wXFl6fJgOVUhl1Ae8DAFqkg34xI3viCInagauWmtUA'

# @pytest.fixture
# def headers():
#     """Fixture to provide the authentication headers."""
#     return {
#         "Authorization": f"Bearer {JWT_TOKEN}",
#         "Content-Type": "application/json",
#     }

def test_books_json_response():
    """Test the JSON response from the /books/ endpoint."""
    # Make a GET request to the /books/ endpoint
    response = requests.get("http://127.0.0.1:8000/books/")
    
    # Assert that the request was successful
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Parse the JSON response
    books = response.json()
    
    # Assert that the response contains a list of books
    assert isinstance(books, list), "Expected a list of books in the response"
    assert len(books) > 0, "The books list is empty"
    
    # Optional: Print the first book's details for debugging
    print(f"Test passed! Found {len(books)} books.")
    print("First book:", books[0])

