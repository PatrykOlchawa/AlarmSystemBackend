from api.auth_service import auth_service
from api.config_service import config_service
from storage.config_store import config_store

def main():
    print("Loggin in...")

    auth_service.login()

    print("Downloading configuration")

    config = config_service.get_config()

    config_store.save(config)

    print(config_store.load())

if __name__ == '__main__':
    main()