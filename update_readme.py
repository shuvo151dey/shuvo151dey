import requests
import base64
import json
import os

# GitHub details
GITHUB_USERNAME = "shuvo151dey"
REPO_NAME = GITHUB_USERNAME  # Profile repo is same as GitHub username
README_FILE = "README.md"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Use an environment variable for security

# LeetCode API URL
LEETCODE_API = f"https://leetcode-stats-api.herokuapp.com/{GITHUB_USERNAME}"

# Fetch LeetCode Stats
def fetch_leetcode_stats():
    response = requests.get(LEETCODE_API)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching LeetCode stats")
        return None

# Fetch current README content from GitHub
def get_readme_content():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{README_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        content = response.json()
        return base64.b64decode(content["content"]).decode("utf-8"), content["sha"]
    else:
        print("Error fetching README file")
        return None, None

# Update README with LeetCode Stats in the Placeholder
def update_readme():
    stats = fetch_leetcode_stats()
    if not stats:
        return

    # Fetch current README content
    readme_content, sha = get_readme_content()
    if readme_content is None:
        return

    # New stats content
    stats_section = f"""<!-- LEETCODE-STATS-START -->
🔢 **Total Solved:** {stats['totalSolved']}  
🏆 **Ranking:** {stats['ranking']}  
🔥 **Easy:** {stats['easySolved']} | **Medium:** {stats['mediumSolved']} | **Hard:** {stats['hardSolved']}  
<!-- LEETCODE-STATS-END -->"""

    # Replace content between the placeholders
    if "<!-- LEETCODE-STATS-START -->" in readme_content and "<!-- LEETCODE-STATS-END -->" in readme_content:
        new_readme_content = readme_content.split("<!-- LEETCODE-STATS-START -->")[0] + stats_section + readme_content.split("<!-- LEETCODE-STATS-END -->")[-1]
    else:
        print("❌ Placeholder not found in README! Please add it manually.")
        return

    # Encode content in base64
    updated_content_encoded = base64.b64encode(new_readme_content.encode("utf-8")).decode("utf-8")

    # Update README on GitHub
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{README_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
    data = {
        "message": "Updated LeetCode stats in README",
        "content": updated_content_encoded,
        "sha": sha,
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("✅ README updated successfully!")
    else:
        print("❌ Failed to update README:", response.json())

# Run the script
update_readme()
