# Repo backup

A lil script that automatically creates a local archive of all your repos from Github and Gitlab. You can run it periodically to keep your archive up to date.

## Requirements

You need to have `git` and `python3` installed and accessible through CLI. 
This scrips works only with SSH, so all your Github and Gitlab accounts need to have SSH access keys set up.


Useful links:

https://www.atlassian.com/git/tutorials/git-ssh

https://gist.github.com/Tamal/1cc77f88ef3e900aeae65f0e5e504794

https://github.com/settings/keys

https://gitlab.com/-/profile/keys

## Setup

Clone this repo, specify your api tokens and path where you want you repos to be saved to in `config.json`:

```json
{
	"archive_path": "path/to/your/archive",
	"github_api_tokens":
	[
		"github_token1",
		"github_token2"
	],
	"gitlab_api_tokens":
	[
		"gitlab_token1",
		"gitlab_token2"
	]
}
```

Specify several API tokens, if you want to archive repositories from several different accounts. 

You can get access tokens here:

https://github.com/settings/tokens?type=beta

https://gitlab.com/-/profile/personal_access_tokens

Note that APi keys need to have the permission to read your repositories and your user info.

**NOTE**: API tokens have an expiration date, you'll have to refresh them if you want to run the script continiousy.

## Usage

Run the script from the root directory of this repo, using:

```bash
python main.py
```

or

```bash
python3 main.py
```


The script runs only once, if you want it to run automatically/periodically, you need to set it up on your own.

