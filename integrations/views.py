import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    if not access_token:
        messages.error(request, "GitHub authorization failed.")
        return redirect('dashboard')

    # Fetch user data
    user_data = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': f'token {access_token}'}
    ).json()

    repos_data = requests.get(
        'https://api.github.com/user/repos',
        headers={'Authorization': f'token {access_token}'}
    ).json()

    languages = set()
    projects = []

    for repo in repos_data:
        projects.append(repo['name'])  # just name; you can add desc if needed
        lang_url = repo['languages_url']
        langs = requests.get(lang_url, headers={'Authorization': f'token {access_token}'}).json()
        languages.update(langs.keys())

    # ✅ Save to user model (not resume)
    request.user.github_skills = list(languages)
    request.user.github_projects = projects
    request.user.save()

    messages.success(request, "✅ GitHub data saved to your profile!")
    return redirect('dashboard')
