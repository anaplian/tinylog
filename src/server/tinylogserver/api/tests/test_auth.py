"""Tests for authentcation against the Tiny Log Server REST API"""
import json

from django.test import TestCase


class TestUserAccountCreation(TestCase):
    def test_create_user_success(self):
        """Should create a new user resource upon valid request

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and the user data is valid
            Then a 201 response should be returned
                 and a link to the new user resource should be returned
        """
        user_data = {
            'username': 'aflorrick',
            'display_name': 'alicia',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        created_resource_response = \
            self.client.get(response.get('location')).json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            'username' in created_resource_response
            and created_resource_response.get('username') == 'aflorrick'
        )
        self.assertTrue(
            'display_name' in created_resource_response
            and created_resource_response.get('display_name') == 'alicia'
        )

    def test_create_user_success_no_display_name(self):
        """Should create a new user resource upon valid request

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and the user data is valid
                 and no display name is given
            Then a 201 response should be returned
                 and a link to the new user resource should be returned
        """
        user_data = {
            'username': 'aflorrick',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        created_resource_response = \
            self.client.get(response.get('location')).json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            'username' in created_resource_response
            and created_resource_response.get('username') == 'aflorrick'
        )
        self.assertTrue(
            'display_name' in created_resource_response
            and created_resource_response.get('display_name') == None
        )

    def test_create_user_missing_username(self):
        """Should return an error if no username is given

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and no username is given
            Then a 400 response should be returned
        """
        user_data = {
            'display_name': 'alicia',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_username_contains_bad_chars(self):
        """Should return an error if a username is given with bad characters

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and a username containing forbidden characters is given
            Then a 400 response should be returned
        """
        user_data = {
            'username': '$$>>?',
            'display_name': 'alicia',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_username_too_long(self):
        """Should return an error if an overly long username is given

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and a long user name is given
            Then a 400 response should be returned
        """
        user_data = {
            'username': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'display_name': 'alicia',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_display_name_contains_bad_chars(self):
        """Should return an error if a display name is given with bad characters

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and a display name containing forbidden characters is given
            Then a 400 response should be returned
        """
        user_data = {
            'username': 'aflorrick',
            'display_name': '$$>>?',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_display_name_too_long(self):
        """Should return an error if an overly long display name is given

            Given that a user is not logged in
            When a user POSTs new user data to the /users URL
                 and a long display name is given
            Then a 400 response should be returned
        """
        user_data = {
            'username': 'aflorrick',
            'display_name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'password': 'goodwife123',
        }
        response = self.client.post('/api/users/', user_data)
        self.assertEqual(response.status_code, 400)
