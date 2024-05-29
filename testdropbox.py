import sqlite3
import time
import dropbox
import requests
from CourseProject import settings

# conn = sqlite3.connect("db.sqlite3")
#
# def insert_presentation(conn, name, modified, link):
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO maindb_presentation (title, time, link, author, rating, 'group', notes) "
#         "SELECT ?, ?, ?, 'Dropbox','Не перевірено','?','Не має' "
#         "WHERE NOT EXISTS "
#         "(SELECT 1 FROM maindb_presentation WHERE title = ? AND time = ?)",
#         (name, modified, link, name, modified)
#     )
#     conn.commit()
#

access_token = None
expires_at = 0


def get_access_token(refresh_token, app_key, app_secret):
    global access_token, expires_at

    if expires_at - time.time() < 3600:
        url = 'https://api.dropboxapi.com/oauth2/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': app_key,
            'client_secret': app_secret
        }
        response = requests.post(url, data=data)
        response_data = response.json()
        access_token = response_data.get('access_token')
        expires_at = time.time() + response_data.get('expires_in')
        print("new token")
        return access_token
    if access_token and expires_at > time.time():
        print("token is ok")
        return access_token


get_access_token(settings.REFRESH_TOKEN, settings.APP_KEY, settings.APP_SECRET)

# dbx = dropbox.Dropbox(access_token)
# for entry in dbx.files_list_folder("/presentation").entries:
#     print(entry.name)
#     print(entry.server_modified)
#
#     file_path = entry.path_display
#     insert_presentation(conn, entry.name, entry.server_modified,
#                         '')
#
# dbx.close()


