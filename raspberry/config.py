from dataclasses import dataclass


@dataclass
class Settings:
    api_url: str = "https://api.wsb-alarm.pl"
    client_id = "e31bc6d5-5a76-4542-ab0f-2081abe420e9"
    secret = "F5u9iOCuQaInqbjuFRZESZWuH0dfFol3URkRaGMp4bU"
   # api_url: str = "http://localhost:8000"
 #   client_id: str = "5369ece7-66e0-4187-83c5-cafffb79e8c9"
  #  secret: str = "_mQeo5D2Bq3nCPQIPq222qko8xfKVTmUWJfvWWnOcfiw"


settings = Settings()