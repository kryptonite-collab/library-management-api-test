import json as json_lib
from urllib.parse import urljoin
from typing import Optional

import allure
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
        request_url = self._build_url(path)
        self._attach_request(method, request_url, request_headers, params, json)

        response = requests.request(
            method=method,
            url=request_url,
            headers=request_headers,
            params=params,
            json=json,
            timeout=timeout or self.timeout,
        )
        response_body = self._parse_body(response)
        self._attach_response(response.status_code, response_body, response.text)

        return {
            "status_code": response.status_code,
            "body": response_body,
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

    def _attach_request(
        self,
        method: str,
        url: str,
        headers: dict,
        params: Optional[dict],
        body: Optional[dict],
    ) -> None:
        allure.attach(
            self._format_json(
                {
                    "method": method.upper(),
                    "url": url,
                    "headers": self._mask_sensitive_headers(headers),
                    "params": params or {},
                    "json": body,
                }
            ),
            name="HTTP Request",
            attachment_type=allure.attachment_type.JSON,
        )

    def _attach_response(
        self,
        status_code: int,
        body,
        text: str,
    ) -> None:
        allure.attach(
            self._format_json(
                {
                    "status_code": status_code,
                    "body": body if body is not None else text,
                }
            ),
            name="HTTP Response",
            attachment_type=allure.attachment_type.JSON,
        )

    @staticmethod
    def _mask_sensitive_headers(headers: dict) -> dict:
        safe_headers = dict(headers)

        for key in list(safe_headers.keys()):
            if key.lower() == "authorization":
                safe_headers[key] = "Bearer ***"

        return safe_headers

    @staticmethod
    def _format_json(data) -> str:
        return json_lib.dumps(data, ensure_ascii=False, indent=2, default=str)
