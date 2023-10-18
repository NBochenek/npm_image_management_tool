import requests
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Load client secrets from your OAuth 2.0 credentials file
# This file is downloaded from Google Cloud Console when creating OAuth 2.0 credentials
CLIENT_SECRETS_FILE = "oauth_client_credentials.json"

# Set the scope you need for the API you're accessing
SCOPES = ['https://www.googleapis.com/auth/photoslibrary', "https://www.googleapis.com/auth/photoslibrary.appendonly",
          "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
          "https://www.googleapis.com/auth/photoslibrary.readonly",
          "https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata",
          "https://www.googleapis.com/auth/photoslibrary.sharing"]


def get_google_oauth2_token():
    creds = None

    # Try to load existing creds from file
    try:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    except FileNotFoundError:
        pass

    # If the credentials are invalid or do not exist, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds.token


def create_album(token, title):
    # Set the URL and headers
    url = f"https://photoslibrary.googleapis.com/v1/albums"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Data payload for the POST request
    data = {
        "album": {
            "title": title
        }
    }

    # Make the POST request with the specified body
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")

def list_albums(token):
    # Set the URL and headers
    url = "https://photoslibrary.googleapis.com/v1/albums"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")


def list_items_in_library(token, all_descriptions, page_size=100, page_token=None):
    # Set the URL and headers
    url = "https://photoslibrary.googleapis.com/v1/mediaItems"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Set the query parameters
    params = {
        "pageSize": page_size
    }
    if page_token:
        params["pageToken"] = page_token

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()

        media_items = response_data['mediaItems']
        print(f"{len(media_items)} media items found in this batch.")

        if media_items:
            #If any items in the batch contains a description, it is added to a set.
            get_media_details(media_items, all_descriptions)
        else:
            print("No media items found or an error occurred.")

        # If there's a nextPageToken, fetch the next page of results
        if 'nextPageToken' in response_data:
            next_page_media_items, all_descriptions, _ = list_items_in_library(token, all_descriptions, page_size, response_data['nextPageToken'])
            media_items.extend(next_page_media_items)

        return media_items, all_descriptions, None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None, all_descriptions, None


def get_media_item(token, item_id):
    # Set the URL and headers
    url = f"https://photoslibrary.googleapis.com/v1/mediaItems/{item_id}"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")


def update_media_item(token, item_id, new_description):
    # Set the base URL and target URL
    base_url = "https://photoslibrary.googleapis.com/v1/mediaItems/"
    url = f"{base_url}{item_id}"

    # Set the headers for the request
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Define the new description data
    # The body should directly contain the fields to be updated.
    update_data = {
        "description": new_description
    }

    # Define the query parameters
    # 'updateMask' should be specified as a query parameter, not in the body of the request.
    params = {
        "updateMask": "description"
    }

    # Make the PATCH request
    response = requests.patch(url, headers=headers, json=update_data, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")


def add_item_to_album(token, item_ids, album_id):
    # Set the URL and headers
    url = f"https://photoslibrary.googleapis.com/v1/albums/{album_id}:batchAddMediaItems"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Data payload for the POST request
    data = {
        "mediaItemIds": item_ids
    }

    # Make the POST request with the specified body
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")


def remove_item_from_album(token, item_ids, album_id):

    # Set the URL and headers
    url = f"https://photoslibrary.googleapis.com/v1/albums/{album_id}:batchRemoveMediaItems"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Data payload for the POST request
    data = {
        "mediaItemIds": item_ids
    }

    # Make the POST request with the specified body
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")
        print("This error may have occurred because the album was empty.")
        # print(f"Debug: {data}")


def upload_photo(token, file_path):
    # Step 2: Upload byte content
    url = "https://photoslibrary.googleapis.com/v1/uploads"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-type": "application/octet-stream",
        "X-Goog-Upload-Protocol": "raw",
        "X-Goog-Upload-File-Name": file_path.split('/')[-1]
    }

    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, data=file)

    if response.status_code == 200:
        return response.text  # This is the upload token
    else:
        print(f"Error uploading photo: {response.text}")
        return None


def create_media_item(token, upload_tokens_list, album_id=None, description=None):  #TODO Reconfigure this to loop through upload tokens, creating a new newMediaItems entry for each.
    # Step 3: Create a media item
    url = "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-type": "application/json"
    }

    body = {
        "newMediaItems": [
            {
                "description": description,
                "simpleMediaItem": {
                    "uploadToken": token
                }
            } for token in upload_tokens_list
        ]
    }

    if album_id:
        body["albumId"] = album_id

    response = requests.post(url, headers=headers, json=body)
    return response.json()


def get_media_details(media_items, input_set):
    """
    Print details of each media item.

    Args:
    media_items (list of dict): A list of dictionaries, each representing a media item.
    """

    for item in media_items:
        # print(f"ID: {item.get('id')}")
        # print(f"Product URL: {item.get('productUrl')}")
        # print(f"Base URL: {item.get('baseUrl')}")
        # print(f"MIME Type: {item.get('mimeType')}")
        # print(f"Filename: {item.get('filename')}")

        # # Extracting and printing media metadata information
        # media_metadata = item.get('mediaMetadata', {})
        # creation_time = media_metadata.get('creationTime')
        # width = media_metadata.get('width')
        # height = media_metadata.get('height')
        #
        # print(f"Created: {creation_time}")
        # print(f"Dimensions: {width} x {height}")

        # If there's a description, add it to the input set.
        if 'description' in item:
            input_set.add(item['description'])
            # print(f"Description Found: {item['description']}")

        # print("\n")  # Print a new line for readability
    return input_set


if __name__ == '__main__':
    token = get_google_oauth2_token()
    album_id = "AGs0phJrJo1E4a7jrjcLWBSD30QD5pHXM6LtUuX4DBbjd0t7eeZ4r3cdeochoeBCJwMy84m9eomZ"
    photo_ids = ['AGs0phJIFoYVEPJAgZKgNNALKCfpmwMuUYVRaWMAxMjNIB_mpYJczS_AYv8auopLzRVblbo1NVD7j7CWXImhQcLjPLONtqOibw',
                 'AGs0phKDn_Fz64RN9GHApBSJUSBnNiclS8REYC8Mobgv-L19tOsae-WFjgAlnO2sNh9GmB9FyHZZ59CjBCY08F1YpAF_sjJlfQ',
                 'AGs0phK7Sl_F8G76yqAU4DiT8wXWsU3CmsDjPSzRCajpIb3P-voN7V6y-JvpF3M3A2vuGH75ozAm9iOYOIl4tRxQhU8EIxTmrQ',
                 'AGs0phJMkSFrfn_xysxU5B9KF4p9YBhsdcs-vyj8tLQeCzU5u4FMGzaSzfLZCHl0pZOSEAJ2v0-LPmnYgP_LI1Eq2YuBLd5VGw']

    update_media_item(token, photo_ids[0], "changed description")