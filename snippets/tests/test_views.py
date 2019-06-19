from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from snippets.models import Snippet


class BaseTestCase(APITestCase):
    def setUp(self):
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)


class AuthUserSnippetTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.url = url = reverse('snippet-list')

    def test_authed_user_can_create_snippet(self):
        
        data = {
            'title': '',
            'code': 'print(\"hello, world\")\n',
            'linenos': False,
            'language': 'python',
            'style': 'friendly'
        }
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)

    def test_authed_user_can_update_own_snippet(self):
        pass 

    def test_authed_user_can_delete_own_snippet(self):
        pass 

    def test_authed_user_can_view_snippets(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        print(resp.content)
        # self.assertEqual(resp.content, '1')


    def test_anon_user_can_view_all_snippets(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_anon_user_cannot_create_snippet(self):
        self.client.logout()
        data = {
            'title': '',
            'code': 'print(\"hello, world\")\n',
            'linenos': False,
            'language': 'python',
            'style': 'friendly'
        }
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_anon_user_cannot_update_snippet(self):
        pass 

    def test_anon_user_cannot_delete_snippet(self):
        pass 
