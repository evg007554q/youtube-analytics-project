import json
import os
from googleapiclient.discovery import build

import isodate
# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        # - id канала id
        # - название канала snippet/title
        # - описание канала snippet/description
        # - ссылка на канал snippet/thumbnails/default/url
        # - количество подписчиков statistics/subscriberCount
        # - количество видео statistics/videoCount
        # - общее количество просмотров statistics/viewCount
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title'] # MoscowPython
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriberCount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.viewCount = channel['items'][0]['statistics']['viewCount']

    # HW3
    def __str__(self):
        return f'{self.title} ({self.url})'
    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)
    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)
    # ><>=<=
    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)
    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)
    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)
    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        # print(channel['items'][0]['snippet']['title'])
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self,file_name):
        for_file_channel = {}
        for_file_channel['channel_id'] = self.__channel_id
        for_file_channel['title'] = self.title
        for_file_channel['description'] = self.description
        for_file_channel['url'] = self.url
        for_file_channel['video_count'] = self.video_count
        for_file_channel['viewCount'] = self.viewCount
        for_file_channel['subscriberCount'] = self.subscriberCount

        # print(for_file_channel)
        with open(file_name,'w') as file_json:
            json.dump(for_file_channel,file_json)

