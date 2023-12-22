import os
import time
from Google_API_Functions import *
from models import Album, album_constructor, sort_albums_by_title

def init_library(token):
    # Gets list of Albums and Media items in library. Creates them into objects for easy reference.
    albums = album_constructor(list_albums(token))
    return albums


def list_files_in_folder(folder_path):
    """
    Generate file paths from a folder.

    Args:
    - folder_path (str): The path to the folder.

    Yields:
    - str: File path.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            yield os.path.join(root, file)


def upload_media_process(token, folder_path, albums):
    upload_token_queue = []
    current_batch = []
    counter = 0
    # Gather all the items in the folder and create upload tokens for them.
    for file in list_files_in_folder(folder_path): #TODO Allow this to run in paralel for faster processing.
        print(f"Adding {file} to the upload queue...   {len(upload_token_queue)}")
        upload_token_queue.append(upload_photo(token, file))

    # If the upload queue has items in it, begin to put them into the current batch.
    while len(upload_token_queue) > 0:
        # Populate current_batch up to 50 items
        while len(current_batch) < 50 and len(upload_token_queue) > 0:
            current_batch.append(upload_token_queue.pop())

        try:
            counter += 1
            print("Select which album you want to upload these photos to:")
            for album in sort_albums_by_title(albums):
                print(str(album.title + " --- " + str(album.quid)))

            album_selection = int(input("Enter the nunber of the album in the list above. Enter 0 to upload without an album:   \n\n\n"))
            for album in albums:
                if album_selection == album.quid:
                    album_selection = album.id
            if album_selection == 0:
                album_selection = None

            response_data = create_media_item(token, current_batch, album_id=album_selection, description="") #TODO: Allow the user to select an album. Create objects from API data for easy list and access.
            # If rate limit exceeded, wait 30 seconds and add the failed token to the end of the list.
            if 'error' in response_data and response_data['error'].get('code') == 429:
                print("Rate limit exceeded! \n"
                      "Waiting 30 seconds...")
                time.sleep(30)
                current_batch.append(upload_token)
                continue

            media_item_data = response_data["newMediaItemResults"][0]
            # print(media_item_data['status']['message'])
            print(f"\nItem Created! URL: {media_item_data['mediaItem']['productUrl']}")
        except KeyError as e:
            print(response_data)
        print(f"\nBatch completed. Media items created: {len(current_batch)}")
        print(f"\n{len(upload_token_queue)} items left to upload. Continuing upload process in 3 seconds...")
        current_batch.clear() # Resets List
        time.sleep(3)
    print("Upload Complete!")
    # print(f"Debug!"
    #       f"Items created: {counter}")





def main():

    token = get_google_oauth2_token()
    albums = init_library(token)

    folder_path = "photo_upload"

    all_descriptions = set()

    #Main Function That Allows User Input
    print("\n\nAhoy! Welcome to the NPM Image Management Tool. This is your Captain speaking.\n"
          "\nPlease let Nick know about any weird happenings.\n"
          "\nFinally, please use at your own risk. Operations made by this app cannot be easily reversed.\n")

    while True:
        print("Here are your options. Enter 'q' to quit. \nPlease enter the number you wish to select:\n"
              "1. List Albums\n"
              "2. Create Album\n"
              "3. Change Photo Descriptions\n"
              "4. Move Photos\n"
              "5. Upload Photos\n")
        user_selection = input("Make your selection:   ").lower()
        if user_selection == "1":
            print(f"I have found {len(albums)} albums:\n")
            for album in albums:
                print(f"Title: {album.title}\n Id: {album.id}\n")
            print("\n\n")
            continue
        if user_selection == "2":
            title = input("Enter the name of the album:     ")
            create_album(token, title)
            # After the new album is created, app clears the existing album object library and re-initializes them.
            print("Album Created! Re-initializing library...")
            if albums is not None:
                albums.clear()
            albums = init_library(token)
            continue
        if user_selection == "3":
            photos_to_be_changed = []

            # Fetch all media items from the library only if we haven't done that already
            if not all_descriptions:
                print("Getting all photo descriptions for the library...")
                photos, all_descriptions, _ = list_items_in_library(token, all_descriptions)

            print("I have found the following descriptions:\n")
            for desc in all_descriptions:
                print(desc)

            identifier = input(
                "\nFirst, input the description identifer string. This string will be used to identify all of the photos you want changed based on their description."
                "\nPlease be specific:     ")

            # Filter photos based on the identifier in their description
            photos_to_be_changed = [photo["id"] for photo in photos if
                                  'description' in photo and identifier.strip() in photo[
                                      'description'].strip()]

            #Converts to set to dedupe.
            photos_to_be_changed = set(photos_to_be_changed)
            photos_to_be_changed= list(photos_to_be_changed)

            print("Debug photo ID's:", photos_to_be_changed)
            print(f"I have found {len(photos_to_be_changed)} photos that will be changed.\n\n")

            desc_selection = input("Type the new description you would like to use:     ")

            for photo in photos_to_be_changed:
                update_media_item(token, photo, desc_selection)
            print("Process complete!")
            continue
        if user_selection == "4":
            photos_to_be_moved = []

            # Fetch all media items from the library only if we haven't done that already
            if not all_descriptions:
                print("Getting all photo descriptions for the library...")
                photos, all_descriptions, _ = list_items_in_library(token, all_descriptions)

            print("I have found the following descriptions:\n")
            for desc in all_descriptions:
                print(desc)

            identifier = input(
                "\nFirst, input the description identifer string. This string will be used to identify all of the photos you want changed based on their description."
                "\nPlease be specific:     ")

            # Fetch all media items from the library
            print("Getting Albums...")
            photos, all_descriptions, _ = list_items_in_library(token, all_descriptions)

            # Filter photos based on the identifier in their description
            photos_to_be_moved = [photo["id"] for photo in photos if
                                  'description' in photo and identifier.strip() in photo[
                                      'description'].strip()]

            #Converts to set to dedupe.
            photos_to_be_moved = set(photos_to_be_moved)
            photos_to_be_moved = list(photos_to_be_moved)

            print("Debug photo ID's:", photos_to_be_moved)
            print(f"I have found {len(photos_to_be_moved)} photos that will be moved.\n\n")

            for album in sort_albums_by_title(albums):
                print(str(album.title + " --- " + str(album.quid)))
            album_selection = input("Select the album number you want to send these photos to:     ")

            for album in albums:  # Cycles through albums. If the user selection equals one of the albums, get its ID.
                if album_selection == str(album.quid):
                    album_selection = album.id
            if len(album_selection) < 3:  # Checks to see if the album selection has been converted to ID. If it hasn't, then the input was invalid.
                print("Invalid selection. Returning to Main Menu...")
                continue

            # Add all album ids to a list UNLESS they contain a certain string.
            print("Removing photos...")
            purged_albums = [album for album in albums if
                             "do not" not in album.title.lower() and album.id != album_selection]

            for album in purged_albums:
                response = remove_item_from_album(token, photos_to_be_moved, album.id)
                if response == 200:
                    print(f"Removed photos from {album.title}")
                else:
                    print(f"Error occurred or {album.title} does not contain target photo.")
                # Wait to avoid Rate Limit Error
                time.sleep(2)

            print("Moving photos...")
            add_item_to_album(token, photos_to_be_moved, album_selection)
            purged_albums.clear()
            continue

        if user_selection == "5":
            print("Upload Module Selected. Scanning for files in default path...")
            upload_media_process(token, folder_path, albums)
            continue

        if user_selection == "q":
            break
        else:
            print("Invalid Selection. Please try again.")



if __name__ == '__main__':

    browser_upload_file_id = 'AGs0phJpnLQJqo72HbmhE4JRJCEJ218sCVicFNPo4EvgZYavRaf8rEGl3BEbjzBA2NVmcuXMTHdgmTq-c8bH0O3aFw0fySz6WQ'
    app_upload_file_id = 'AGs0phJMF1EMdvUKhcTiBfBZGfVhAd_Gps1vsdUpQJQizYhfiQO24kKoVX3j7J5mZlpKmWZ1QWq_Nqlm6YKZDYFIrDRQYEOFOg'
    test_album_id = "AGs0phL0B6WWin3WsWP760kK6xcuu_JB8LRDnn832buuPjCMGm7pkM6t_oZTdRSspktwCO6dWy9k"
    update_data = {
        "description": "TEST"
    }
    # token = get_google_oauth2_token()
    # print("Bearer token:", token)
    # albums = list_albums(token)
    # lib_items = list_items_in_library(token)
    # print(albums)
    # print(lib_items)
    # print(get_media_item(token, digiKam_upload_file_id))
    # print(update_media_item(token, app_upload_file_id, update_data))

    # Using the functions
    folder_path = "photo_upload"
    # upload_token = upload_photo(token, file_path)
    # if upload_token:
    #     print(create_media_item(token, upload_token))

    # create_album(token, "TEST ALBUM")
    #
    # add_item_to_album(token, app_upload_file_id, test_album_id)

    # upload_media_process(folder_path)
    main()