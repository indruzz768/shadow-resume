import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def github_login(request):
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&scope=read:user repo"
    )
    return redirect(github_auth_url)


@login_required
def github_callback(request):
    code = request.GET.get('code')
    token_response = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},
        data={
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code,
        }
    )
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    # Now fetch user data
    user_data = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': f'token {access_token}'}
    ).json()

    repos_data = requests.get(
        'https://api.github.com/user/repos',
        headers={'Authorization': f'token {access_token}'}
    ).json()

    languages = []
    projects = []

    for repo in repos_data:
        projects.append(f"{repo['name']}: {repo.get('description', '')}")
        lang_url = repo['languages_url']
        langs = requests.get(lang_url, headers={'Authorization': f'token {access_token}'}).json()
        languages.extend(list(langs.keys()))

    # Save into Resume model (optional – create logic to update latest resume)
    request.user.resume_set.first().skills = ', '.join(set(languages))
    request.user.resume_set.first().projects = '\n'.join(projects)
    request.user.resume_set.first().save()

    return render(request, 'integrations/github_success.html', {
        'user_data': user_data,
        'projects': projects,
        'skills': list(set(languages)),
    })
