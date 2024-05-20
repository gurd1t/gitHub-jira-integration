from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json

# Creating a Flask app
app = Flask(__name__)

# Webhook endpoint to receive GitHub events
@app.route('/webhook', methods=['POST'])
def webhook():
    # Extracting payload from GitHub webhook
    payload = request.json

    # Checking if the payload is a comment event
    if 'comment' in payload:
        # Extracting comment body
        comment_body = payload['comment']['body']
        # Checking if the comment contains '/jira'
        if '/jira' in comment_body:
            # Extracting relevant information from the GitHub payload
            user_login = payload['issue']['user']['login']
            issue_title = payload['issue']['title']
            issue_body = payload['comment']['body']
            
            # Creating Jira issue with extracted information
            create_jira_issue(user_login, issue_title, issue_body)
            return 'Jira issue created successfully.'

    return 'No action taken.'

def create_jira_issue(user_login, issue_title, issue_body):
    # Jira API endpoint for creating an issue
    url = "<jira-url>"

    # Jira API token for authentication
    token = "<jira-token>"

    # Authentication object for Jira API
    auth = HTTPBasicAuth("<jira-email-id>", token)

    # Headers for Jira API request
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }

    # Constructing Jira issue payload with GitHub information
    payload = json.dumps({
      "fields": {
        "description": {
          "content": [
            {
              "content": [
                {
                  "text": f"GitHub user login: {user_login}\n\nGitHub issue title: {issue_title}\n\nGitHub issue body:\n{issue_body}",
                  "type": "text"
                }
              ],
              "type": "paragraph"
            }
          ],
          "type": "doc",
          "version": 1
        },
        "issuetype": {
          "id": "10005"
        },
        "project": {
          "key": "DP"
        },
        "summary": "JIRA Ticket"
      },
      "update": {}
    })

    # Sending request to create Jira issue
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    return response.text

# Running the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

