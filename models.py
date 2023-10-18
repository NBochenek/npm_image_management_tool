class Album:
    def __init__(self, id, quid, title, url, writeable, coverPhotoUrl):
        self.id = id
        self.quid = quid
        self.title = title
        self.url = url
        self.writeable = writeable
        self.coverPhotoUrl = coverPhotoUrl

class Photo:
    def __int__(self):
        pass


def album_constructor(album_data):
    objects = []
    count = 1
    try:
        for result in album_data["albums"]:
            id = result["id"]
            quid = count
            title = result["title"]
            url = result["productUrl"]
            writeable = bool(result.get("isWriteable", True))
            coverPhotoUrl = result["coverPhotoBaseUrl"]
            album = Album(id, quid, title, url, writeable, coverPhotoUrl)
            objects.append(album)
            count += 1
        return objects
    except KeyError as e:
        print("No albums found.")

if __name__ == '__main__':
    test = {
      'albums': [
        {
          'id': 'AGs0phJbzLUb9C7CgpT4zdOpCFWGnt4dOHVBfODmA9pblgXQ5tMz8eYHHlWWFx_Cj4RBZQ_jqIA6',
          'title': 'TEST ALBUM',
          'productUrl': 'https://photos.google.com/lr/album/AGs0phJbzLUb9C7CgpT4zdOpCFWGnt4dOHVBfODmA9pblgXQ5tMz8eYHHlWWFx_Cj4RBZQ_jqIA6',
          'isWriteable': True,
          'coverPhotoBaseUrl': 'https://lh3.googleusercontent.com/lr/AAJ1LKduJ-amiPJpJqt6fzn5Me23MQD9_Rqs18Y21MfqMdvxaH-ZJc0Yz9LQscqT7ip0AsFgGT8tE-W3cHg6p9UGYpTH83ySEaeUDQeP472qS4XId2OUjXfsCwEFZDHzPtjAxXvhvmxBYQSn5Fp9Yn82A-xLTDZuTanH61pKbQIzJB5wM_5y5_9Jf5cwIx5w4DehnuVODtEb4yDlUfTj0FImh7zUoIegA2gncSJ0nuVAMxEfvhTABAATu2PJ9HSdD95RU8z0HyM2AOED7tQZ5UfXTVLHKjM8onsospiL3SACVxuWJBIHzaiCqEvC2o2LOGiYmmG3OBpp4kegIhtydTbcQ8otEVPbVA-A8TC-ha5QcPyRyR5q40oP9ZOtzA2_Se_X63H0NphqfFLSr0JrbnWivKT0aplSAHOD5rPMl3BnVQD-bNdFZieSSM3nO4KTgtmVp8SYkmwoN-_LsGKH3OhFzcSUOHhCgcrsFSjGZDbiTAkxSHtHClJ5ZBr873KoM5n-BktyUMq36Zdqe6fDFExgQsakqLJGax9LvHXKM00rSwJmwJQv0Zj_WAENts7tdq9mmcZx5ezRcVT9q83h5AJFaXYOrc3No6YHbzoeIusxUGftJwv-YEgXE8ZFGPn8n4bWuwYfANmfZxz7B-cvqFi4-1wwXnXSbJPYEfRch8veicdnBW8twQSXU2t7P_5yC515mM2uT6XgC0pelJj2saQRYz_g5XktUtejJgtGT9mpL6JcGolVo0rDfxuFpXPZVw0ArvLqCJy1MiavuSMsxlnOUAIXjCr0--53G4y6UXaddRWvOXpxcmdNle_HnxlZXOL0Yb9atGSN5eXJkNMCR8mXhNRQB3dazZOrmY128d53wDCgrBFrj963E5eH9EtdWWqReiNtYvcBHz6EzfbJN3Tq0aO46rWS_aFkBqB6L7r4zjgJY3gmk6K_D4Ug47B1B04i9I1abw6pHJylTTeJnLUJ7a79AaMtwe_BdNDlj2EcC_vSBf38rzERVJoLBr7G_AN4yT-rq7nijOE2M4jdVKEEb94D5ZGVNCFmeFBrSKc5AEnwQyhJpYDMYu6K9-dhgMHUMQQGZYZa'
        }
      ]
    }
    albums = album_constructor(test)
    print(albums[0].title)
    print(albums[0].url)

