# projects/views.py
from django.shortcuts import render
from .github_helper import fetch_wiki_page,get_wiki_page_list,get_selected_issues
from .models import Repository, UserGroupSelection
import urllib.parse
import markdown2


def home(request):
#    repo_name = 'meahmadi/projectBuilding'  # Replace with the actual repo name or make it dynamic
#    github_data = fetch_github_data(repo_name)
#    repo_name = 'meahmadi/projectBuilding'
    user_groups = UserGroupSelection.objects.filter(user=request.user).values_list('group', flat=True)
    repositories = Repository.objects.filter(group__in=user_groups)

    wikis = []
    issues_by_difficulty = {}
    for repo in repositories:
        repo_name = repo.name
        selected_issues = get_selected_issues(repo)

        wikilist = [w for w in get_wiki_page_list(repo) if w.startswith("#") or w.startswith("%23")]
        wikilist.sort(reverse=True)

        for wiki in wikilist:
            content = fetch_wiki_page(repo, wiki)
            wikiname = wiki
            if "%" in wiki:
                wikiname = urllib.parse.unquote(wikiname)
            if content:
                wikis.append({"title":"_".join(wikiname.split("_")[1:]).replace("-"," "),"content":markdown2.markdown(content),"name":wikiname})

        # Group issues by difficulty level
        for issue in selected_issues:
            issue['body'] = markdown2.markdown(issue['body'])
            level = issue['difficulty']
            if level not in issues_by_difficulty:
                issues_by_difficulty[level] = {"title":issue["level_title"],"issues":[]}
            issues_by_difficulty[level]["issues"].append(issue)
            
    issues_by_difficulty = dict(sorted(issues_by_difficulty.items(), key=lambda item: item[0]))

    return render(request, 'projects/home.html', {
        'wiki_pages': wikis,
        'issues_by_difficulty': issues_by_difficulty,
        'projects': repositories,
    })
