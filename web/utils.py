import requests

def fetch_repository_data(query):
    try:
        url = f'https://api.github.com/search/repositories?q={query}+in:name'
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        if response.status_code == 200:
            return response.json()['items']
        else:
            return {'error': f"API request failed with status code {response.status_code}"}
    except requests.RequestException as e:
        return {'error': f"Error fetching data: {e}"}