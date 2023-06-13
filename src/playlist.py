import json
import os
from googleapiclient.discovery import build

import isodate
# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')
# print(api_key)

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class PlayList:
    # title: object

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        self.__total_duration = None
        self.__show_best_video = None
        self.video_ids = None
        self.title = None
        # playlist_y = youtube.playlists().list(id=playlist_id,
        #                                       part='contentDetails,snippet',
        #                                       maxResults=50,
        #                                       ).execute()
        self.set_attributes_playlist()

    def set_attributes_playlist(self):
        playlist_id = self.playlist_id

        playlist_y = youtube.playlists().list(id=playlist_id,
                                              part='contentDetails,snippet',
                                              maxResults=50,
                                              ).execute()

        # self.title = playlist_y['items'][0]['snippet']['title']

        playlist_y = youtube.playlistItems().list(playlistId=playlist_id,
                                                  part='contentDetails,snippet',
                                                  maxResults=50,
                                                  ).execute()

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_y['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()

        duration = isodate.parse_duration('PT0M0S')
        best_like_count = 0
        self.__show_best_video = ''

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
            # print(type(duration))
            like_count = int(video['statistics']['likeCount'])
            if like_count > best_like_count:
                self.__show_best_video = video['id']
                best_like_count = like_count
                # print(type(self.__show_best_video) )

        self.__total_duration = duration

    @property
    def total_duration(self):
        return self.__total_duration

    # @property
    def show_best_video(self):
        return 'https://youtu.be/' +  self.__show_best_video
