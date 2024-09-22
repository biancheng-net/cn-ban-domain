import requests
import base64
from github import Github
import os
from datetime import datetime

FILENAME = "gfwlist.txt"  # Constant filename

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
        
        # Save content to a file with the constant filename
        with open(FILENAME, "w", encoding="utf-8") as f:
            f.write(gfwlist_content)
        
        # Upload to GitHub release
        github_token = os.environ["GITHUB_TOKEN"]
        repo_name = os.environ["GITHUB_REPOSITORY"]
        
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        releases = list(repo.get_releases())
        if releases:
            release = releases[0]
            # Check if asset already exists and delete it
            for asset in release.get_assets():
                if asset.name == FILENAME:
                    asset.delete_asset()
                    print(f"Existing {FILENAME} asset deleted")
            release.upload_asset(FILENAME)
            print(f"GFWList uploaded to the latest release as {FILENAME}")
        else:
            current_date = datetime.now().strftime("%Y-%m-%d")
            release = repo.create_git_release(
                tag="latest",
                name=f"Latest GFWList - {current_date}",
                message=f"Updated GFWList on {current_date}",
                draft=False,
                prerelease=False
            )
            release.upload_asset(FILENAME)
            print(f"New release created with GFWList as {FILENAME}")
        
        # Clean up the local file
        os.remove(FILENAME)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()