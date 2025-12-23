# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
import httpx
from typing import Optional, List

from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)

def _get_headers():
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set.")
    return {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

def _get_repo():
    github_repo = os.getenv("GITHUB_REPO")
    if not github_repo:
        raise ValueError("GITHUB_REPO environment variable not set.")
    return github_repo


def create_github_issue(
    title: str, body: str, labels: List[str] = [], tool_context: ToolContext = None
) -> str:
    """Call this tool to create a GitHub issue.
    'title' is the title of the issue.
    'body' is the body of the issue.
    'labels' is an optional list of labels to apply to the issue (e.g. ['idea', 'bug']).
    """
    logger.info("--- TOOL CALLED: create_github_issue ---")
    logger.info(f"  - Title: {title}")
    logger.info(f"  - Body: {body}")
    logger.info(f"  - Labels: {labels}")

    try:
        repo = _get_repo()
        headers = _get_headers()
        url = f"https://api.github.com/repos/{repo}/issues"
        
        payload = {
            "title": title,
            "body": body,
            "labels": labels
        }

        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            issue_data = response.json()
            issue_url = issue_data.get("html_url")
            
            logger.info(f"Successfully created issue: {issue_url}")
            return json.dumps(
                {
                    "success": True,
                    "message": f"GitHub issue created successfully: {issue_url}",
                    "issue_url": issue_url,
                    "issue_number": issue_data.get("number")
                }
            )
    except Exception as e:
        error_msg = f"Error creating issue: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"success": False, "message": error_msg})


def search_issues(
    query: str, sort_by: str = "created", tool_context: ToolContext = None
) -> str:
    """Search for issues in the repository.
    'query' is the search query (e.g., 'is:issue is:open label:idea').
    'sort_by' can be 'created', 'updated', or 'comments'.
    """
    logger.info(f"--- TOOL CALLED: search_issues query='{query}' sort='{sort_by}' ---")
    
    try:
        repo = _get_repo()
        headers = _get_headers()
        
        # Use the List Issues API instead of Search API to avoid indexing latency/errors
        url = f"https://api.github.com/repos/{repo}/issues"
        
        params = {
            "sort": sort_by,
            "direction": "desc",
            "per_page": 10
        }
        
        # Simple parsing of the query to support basic filtering
        # Supported: label:x, is:open, is:closed
        parts = query.split()
        for part in parts:
            if part.startswith("label:"):
                params["labels"] = part.split(":", 1)[1]
            elif part == "is:open":
                params["state"] = "open"
            elif part == "is:closed":
                params["state"] = "closed"
            elif part == "is:all":
                params["state"] = "all"
        
        # If no state specified, GitHub defaults to open.
        
        with httpx.Client() as client:
            req = client.build_request("GET", url, headers=headers, params=params)
            logger.info(f"Sending Request: {req.url}")
            response = client.send(req)
            response.raise_for_status()
            data = response.json()
            
            # Simplified list for the agent
            issues = []
            for item in data:
                # API returns list of issues directly
                issues.append({
                    "number": item["number"],
                    "title": item["title"],
                    "state": item["state"],
                    "comments": item["comments"],
                    "labels": [l["name"] for l in item["labels"]],
                    "author": item["user"]["login"],
                    "reactions": item.get("reactions", {}).get("+1", 0) # Basic support for upvotes
                })
                
            return json.dumps(issues)

    except Exception as e:
        error_msg = f"Error searching issues: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg})


def get_issue_details(
    issue_number: int, tool_context: ToolContext = None
) -> str:
    """Get full details for a specific issue, including comments.
    'issue_number' is the ID of the issue.
    """
    logger.info(f"--- TOOL CALLED: get_issue_details number={issue_number} ---")
    
    try:
        repo = _get_repo()
        headers = _get_headers()
        base_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
        
        with httpx.Client() as client:
            # Get Issue
            issue_resp = client.get(base_url, headers=headers)
            issue_resp.raise_for_status()
            issue = issue_resp.json()
            
            # Get Comments
            comments_resp = client.get(f"{base_url}/comments", headers=headers)
            comments_resp.raise_for_status()
            comments_data = comments_resp.json()
            
            comments = []
            for c in comments_data:
                comments.append({
                    "id": c["id"],
                    "body": c["body"],
                    "user": c["user"]["login"],
                    "created_at": c["created_at"]
                })

            result = {
                "number": issue["number"],
                "title": issue["title"],
                "body": issue["body"],
                "state": issue["state"],
                "author": issue["user"]["login"],
                "labels": [l["name"] for l in issue["labels"]],
                "reactions": issue.get("reactions", {}),
                "comments": comments
            }
            return json.dumps(result)

    except Exception as e:
        error_msg = f"Error getting issue details: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg})


def add_reaction(
    issue_number: int, reaction_type: str = "+1", tool_context: ToolContext = None
) -> str:
    """Add a reaction to an issue.
    'issue_number' is the ID of the issue.
    'reaction_type' can be '+1', '-1', 'laugh', 'confused', 'heart', 'hooray', 'rocket', 'eyes'.
    """
    logger.info(f"--- TOOL CALLED: add_reaction number={issue_number} type={reaction_type} ---")
    
    try:
        repo = _get_repo()
        headers = _get_headers()
        # Accept header for reactions preview API (though it's standard now, good practice)
        headers["Accept"] = "application/vnd.github.squirrel-girl-preview+json"
        
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/reactions"
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json={"content": reaction_type})
            response.raise_for_status()
            
            return json.dumps({"success": True, "message": "Reaction added."})

    except Exception as e:
        error_msg = f"Error adding reaction: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg})


def add_comment(
    issue_number: int, body: str, tool_context: ToolContext = None
) -> str:
    """Add a comment to an issue.
    'issue_number' is the ID of the issue.
    'body' is the comment text.
    """
    logger.info(f"--- TOOL CALLED: add_comment number={issue_number} ---")
    
    try:
        repo = _get_repo()
        headers = _get_headers()
        
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json={"body": body})
            response.raise_for_status()
            
            return json.dumps({"success": True, "message": "Comment posted."})

    except Exception as e:
        error_msg = f"Error posting comment: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"error": error_msg})