import requests


def get_github_repo_by_name(username: str) -> list:
    """Get all public repos for the specified GitHub user."""
    repositories: list = []
    page: int = 1

    while True:
        url: str = f'https://api.github.com/users/{username}/repos'
        params: dict[str, str | int] = {
            'type': 'public',
            'per_page': 100,
            'page': page
        }

        response = requests.get(url=url, params=params)
        response.raise_for_status()

        repos = response.json()
        if not repos:
            break

        repositories.extend(repos)
        page += 1

    return repositories


def main():
    try:
        repos = get_github_repo_by_name('jackoCode')

        for repo in repos:
            print(f'{repo["name"]}: {repo["html_url"]}')

    except requests.exceptions.HTTPError as e:
        print(f'API error occurred: {e}')
    except requests.exceptions.RequestException as e:
        print(f'Request error: {e}')


if __name__ == '__main__':
    main()
