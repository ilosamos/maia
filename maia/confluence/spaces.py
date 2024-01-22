"""This module contains functions to interact with Confluence spaces"""
# See ref: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-spaces-id-pages-get
import json
import logging

import requests
from requests.auth import HTTPBasicAuth

from settings import (CONFLUENCE_API_EMAIL, CONFLUENCE_API_TOKEN,
                      CONFLUENCE_BASE_URL)

auth = HTTPBasicAuth(CONFLUENCE_API_EMAIL, CONFLUENCE_API_TOKEN)

def get_space_by_key(key):
    """Returns a space by its key"""
    url = f"{CONFLUENCE_BASE_URL}/wiki/api/v2/spaces"

    headers = {
      "Accept": "application/json"
    }

    params = {
        "keys": key
    }

    response = requests.request(
       "GET",
       url,
       headers=headers,
       auth=auth,
       params=params,
       timeout=5
    )

    return json.loads(response.text)    

def list_all_pages(space_id="198279170"):
    """Returns all pages in a space"""
    logging.info("Getting all pages in space %s", space_id)

    url = f"{CONFLUENCE_BASE_URL}/wiki/api/v2/spaces/{space_id}/pages"
    params = { 
        'id': space_id, 
        'limit': 50
    }
    results = get_pages(url, params)

    logging.info("Found %d pages in space %s", len(results), space_id)

    fields_to_keep = ['_links', 'createdAt', 'id', 'title']

    # file fields_to_keep for results array
    results = [{ key: value for key, value in item.items() if key in fields_to_keep } for item in results]

    # remap fields to make it more readable for AI
    return [{ 'id': item['id'], 
             'title': item['title'], 
             'url': f"{CONFLUENCE_BASE_URL}/wiki{item['_links']['webui']}", 
             'dateCreated': item['createdAt']
            } for item in results]


def get_pages(url, params=None, results=None):
    """Returns all pages in a space"""
    headers = { "Accept": "application/json" }

    if results is None:
        results = []

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=params,
       auth=auth,
       timeout=5
    )

    if response.status_code == 200:
        response = json.loads(response.text)
        results.extend(response['results'])

        if 'next' in response['_links']:
            get_pages(f"{CONFLUENCE_BASE_URL}{response['_links']['next']}", params=params, results=results)

    return results

def get_page_content(page_id):
    """Returns the content of a page"""
    url = f"{CONFLUENCE_BASE_URL}/wiki/api/v2/pages/{page_id}"
    headers = { "Accept": "application/json" }
    storage_format = "view"
    params={ "body-format": storage_format }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params,
        auth=auth,
        timeout=5
    )

    return json.loads(response.text)['body'][storage_format]['value']