from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json

# Creating a Flask app interface
app = Flask(__name__)

# Decorator for the webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    # Getting the payload from the GitHub webhook
    payload = request.json

    # Extracting relevant information from the payload
    user_login = payload['issue']['user']['login']
    issue_title = payload['issue']['title']
    issue_body = payload['comment']['body']

    # Checking if the comment contains '/jira'
    if '/jira' in issue_body:
        # Creating Jira issue with extracted information
        create_jira_issue(user_login, issue_title, issue_body)
        return 'Jira issue created successfully.'

    return 'No action taken.'

# Function to create a Jira issue
def create_jira_issue(user_login, issue_title, issue_body):
    url = "https://jira-domain/rest/api/3/issue"
    token = "JIRA_API_TOKEN"
    auth = HTTPBasicAuth("JIRA_EMAIL", token)
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
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
          "key": "PROJECT_KEY"
        },
        "summary": "JIRA Ticket"
      },
      "update": {}
    })
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
