import encodings
import hashlib
import json

import requests
from requests.exceptions import ConnectionError, HTTPError

BASE_URL = 'http://0.0.0.0:8888'
UTF_8 = encodings.utf_8.getregentry().name

def get_auth_token() -> str: 
    """
    Retrieves authentication token.

    Returns:
    str: authentication token

    """
    url = ''.join([BASE_URL, '/auth'])
    response = retry(url)
    auth_token = response.headers['Badsec-Authentication-Token']
    return auth_token

def get_checksum(auth_token:str, endpoint:str) -> str:
    """
    Generates hash.

    Parameters:
    auth_token: authentication token
    endpoint: URL endpoint including the forward slash

    Returns:
    str: HEX string of hash

    """
    content = ''.join([auth_token, endpoint])
    encoded = content.encode(UTF_8)
    hash = hashlib.sha256(encoded)
    checksum = hash.hexdigest()
    return checksum

def get_users(checksum:str) -> str:
    """
    Retrieves users.

    Parameters:
    checksum: Hex string of hash

    Returns:
    str: content of requests.Response() in Unicode
    """
    url = ''.join([BASE_URL, '/users'])
    headers = {'X-Request-Checksum': checksum}
    response = retry(url, headers)
    users = response.text
    return users

def formatted(text:str) -> str:
    """
    Formats input into JSON.

    Parameter:
    text: content as string

    Returns:
    str: JSON formatted input
    """
    split = text.splitlines()
    jsonified = json.dumps(split)
    return jsonified

def get_noclist() -> str:
    """
    Retrieves NOC list.
    """
    auth_token = get_auth_token()
    checksum = get_checksum(auth_token, '/users')
    users = get_users(checksum)
    noclist = formatted(users)
    print(noclist)
    exit(0)

def retry(url:str, headers=None) -> requests.Response:
    """
    Retries request three times maximum.

    Parameters:
    url: request URL
    headers: request headers

    Returns:
    requests.Response: request response

    """
    max_tries = 3
    tries = 0
    try:
        while (tries < max_tries):
            tries += 1 
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == requests.codes.ok:
                    return response
            except ConnectionError:
                continue
    except HTTPError:
        exit(1)

if __name__ == '__main__':
    get_noclist()
