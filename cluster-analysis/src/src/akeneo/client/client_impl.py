from __future__ import annotations

from http.client import responses

import requests
import requests.auth

from .bearerauth import BearerAuth
from .client import Client, JsonBody
from .route import PathVars, RestMethods, Route


class ClientImpl(Client):
    def __init__(
        self, host: str, client_id: str, secret: str, username: str, password: str
    ) -> None:
        self._host = host
        self._client_id = client_id
        self._secret = secret
        self._username = username
        self._password = password

        self._token_path, self._routes_dict = self._get_routes()
        self._auth_init()

    # interface ----------------------------------------------------------------

    def get_routes(self) -> list[Route]:
        return list(self._routes_dict.values())

    def request(
        self,
        route_id: str,
        path_vars: PathVars = None,
        body: JsonBody = None,
        params: dict = None,
    ) -> JsonBody:
        route = self._routes_dict[route_id]
        url = f"{self._host}{route.make_path(path_vars)}"

        if route_id[-5:] == "_list":
            assert route.method != "PATCH", "patch list is not implemented yet"
            return self._get_list(url, params)

        res = self._request(route.method, url, params, body)

        if route.method == "GET":
            res.raise_for_status()
            return res.json()

        try:
            return res.json()
        except:
            return {
                "status": res.status_code,
                "message": responses.get(res.status_code, "unknown"),
            }

    # rest methods -------------------------------------------------------------

    def _get_routes(self) -> tuple[str, dict[str, Route]]:
        res = requests.get(f"{self._host}/api/rest/v1")
        assert res.status_code == 200, f"Wrong host: {self._host}"

        res_body = res.json()

        token_path = res_body["authentication"]["fos_oauth_server_token"]["route"]

        res_routes: dict[str, dict] = res_body["routes"]
        routes = {}
        for (route_id, route_details) in res_routes.items():
            path = route_details["route"]
            method = route_details["methods"][0]
            route = Route(route_id, path, method)
            routes[route_id] = route

        return token_path, routes

    def _post_auth(self, req_body: dict) -> tuple[str, str]:
        auth = requests.auth.HTTPBasicAuth(self._client_id, self._secret)

        res = requests.post(f"{self._host}{self._token_path}", req_body, auth=auth)
        res.raise_for_status()

        res_body = res.json()

        return res_body["access_token"], res_body["refresh_token"]

    def _request(
        self, method: RestMethods, url: str, params: dict = None, body: JsonBody = None
    ) -> requests.Response:
        auth = BearerAuth(self._token_access)

        res = requests.request(method, url, params=params, json=body, auth=auth)
        if res.status_code == 401:
            self._auth_refresh()
            res = requests.request(method, url, params=params, json=body, auth=auth)

        return res

    # --------------------------------------------------------------------------

    def _auth_init(self) -> None:
        req_body = {
            "username": self._username,
            "password": self._password,
            "grant_type": "password",
        }
        self._token_access, self._token_refresh = self._post_auth(req_body)

    def _auth_refresh(self) -> None:
        try:
            req_body = {
                "refresh_token": self._refresh_token,
                "grant_type": "refresh_token",
            }
            self._token_access, self._token_refresh = self._post_auth(req_body)
        except:
            self._auth_init()

    def _clean_list_items(self, items: list[dict]):
        for i in range(len(items)):
            del items[i]["_links"]

    def _get_list(self, url: str, params: dict = None) -> list[dict]:
        result = []

        params_ = {}
        if params:
            params_ = params.copy()
        params_["page"] = 1
        params_["limit"] = 100

        has_next = True

        while has_next:
            res = self._request("GET", url, params_).json()

            items = res["_embedded"]["items"]
            self._clean_list_items(items)
            result.extend(items)

            if "next" in res["_links"]:
                params_["page"] += 1
            else:
                has_next = False

        return result

    def _clean_list_items(self, items: list[dict]):
        for i in range(len(items)):
            del items[i]["_links"]
