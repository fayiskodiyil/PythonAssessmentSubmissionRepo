from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import Http404, HttpResponseBadRequest

from web.models import Repository, Topic
from .utils import fetch_repository_data

def index(request):
    # Render the index.html template
    context = {
        "is_home" : True,
        "page_title" : "Home"
    }
    return render(request, 'web/index.html', context)


def search_repositories(request):
    try:
        query = request.GET.get('query')
        page = request.GET.get('page')

        if not query:
            # If no search query provided, return bad request response
            return HttpResponseBadRequest('Please enter a search query.')

        repositories = Repository.objects.filter(name__icontains=query)

        if not repositories:
            # If repositories not found in the database, fetch from API
            fetched_data = fetch_repository_data(query)

            if 'error' in fetched_data:
                # If an error occurred during API request, raise Http404 exception
                raise Http404(fetched_data['error'])

            for item in fetched_data:
                # Create or get the Repository object
                repository, created = Repository.objects.get_or_create(
                    name=item['name'],
                    full_name=item['full_name'],
                    owner=item['owner']['login'],
                    description=item['description'],
                    stars=item['stargazers_count'],
                    forks=item['forks_count'],
                    avatar_url=item['owner']['avatar_url'],
                    html_url=item['html_url'],
                    updated_at=item['updated_at']
                )

                # Get or create Topic objects and add them to the repository
                topics = item.get('topics', [])
                for topic_name in topics:
                    topic, _ = Topic.objects.get_or_create(name=topic_name)
                    repository.topic.add(topic)

        # Re-query repositories after fetching from API
        repositories = Repository.objects.filter(name__icontains=query)
        results_count = repositories.count()

        # Paginate the repositories
        paginator = Paginator(repositories, 10)
        try:
            repositories = paginator.page(page)
        except PageNotAnInteger:
            repositories = paginator.page(1)
        except EmptyPage:
            repositories = paginator.page(paginator.num_pages)

        context = {
            'repositories': repositories,
            'query': query,
            'page_title': "Search Results",
            'results_count' : results_count
        }

        return render(request, 'web/search_results.html', context)

    except Exception as e:
        # Handle any other exceptions gracefully
        messages.error(request, str(e))
        page_context = {
            "page_title": "Error",
            "message" : e
        }
        return render(request, 'errors/500.html', page_context)