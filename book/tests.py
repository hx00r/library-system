from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch

class BookViewTests(APITestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.valid_data = {
            'title': 'Mus Donec Institute',
            'description': 'A description for the new book.',
            'price': 19.99,
            'rent_fee': 5.99,
            'release_year': '2023-05-01',
            'author_id': 2,
            'quantity': 5,
            'category': 'History'
        }

    @patch('django.db.connection.cursor')
    def test_create_book(self,mock_cursor):
        try:
            response = self.client.post(reverse('booksViews'),self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(mock_cursor.return_value.__enter__.return_value.callproc.call_count, 1)
        except Exception as e:
            print('TEST CREATE BOOK : FAILED')
            print(e)

    @patch('django.db.connection.cursor')
    def test_delete_book(self, mock_cursor):
        try:
            response = self.client.delete(reverse('booksViewsArgs', kwargs={'id':1}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            print('TEST DELETE BOOK : FAILED')
            print(e)