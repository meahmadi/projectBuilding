import requests
from django.core.cache import cache
from django.conf import settings


def fetch_wiki_page(repo_name, page_name):
    # Construct the URL to the raw wiki page file
    url = f"https://raw.githubusercontent.com/wiki/{repo_name}/{page_name}.md"
    headers = {'Authorization': f'{settings.GITHUB_TOKEN}'}
    print(url,headers)
    try:
        response = requests.get(url, headers=headers)
        print(response)    
        # Check if the page exists
        if response.status_code == 200:
            return response.text  # Returns the markdown content of the wiki page
        elif response.status_code == 404:
            print("Wiki page not found.")
        else:
            print("Error fetching the wiki page:", response.status_code)

    except requests.RequestException as e:
        print("Error fetching data:", e)
    
    return None  # Return None if there was an issue


def fetch_github_data(repo_name):
    # Define the cache key and check if data is already cached
    cache_key = f'github_data_{repo_name}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    # Fetch wiki pages and project data from GitHub API
    github_api_base = "https://api.github.com/repos"
    headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}  # Ensure GITHUB_TOKEN is set in your settings

    wiki_url = f"{github_api_base}/{repo_name}/wiki"
    project_url = f"{github_api_base}/{repo_name}/projects"
    print(wiki_url,project_url)

    try:
        wiki_response = requests.get(wiki_url, headers=headers)
        project_response = requests.get(project_url, headers=headers)

        print(wiki_response,project_response)

        # Check if the response is successful
        if wiki_response.status_code == 200 and project_response.status_code == 200:
            data = {
                'wiki_pages': wiki_response.json(),
                'projects': project_response.json()
            }
            
            # Cache the data for a specified timeout period (e.g., 10 minutes)
            cache.set(cache_key, data, timeout=600)  # 600 seconds = 10 minutes
            return data

    except requests.RequestException as e:
        print("Error fetching data:", e)

    return None  # Return None if there was an issue
