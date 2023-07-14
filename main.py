import requests
import json
import os
import subprocess
import re

github_api_tokens = None
gitlab_api_tokens = None
archive_path = None

def load_config():
	global github_api_tokens, gitlab_api_tokens, archive_path
	with open("config.json") as f:
		j = json.load(f)
		github_api_tokens = j["github_api_tokens"]
		gitlab_api_tokens = j["gitlab_api_tokens"]
		archive_path = j["archive_path"]

def get_github_repos():
	global github_api_tokens

	repos = []

	for token in github_api_tokens:
		headers = {
			"X-GitHub-Api-Version": "2022-11-28",
			"Accept": "application/vnd.github+json",
			"Authorization": "Bearer " + token
		}
		response = requests.get("https://api.github.com/user", headers=headers)

		if response.status_code != 200:
			print("API KEY ERROR: the key " + token + " is invalid or has expired! Aborting")
			continue

		resposnse_json = json.loads(response.content)
		username = resposnse_json["name"]
		print("Looking up Github repositories for user " + username)

		response = requests.get("https://api.github.com/search/repositories?q=user:" + username, headers=headers)
		resposnse_json = json.loads(response.content)

		for repo in resposnse_json["items"]:
			repos.append(repo["ssh_url"])
			if repo["private"]:
				print("Private repo found: " + repo["ssh_url"])
			else:
				print("Public repo found: " + repo["ssh_url"])
			
	return repos

def extract_repo_from_url(url):
	repo_pattern = r".+?[:/](?:[^/]+)/([^/]+)\.git"
	match = re.search(repo_pattern, url)
	return match.group(1)

def extract_username_from_url(url):
	username_pattern = r".+?[:/]([^/]+)/[^/]+\.git"
	match = re.search(username_pattern, url)
	return match.group(1)

def extract_site_from_url(url):
	site_pattern = r".+?@(.+?):"
	match = re.search(site_pattern, url)
	return match.group(1)

def update_repos(repos):
	global archive_path

	for repo in repos:
		repo_name = extract_repo_from_url(repo)
		username = extract_username_from_url(repo)
		site_name = extract_site_from_url(repo)

		repo_path = archive_path + "/" + site_name + "/" + username + "/" + repo_name

		if os.path.exists(repo_path):
			print(repo_path + " already exists. Pulling latest changes...")
			cmd = "git pull --all --force  --recurse-submodules"
			subprocess.run(cmd, shell = True, cwd=repo_path)
		else:
			print("Cloning " + repo_path)
			cmd = "git clone --recurse-submodules " + repo + " " + repo_path
			subprocess.run(cmd, shell = True)


load_config()
github_repos = get_github_repos()
update_repos(github_repos)

