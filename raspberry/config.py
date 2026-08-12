from dataclasses import dataclass


@dataclass
class Settings:
    api_url: str = "https://api.wsb-alarm.pl"
    client_id = "e31bc6d5-5a76-4542-ab0f-2081abe420e9"
    secret = "NjjEa3BKehIlmn_-Q24U55OCFBBhCtYwDUvNuz-8VQM"
   # api_url: str = "http://localhost:8000"
 #   client_id: str = "1bcd392e-c7e9-4cef-bcad-536d7fe05091"
  #  secret: str = "_mQeo5D2Bq3nCPQIPq222qko8xfKVTmUWJfvWWnOcfiw"


settings = Settings()