import sys
import requests

# GitHub API base URL
base_url = "https://api.github.com"

# Function to add an issue to a project column
def add_issue_to_project(repo_owner, repo_name, project_id, column_name, issue_number):
    try:
        # Headers for GitHub API requests
        headers = {
            "Authorization": f"token {sys.argv[1]}",
            "Accept": "application/vnd.github.inertia-preview+json",  # Enable Projects API preview
        }
        
        # Find the column ID
        url = f"{base_url}/repos/{repo_owner}/{repo_name}/projects/{project_id}/columns"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        columns_data = response.json()

        column_id = None
        for column in columns_data:
            if column["name"] == column_name:
                column_id = column["id"]
                break
        
        if not column_id:
            print(f"Column '{column_name}' not found in project.")
            return False
        
        # Add issue to project column
        url = f"{base_url}/repos/{repo_owner}/{repo_name}/projects/columns/{column_id}/cards"
        payload = {"content_id": issue_number, "content_type": "Issue"}
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print(f"Issue {issue_number} added to project column '{column_name}' successfully")
            return True
        else:
            print(f"Failed to add issue {issue_number} to project column '{column_name}'. Status code: {response.status_code}")
            print("Response content:", response.content.decode('utf-8'))
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error adding issue to project: {e}")
        return False

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python add_issue_to_project.py <github_token> <repo_owner> <repo_name> <project_id> <column_name> <issue_number>")
        sys.exit(1)
    
    github_token = sys.argv[1]
    repo_owner = sys.argv[2]
    repo_name = sys.argv[3]
    project_id = sys.argv[4]
    column_name = sys.argv[5]
    issue_number = sys.argv[6]

    added = add_issue_to_project(repo_owner, repo_name, project_id, column_name, issue_number)
    if added:
        sys.exit(0)
    else:
        sys.exit(1)
