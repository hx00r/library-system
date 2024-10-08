from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers.books_serializer import BookSerializer
from .pagination import BookPagination
    
class BooksViews(APIView):
    """
    Books API end-point That contains full CRUD operation.
    """
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, id=None, format=None):
        title = request.query_params.get('title', None)
        if title: # filter by query param
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM book WHERE title="{title}"')
                row = cursor.fetchone()
                converted_result = self.convert_row(cursor=cursor, row=row)
                return Response(BookSerializer(converted_result).data, status=status.HTTP_200_OK)
        with connection.cursor() as cursor:
            if id == None:
                cursor.callproc('index_books')
                rows = cursor.fetchall()
                converted_results = self.convert_rows(cursor=cursor, rows=rows)
                paginator = BookPagination()  # Create a paginator instance
                paginated_books = paginator.paginate_queryset(converted_results, request)  # Paginate the queryset
                # Serialize the paginated results
                serializer = BookSerializer(paginated_books, many=True)  # Use your existing serializer
                return paginator.get_paginated_response(serializer.data)
            # Fetch single row 
            cursor.callproc('get_book_by_id', [id])
            row = cursor.fetchone()
            if row:
                try:
                    converted_result = self.convert_row(cursor=cursor, row=row)
                    return Response(BookSerializer(converted_result).data, status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
            return Response({'status':'no book was found'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Extract the validated data
                title = serializer.validated_data['title']
                description = serializer.validated_data['description']
                price = serializer.validated_data['price']
                rent_fee = serializer.validated_data['rent_fee']
                release_year = serializer.validated_data.get('release_year')
                author_id = serializer.validated_data.get('author_id')
                quantity = serializer.validated_data.get('quantity')
                category = serializer.validated_data['category']
                # Call the stored procedure to create the book
                cursor.callproc('create_book', [
                    title, description, price, rent_fee, release_year, author_id, quantity, category
                ])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None, format=None):
        if id is None:
            return Response({'error': 'Book ID is required for update.'}, status=status.HTTP_400_BAD_REQUEST)
        # Validate if there is a record with that ID
        with connection.cursor() as cursor:
            cursor.callproc('get_book_by_id', [id])
            row = cursor.fetchone()
            if not row: return Response({'error': 'No book found with this ID'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                # Extract the validated data
                id = serializer.validated_data['id']
                title = serializer.validated_data['title']
                description = serializer.validated_data['description']
                price = serializer.validated_data['price']
                rent_fee = serializer.validated_data['rent_fee']
                release_year = serializer.validated_data.get('release_year')
                author_id = serializer.validated_data.get('author_id')
                quantity = serializer.validated_data.get('quantity')
                category = serializer.validated_data['category']
                # Call the stored procedure to update the book
                cursor.callproc('update_book', [
                    id, title, description, price, rent_fee, release_year, author_id, quantity, category
                ])
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, format=None):
        if id is None:
            return Response({'error': 'Book ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        # Validate if there is a record with that ID
        with connection.cursor() as cursor:
            cursor.callproc('get_book_by_id', [id])
            row = cursor.fetchone()
            if not row: return Response({'error': 'No book found with this ID'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            # Call the stored procedure to delete the book
            cursor.callproc('remove_book_by_id', [id])
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)
    
    def convert_row(self, cursor, row) -> dict:
        """
        This is a helper function that will take two params and will 
        return a single object for serialization.
        @param cursor
        @param row
        """
        # Get the column names
        columns = [col[0] for col in cursor.description]
        # Convert the row into a dictionary
        return dict(zip(columns, row))
    
    def convert_rows(self, cursor, rows) -> list:
        """
        This is a helper function that will take two params and will 
        return a list of objects for serialization.
        @param cursor
        @param rows
        """
        # Get the column names
        columns = [col[0] for col in cursor.description]
        # Convert the row into a dictionary
        return [dict(zip(columns, row)) for row in rows]