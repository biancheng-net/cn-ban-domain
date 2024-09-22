import requests
import base64
from github import Github
import os

def download_and_decode_gfwlist(url):
    response = requests.get(url)
    response.raise_for_status()
    encoded_content = response.text.strip()
    # Remove newlines from the encoded content
    encoded_content = encoded_content.replace('\n', '')
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    return decoded_content

def main():
    gfwlist_url = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
    
    try:
        gfwlist_content = download_and_decode_gfwlist(gfwlist_url)
        print("GFWList downloaded and decoded successfully")
        
        # Save content to a file
        with open("gfwlist.txt", "w", encoding="utf-8") as f:
            f.write(gfwlist_content)
        
        # Upload to GitHub release
        github_token = os.environ["GITHUB_TOKEN"]
        repo_name = os.environ["GITHUB_REPOSITORY"]
        
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        releases = list(repo.get_releases())
        if releases:
            release = releases[0]
            release.upload_asset("gfwlist.txt")
            print("GFWList uploaded to the latest release")
        else:
            release = repo.create_release(
                "latest",
                name="Latest GFWList",
                body="Updated GFWList",
                draft=False,
                prerelease=False
            )
            release.upload_asset("gfwlist.txt")
            print("New release created with GFWList")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()