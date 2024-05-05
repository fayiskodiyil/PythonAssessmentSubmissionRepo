from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

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
    query = request.GET.get('query')
    page = request.GET.get('page')

    if not query:
        # If no search query provided, display error message
        page_context = {
            "is_home" : True,
            "page_title" : "Home",
            'message' : 'Please enter a search query.'
        }

        return render(request, 'web/index.html', page_context)

    repositories = Repository.objects.filter(name__icontains=query)

    if not repositories:
        # If repositories not found in the database, fetch from API
        fetched_data = fetch_repository_data(query)

        print("fetched_data",fetched_data)

        if 'error' in fetched_data:
            # If an error occurred during API request, display error message
            messages.error(request, fetched_data['error'])
            page_context = {
                "page_title" : "Error",
            }
            return render(request, 'web/errors.html', page_context)

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
        'page_title' : "Search Results"
    }

    return render(request, 'web/search_results.html', context)