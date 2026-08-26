import requests
class MediaMTXClient:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:9997",
    ):
        self.base_url = base_url.rstrip("/")

    def get_paths(
        self,
    ) -> list[str]:
        response = requests.get(
            f"{self.base_url}/v3/config/paths/list",
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        return [
            item["name"]
            for item in data.get("items", [])
        ]
    def get_path_config(
        self,
        path: str,
    ) -> dict:
        response = requests.get(
            f"{self.base_url}/v3/config/paths/get/{path}",
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    def create_path(
        self,
        path: str,
        config: dict,
    ) -> dict:

        response = requests.post(
            f"{self.base_url}/v3/config/paths/add/{path}",
            json=config,
            timeout=5,
        )
        if not response.ok:
            raise RuntimeError(
                f"MediaMTX create path failed: "
                f"status={response.status_code}, "
                f"body={response.text}"
            )

        return response.json()

    def patch_path(
        self,
        path: str,
        config: dict,
    ) -> dict:
        response = requests.patch(
            f"{self.base_url}/v3/config/paths/patch/{path}",
            json=config,
            timeout=5,
        )

        response.raise_for_status()
        return response.json()

    def delete_path(
        self,
        path:str,
    ) -> None:
        response = requests.delete(
            f"{self.base_url}/v3/config/paths/delete/{path}",
            timeout=5,
        )
        response.raise_for_status()

    def path_exists(
        self,
        path:str,
    ) -> bool:
        response = requests.get(
            f"{self.base_url}/v3/config/paths/get/{path}",
            timeout=5,
        )

        if response.status_code == 404:
            return False
        
        response.raise_for_status()

        return True