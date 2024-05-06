from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import QueryDict

from web.models import Repository, Topic
from .views import search_repositories

class RepositorySearchTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.repository = Repository.objects.create(
            name='Test Repo',
            full_name='Test Repo',
            owner='test_owner',
            description='Test description',
            stars=10,
            forks=5,
            avatar_url='https://example.com/avatar.jpg',
            html_url='https://example.com/test-repo',
            updated_at='2024-01-01T00:00:00Z'
        )
        self.topic = Topic.objects.create(name='Test Topic')
        self.repository.topic.add(self.topic)

        # Set up request factory
        self.factory = RequestFactory()

    def get_request(self):
        request = self.factory.get('/')
        # Add middleware to the request
        middleware = SessionMiddleware(get_response=lambda request: None)
        middleware.process_request(request)
        middleware = MessageMiddleware(FallbackStorage(request))
        middleware.process_request(request)
        return request

    def test_search_repositories_with_query(self):
        # Test searching repositories with a query
        url = reverse('web:search_repositories')
        request = self.get_request()
        query_dict = QueryDict(mutable=True)
        query_dict['query'] = 'Test'
        request.GET = query_dict
        response = search_repositories(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Repo')

    def test_search_repositories_pagination(self):
        # Test pagination of search results
        url = reverse('web:search_repositories')
        request = self.factory.get(url, {'query': 'Test'})
        response = search_repositories(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Repo')
        self.assertContains(response, 'page-item active')
        
    def test_search_repositories_without_query(self):
        # Test searching repositories without a query
        url = reverse('web:search_repositories')
        request = self.factory.get(url)
        response = search_repositories(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Please enter a search query.')

    # def test_search_repositories_no_results(self):
    #     # Test searching repositories with no results
    #     url = reverse('web:search_repositories')
    #     request = self.factory.get(url, {'query': 'Nonexistent'})
    #     response = search_repositories(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'No repositories found for the given search query.')

    # def test_search_repositories_error(self):
    #     # Test searching repositories with an API error
    #     url = reverse('web:search_repositories')
    #     request = self.factory.get(url, {'query': 'Error'})
    #     response = search_repositories(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'An error occurred during the API request.')


    # Add more test cases as needed
