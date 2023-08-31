# Example scripts for using GitHubAPI for data collection

## Required package
strudel scraper (https://cmustrudel.github.io/strudel.scraper/)

### Installation
```bash
    pip install --user --upgrade strudel.scraper


## GithubAPI_Example_IssueTimeline.py
an example of collecting event timelines for a given list of issues and repositories.(issue ids and reposlugs need to be provided)

## githubSettings.py 
Set up the tokens needed for using GitHub API. Please generate the tokens via your GitHub account as needed

##repo_issues.ipynb
An example of collecting issues for a given repository. (repo slugs need to be provided)

## githubSearch.py
using package PyGithub to utilize the search engine of GithubAPI to search for repositories, commits, codes, etc. with advanced search queries.
