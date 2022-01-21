import requests
import requests.auth

from .bearerauth import BearerAuth
from .client import Client, JsonBody
import akeneo.models as models


class ClientImpl(Client):

    def __init__(self, host: str, client_id: str, secret: str, username: str, password: str) -> None:
        super().__init__()
        self._assign(host, client_id, secret, username, password)
        self._init_routes()
        self._auth_init()

    # interface ----------------------------------------------------------------

    def get_routes(self) -> list[models.Route]:
        return self._routes

    def get(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> JsonBody:
        url = self._get_url(route_id, path_vars)
        return self._get(url, params)

    def get_list(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> list[dict]:
        assert self._get_route(route_id).is_list, f"Passed route is not a list"
        url = self._get_url(route_id, path_vars)

        result = []

        params_ = {}
        if params:
            params_ = params.copy()
        params_["page"] = 1
        params_["limit"] = 100

        has_next = True

        while has_next:
            res = self._get(url, params_)

            items = res["_embedded"]["items"]
            self._clean_list_items(items)
            result.extend(items)

            if "next" in res["_links"]:
                params_["page"] += 1
            else:
                has_next = False

        return result

    # init ---------------------------------------------------------------------

    def _assign(self, host: str, client_id: str, secret: str, username: str, password: str) -> None:
        self._host = host
        self._client_id = client_id
        self._secret = secret
        self._username = username
        self._password = password

    def _init_routes(self) -> None:
        res = requests.get(f"{self._host}/api/rest/v1")
        assert res.status_code == 200, f"Wrong host: {self._host}"

        res_body = res.json()

        token_path = res_body["authentication"]["fos_oauth_server_token"]["route"]
        self._token_url = f"{self._host}{token_path}"

        res_routes: dict[str, dict] = res_body["routes"]
        routes: list[models.Route] = []
        for (route_id, route_details) in res_routes.items():
            path = route_details["route"]
            method = route_details["methods"][0]
            route = models.Route(route_id, path, method)
            routes.append(route)
        self._routes = routes

    # auth ---------------------------------------------------------------------

    def _auth(self, req_body: dict):
        auth = requests.auth.HTTPBasicAuth(self._client_id, self._secret)

        res = requests.post(self._token_url, req_body, auth=auth)
        res.raise_for_status()

        res_body = res.json()

        self._access_token = res_body["access_token"]
        self._refresh_token = res_body["refresh_token"]

    def _auth_init(self):
        req_body = {
            "username": self._username,
            "password": self._password,
            "grant_type": "password"
        }
        self._auth(req_body)

    def _auth_refresh(self):
        req_body = {
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token"
        }
        self._auth(req_body)

    # util ---------------------------------------------------------------------

    def _clean_list_items(self, items: list[dict]):
        for i in range(len(items)):
            del items[i]["_links"]

    def _get(self, url: str, params: dict = None) -> JsonBody:
        auth = BearerAuth(self._access_token)

        res = requests.get(url, params, auth=auth)
        if res.status_code == 401:
            self._auth_refresh()
            res = requests.get(url, params, auth=auth)
        res.raise_for_status()

        return res.json()

    def _get_route(self, route_id: str) -> models.Route:
        for route in self._routes:
            if route.id == route_id:
                return route
        raise ValueError("passed route_id unknown")

    def _get_url(self, route_id: str, path_vars: dict[str, str] = None) -> str:
        route = self._get_route(route_id)
        return f"{self._host}{route.make_path(path_vars)}"
