import json
import os
from googleapiclient.discovery import build

import isodate
# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)
print(api_key)

def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Video:
    def __init__(self,video_id):

        self.video_id = video_id
        self.url = 'https://youtu.be/' + video_id


        # вынесено в отдельную функцию
        # self.title = video_response['items'][0]['snippet']['title']
        # self.viewCount = video_response['items'][0]['statistics']['viewCount']
        # self.likeCount = video_response['items'][0]['statistics']['likeCount']
        # self.duration = video_response['items'][0]['statistics']['likeCount']

        self.set_attributes_video()

    def __str__(self):
        return f'{self.title}'

    def set_attributes_video(self):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()

        self.title = video_response['items'][0]['snippet']['title']
        self.viewCount = video_response['items'][0]['statistics']['viewCount']
        self.likeCount = video_response['items'][0]['statistics']['likeCount']
        self.duration = video_response['items'][0]['statistics']['likeCount']

class PLVideo(Video):
    def __init__(self, video_id, channel_id):
        super().__init__(video_id)
        self.channel_id = channel_id


