# projects/views.py
from django.shortcuts import render
from .models import WikiPage, Project
from .github_helper import fetch_github_data,fetch_wiki_page


def home(request):
#    repo_name = 'meahmadi/projectBuilding'  # Replace with the actual repo name or make it dynamic
#    github_data = fetch_github_data(repo_name)

    content = fetch_wiki_page('meahmadi/projectBuilding', 'Home')
    if content:
        print(content)  # Process the markdown content as needed


    return render(request, 'projects/home.html', {
        'wiki_pages': [{"title":'Home',"content":content}],
        'projects': [],
    })
