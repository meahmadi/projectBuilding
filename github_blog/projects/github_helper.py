import requests
from django.core.cache import cache
from django.conf import settings

from bs4 import BeautifulSoup

def get_wiki_page_list(repo):
    # URL to the wiki's home page
    url = f"https://github.com/{repo.name}/wiki"
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = []
        
        # Find all wiki page links (adjust selector if GitHub’s structure changes)
        for link in soup.select('a'):
            link_text = link.get('href')
            if link_text.startswith(f"/{repo.name}/wiki"):
                wiki_page_names = link_text.split('/')
                if len(wiki_page_names)>4 and len(wiki_page_names[4])>0:
                    page_name = wiki_page_names[4]
                    if page_name not in pages:
                        pages.append(page_name)  # Extracts the page name
        
        return pages
    else:
        print("Failed to retrieve wiki page list:", response.status_code)
        return []

def fetch_wiki_page(repo, page_name):
    # Construct the URL to the raw wiki page file
    url = f"https://raw.githubusercontent.com/wiki/{repo.name}/{page_name}.md"
    headers = {'Authorization': repo.token}
    try:
        response = requests.get(url, headers=headers)
        # print(response)    
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


def get_selected_issues(repo):
    url = f"https://api.github.com/repos/{repo.name}/issues"
    headers = {'Authorization': repo.token}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        issues = response.json()
        selected_issues = []

        for issue in issues:
            for label in issue.get('labels', []):
                label_name = label.get('name', '')
                label_description = label.get('description','')
                # Check if label starts with "#" and extract difficulty level
                if label_name.startswith('#') and label_name[1:].isdigit():
                    difficulty = int(label_name[1:])  # Extract number after #
                    selected_issues.append({
                        'title': issue.get('title'),
                        'url': issue.get('html_url'),
                        'difficulty': difficulty,
                        'level_title': label_description,
                        'body': issue.get('body', '')
                    })
                    break  # Only take the first matching label

        # Sort issues by difficulty level
        selected_issues.sort(key=lambda x: x['difficulty'],reverse=True)
        return selected_issues
    else:
        print("Failed to retrieve issues:", response.status_code)
        return []



