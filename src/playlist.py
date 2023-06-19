import json
import os
from googleapiclient.discovery import build

import isodate
# YT_API_KEY скопирован из гугла и вставлен в переменные окружения

class APIMixin:
    api_key: str = os.getenv('YT_API_KEY')
    # print(api_key)

    @classmethod
    def get_service(cls):
        """Объект для работы с API"""
        service = build('youtube', 'v3', developerKey = cls.api_key)
        return service

class PlayList(APIMixin):
    """"""
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self._init_from_api()

    def _init_from_api(self):
        """Получаем данные по API и инициализируем ими экземпляр класса."""
        playlist_id = self.playlist_id
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        playlist_y = self.get_service().playlists().list(id=playlist_id,
                                              part='contentDetails,snippet',
                                              maxResults=50,
                                              ).execute()
        self.title = playlist_y['items'][0]['snippet']['title']
        # self.total_duration()
        # self.show_best_video()

    @property
    def total_duration(self):
        """Возвращает суммарную длительность плей-листа в формате 'datetime.timedelta' (hh:mm:ss))."""
        video_response = self._get_playlist_videos()
        duration = isodate.parse_duration('PT0M0S')
        for video in video_response['items']:
             # YouTube video duration is in ISO 8601 format
             iso_8601_duration = video['contentDetails']['duration']
             duration += isodate.parse_duration(iso_8601_duration)

        # self.__total_duration = duration

        return duration
    def show_best_video(self) -> None:
        """Выводит ссылку на самое залайканое видео в плейлисте."""
        video_response = self._get_playlist_videos()

        best_like_count = 0
        self.__show_best_video = ''

        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > best_like_count:
                self.__show_best_video = video['id']
                best_like_count = like_count
                self.best_like_count = best_like_count
        return 'https://youtu.be/' + self.__show_best_video

    def _get_playlist_videos(self):
        playlist_y = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                   part='contentDetails,snippet',
                                                   maxResults=50,
                                                   ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_y['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                            id=','.join(video_ids)
                                                ).execute()
        return video_response



