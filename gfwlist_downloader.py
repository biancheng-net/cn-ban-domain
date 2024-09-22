import requests
import base64
from github import Github
import os
from datetime import datetime

def download_and_decode_gfwlist(url):
    response = requests.get(url)
    response.raise_for_status()
    encoded_content = response.text.strip()
    encoded_content = encoded_content.replace('\n', '')
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    return decoded_content

def main():
    gfwlist_url = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
    
    try:
        gfwlist_content = download_and_decode_gfwlist(gfwlist_url)
        print("GFWList downloaded and decoded successfully")
        
        # Generate a unique filename with timestamp
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"gfwlist_{current_date}.txt"
        
        # Save content to a file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(gfwlist_content)
        
        # Upload to GitHub release
        github_token = os.environ["GITHUB_TOKEN"]
        repo_name = os.environ["GITHUB_REPOSITORY"]
        
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        releases = list(repo.get_releases())
        if releases:
            release = releases[0]
            release.upload_asset(filename)
            print(f"GFWList uploaded to the latest release as {filename}")
        else:
            release = repo.create_git_release(
                tag="latest",
                name=f"Latest GFWList - {current_date}",
                message=f"Updated GFWList on {current_date}",
                draft=False,
                prerelease=False
            )
            release.upload_asset(filename)
            print(f"New release created with GFWList as {filename}")
        
        # Clean up the local file
        os.remove(filename)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()