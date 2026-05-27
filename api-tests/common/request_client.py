from urllib.parse import urljoin
from typing import Optional

import requests

from common.config import BASE_URL, REQUEST_TIMEOUT


class RequestClient:
    def __init__(self, base_url: str = BASE_URL, timeout: float = REQUEST_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = {}

    def set_token(self, token: str) -> None:
        self.default_headers["Authorization"] = f"Bearer {token}"

    def request(
        self,
        method: str,
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        request_headers = {**self.default_headers, **(headers or {})}
        response = requests.request(
            method=method,
            url=self._build_url(path),
            headers=request_headers,
            params=params,
            json=json,
            timeout=timeout or self.timeout,
        )

        return {
            "status_code": response.status_code,
            "body": self._parse_body(response),
            "text": response.text,
            "headers": dict(response.headers),
        }

    def get(
        self,
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        return self.request("GET", path, headers=headers, params=params, timeout=timeout)

    def post(
        self,
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        return self.request(
            "POST",
            path,
            headers=headers,
            params=params,
            json=json,
            timeout=timeout,
        )

    def put(
        self,
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        return self.request(
            "PUT",
            path,
            headers=headers,
            params=params,
            json=json,
            timeout=timeout,
        )

    def delete(
        self,
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        return self.request(
            "DELETE",
            path,
            headers=headers,
            params=params,
            json=json,
            timeout=timeout,
        )

    def _build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path

        return urljoin(f"{self.base_url}/", path.lstrip("/"))

    @staticmethod
    def _parse_body(response: requests.Response):
        try:
            return response.json()
        except ValueError:
            return None
