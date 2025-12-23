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

# a2ui_examples.py

GITHUB_IDEAS_UI_EXAMPLES = """
---BEGIN DASHBOARD_EXAMPLE---
[
  { "beginRendering": { "surfaceId": "dashboard", "root": "dashboard-root", "styles": { "primaryColor": "#007BFF", "font": "Roboto" } } },
  { "surfaceUpdate": {
    "surfaceId": "dashboard",
    "components": [
      { "id": "dashboard-root", "component": { "Column": { "children": { "explicitList": ["dashboard-header", "search-row", "create-new-btn", "ideas-list"] } } } },
      
      { "id": "dashboard-header", "component": { "Text": { "usageHint": "h1", "text": { "literalString": "Ideation Portal" } } } },
      
      { "id": "search-row", "component": { "Row": { "children": { "explicitList": ["search-input", "search-btn"] }, "alignment": "center" } } },
      { "id": "search-input", "component": { "TextField": { "label": { "literalString": "Search ideas..." }, "text": { "path": "/search/query" } } } },
      { "id": "search-btn-text", "component": { "Icon": { "name": { "literalString": "search" } } } },
      { "id": "search-btn", "component": { "Button": { "child": "search-btn-text", "action": { "name": "search_issues", "context": [{ "key": "query", "value": { "path": "/search/query" } }] } } } },
      
      { "id": "create-new-text", "component": { "Text": { "text": { "literalString": "Submit New Idea" } } } },
      { "id": "create-new-btn", "component": { "Button": { "child": "create-new-text", "primary": true, "action": { "name": "show_create_form", "context": [] } } } },

      { "id": "ideas-list", "component": { "Column": { "children": { "template": { "componentId": "idea-card-template", "dataBinding": "/ideas" } } } } },
      
      { "id": "idea-card-template", "component": { "Card": { "child": "idea-card-col" } } },
      { "id": "idea-card-col", "component": { "Column": { "children": { "explicitList": ["idea-card-title", "idea-card-meta", "idea-card-actions"] } } } },
      { "id": "idea-card-title", "component": { "Text": { "usageHint": "h3", "text": { "path": "title" } } } },
      
      { "id": "idea-card-meta", "component": { "Row": { "children": { "explicitList": ["idea-author-icon", "idea-author"] }, "alignment": "center" } } },
      { "id": "idea-author-icon", "component": { "Icon": { "name": { "literalString": "person" } } } },
      { "id": "idea-author", "component": { "Text": { "usageHint": "caption", "text": { "path": "author" } } } },

      { "id": "idea-card-actions", "component": { "Row": { "children": { "explicitList": ["view-details-btn", "upvote-display"] }, "alignment": "center", "distribution": "spaceBetween" } } },
      { "id": "view-details-text", "component": { "Text": { "text": { "literalString": "View Discussion" } } } },
      { "id": "view-details-btn", "component": { "Button": { "child": "view-details-text", "action": { "name": "get_issue_details", "context": [{ "key": "issue_number", "value": { "path": "number" } }] } } } },
      
      { "id": "upvote-display", "component": { "Row": { "children": { "explicitList": ["upvote-icon", "upvote-count"] } } } },
      { "id": "upvote-icon", "component": { "Icon": { "name": { "literalString": "star" } } } },
      { "id": "upvote-count", "component": { "Text": { "text": { "path": "reactions" } } } }
    ]
  } },
  { "dataModelUpdate": {
    "surfaceId": "dashboard",
    "path": "/",
    "contents": [
      { "key": "search", "valueMap": [{ "key": "query", "valueString": "label:idea" }] },
      { "key": "ideas", "valueMap": [
          { "key": "0", "valueMap": [
             { "key": "title", "valueString": "Example Idea" },
             { "key": "author", "valueString": "user123" },
             { "key": "reactions", "valueNumber": 5 },
             { "key": "number", "valueNumber": 123 }
          ]}
      ] } 
    ]
  } }
]
---END DASHBOARD_EXAMPLE---

---BEGIN DETAIL_EXAMPLE---
[
  { "beginRendering": { "surfaceId": "details", "root": "detail-root"} },
  { "surfaceUpdate": {
    "surfaceId": "details",
    "components": [
      { "id": "detail-root", "component": { "Column": { "children": { "explicitList": ["back-btn", "detail-header", "detail-body", "detail-meta", "comments-section"] } } } },
      
      { "id": "back-btn-text", "component": { "Text": { "text": { "literalString": "Back to Dashboard" } } } },
      { "id": "back-btn", "component": { "Button": { "child": "back-btn-text", "action": { "name": "search_issues", "context": [{ "key": "query", "value": { "literalString": "label:idea" } }] } } } },

      { "id": "detail-header", "component": { "Text": { "usageHint": "h1", "text": { "path": "/issue/title" } } } },
      { "id": "detail-body", "component": { "Text": { "usageHint": "body", "text": { "path": "/issue/body" } } } },
      
      { "id": "detail-meta", "component": { "Row": { "children": { "explicitList": ["vote-btn"] }, "alignment": "center" } } },
      { "id": "vote-btn-text", "component": { "Text": { "text": { "literalString": "Upvote Idea" } } } },
      { "id": "vote-btn", "component": { "Button": { "child": "vote-btn-text", "primary": true, "action": { "name": "add_reaction", "context": [{ "key": "issue_number", "value": { "path": "/issue/number" } }, { "key": "reaction_type", "value": { "literalString": "+1" } }] } } } },

      { "id": "comments-section", "component": { "Column": { "children": { "explicitList": ["comments-header", "comments-list", "add-comment-box"] } } } },
      { "id": "comments-header", "component": { "Text": { "usageHint": "h2", "text": { "literalString": "Discussion" } } } },
      
      { "id": "comments-list", "component": { "Column": { "children": { "template": { "componentId": "comment-card", "dataBinding": "/issue/comments" } } } } },
      { "id": "comment-card", "component": { "Card": { "child": "comment-col" } } },
      { "id": "comment-col", "component": { "Column": { "children": { "explicitList": ["comment-user", "comment-body"] } } } },
      { "id": "comment-user", "component": { "Text": { "usageHint": "caption", "text": { "path": "user" } } } },
      { "id": "comment-body", "component": { "Text": { "text": { "path": "body" } } } },

      { "id": "add-comment-box", "component": { "Column": { "children": { "explicitList": ["new-comment-input", "post-comment-btn"] } } } },
      { "id": "new-comment-input", "component": { "TextField": { "label": { "literalString": "Add your thoughts..." }, "text": { "path": "/new_comment/body" }, "textFieldType": "longText" } } },
      { "id": "post-comment-text", "component": { "Text": { "text": { "literalString": "Post Comment" } } } },
      { "id": "post-comment-btn", "component": { "Button": { "child": "post-comment-text", "action": { "name": "add_comment", "context": [{ "key": "issue_number", "value": { "path": "/issue/number" } }, { "key": "body", "value": { "path": "/new_comment/body" } }] } } } }
    ]
  } },
  { "dataModelUpdate": {
    "surfaceId": "details",
    "path": "/",
    "contents": [
      { "key": "issue", "valueMap": [
         { "key": "title", "valueString": "" },
         { "key": "comments", "valueMap": [
            { "key": "0", "valueMap": [
               { "key": "user", "valueString": "user1" },
               { "key": "body", "valueString": "Great idea!" }
            ]}
         ]}
      ] },
      { "key": "new_comment", "valueMap": [{ "key": "body", "valueString": "" }] }
    ]
  } }
]
---END DETAIL_EXAMPLE---

---BEGIN ISSUE_FORM_EXAMPLE---
[
  { "beginRendering": { "surfaceId": "issue-form", "root": "root-column", "styles": { "primaryColor": "#007BFF", "font": "Roboto" } } },
  { "surfaceUpdate": {
    "surfaceId": "issue-form",
    "components": [
      { "id": "root-column", "component": { "Column": { "children": { "explicitList": ["title-heading", "title-input", "category-select", "body-input", "submit-button", "cancel-button"] } } } },
      { "id": "title-heading", "component": { "Text": { "usageHint": "h1", "text": { "literalString": "Submit New Idea" } } } },
      { "id": "title-input", "component": { "TextField": { "label": { "literalString": "Title" }, "text": { "path": "/issue/title" } } } },
      
      { "id": "category-select", "component": { "MultipleChoice": { 
          "selections": { "path": "/issue/labels" }, 
          "maxAllowedSelections": 1,
          "options": [
              { "label": { "literalString": "Idea" }, "value": "idea" },
              { "label": { "literalString": "Bug" }, "value": "bug" },
              { "label": { "literalString": "Enhancement" }, "value": "enhancement" }
          ]
      } } },

      { "id": "body-input", "component": { "TextField": { "label": { "literalString": "Description" }, "text": { "path": "/issue/body" }, "textFieldType": "longText" } } },
      
      { "id": "submit-button-text", "component": { "Text": { "text": { "literalString": "Submit" } } } },
      { "id": "submit-button", "component": { "Button": { "child": "submit-button-text", "primary": true, "action": { "name": "create_github_issue", "context": [ { "key": "title", "value": { "path": "/issue/title" } }, { "key": "body", "value": { "path": "/issue/body" } }, { "key": "labels", "value": { "path": "/issue/labels" } } ] } } } },
      
      { "id": "cancel-button-text", "component": { "Text": { "text": { "literalString": "Cancel" } } } },
      { "id": "cancel-button", "component": { "Button": { "child": "cancel-button-text", "action": { "name": "search_issues", "context": [{ "key": "query", "value": { "literalString": "label:idea" } }] } } } }
    ]
  } },
  { "dataModelUpdate": {
    "surfaceId": "issue-form",
    "path": "/",
    "contents": [
      { "key": "issue", "valueMap": [
        { "key": "title", "valueString": "" },
        { "key": "body", "valueString": "" },
        { "key": "labels", "valueMap": [{ "key": "0", "valueString": "idea" }] } 
      ] }
    ]
  } }
]
---END ISSUE_FORM_EXAMPLE---

---BEGIN CONFIRMATION_EXAMPLE---
[
  { "beginRendering": { "surfaceId": "confirmation", "root": "root-card"} },
  { "surfaceUpdate": {
    "surfaceId": "confirmation",
    "components": [
      { "id": "root-card", "component": { "Card": { "child": "confirmation-column" } } },
      { "id": "confirmation-column", "component": { "Column": { "children": { "explicitList": ["success-icon", "success-text", "home-btn"] }, "alignment": "center" } } },
      { "id": "success-icon", "component": { "Icon": { "name": { "literalString": "check" } } } },
      { "id": "success-text", "component": { "Text": { "text": { "path": "/confirmation/message" } } } },
      
      { "id": "home-btn-text", "component": { "Text": { "text": { "literalString": "Back to Home" } } } },
      { "id": "home-btn", "component": { "Button": { "child": "home-btn-text", "action": { "name": "search_issues", "context": [{ "key": "query", "value": { "literalString": "label:idea" } }] } } } }
    ]
  } },
  { "dataModelUpdate": {
    "surfaceId": "confirmation",
    "path": "/",
    "contents": [
      { "key": "confirmation", "valueMap": [
        { "key": "message", "valueString": "GitHub issue created successfully!" }
      ] }
    ]
  } }
]
---END CONFIRMATION_EXAMPLE---
"""
