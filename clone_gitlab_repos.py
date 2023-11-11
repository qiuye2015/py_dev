import os

import gitlab

"""
pip install gitlabber 或者
pip3 install python-gitlab
"""
# GitLab Personal Access Token
token = "xxxx"
# GitLab server URL
url = "https://gitlab.nioint.com"
# Group path, e.g. "my-group"
group_path = ""
# Local directory to clone repositories into
local_dir = "./"

# Connect to GitLab server
gl = gitlab.Gitlab(url, private_token=token)

# Find the group
group = gl.groups.get(group_path)

# Iterate over the group's projects
for project in group.projects.list(all=True):
    # Clone the repository
    repo_url = project.ssh_url_to_repo
    repo_name = project.name
    repo_dir = os.path.join(local_dir, repo_name)
    if not os.path.exists(repo_dir):
        print(f"Cloning {repo_name}...")
        os.system(f"git clone {repo_url} {repo_dir}")
    else:
        print(f"{repo_name} already exists, skipping.")
