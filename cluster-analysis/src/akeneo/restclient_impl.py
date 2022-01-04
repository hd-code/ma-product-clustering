import json

import requests
import requests.auth

from akeneo.bearerauth import BearerAuth
from akeneo.restclient import AkeneoRestClient, JsonBody
from akeneo.route import AkeneoRoute


class AkeneoRestClientImpl(AkeneoRestClient):

    @property
    def routes(self) -> list[AkeneoRoute]:
        return self._routes

    def get(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> JsonBody:
        auth = BearerAuth(self._access_token)
        route = self._get_route(route_id)
        url = f"{self._host}{route.make_path(path_vars)}"

        res = requests.get(url, params, auth=auth)
        if res.status_code == 401:
            self._auth_refresh()
            res = requests.get(url, params, auth=auth)

        assert res.status_code == 200, f"Http-Error: {res.status_code}\n{json.dumps(res.json())}"

        return res.json()

    def get_list(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> list[dict]:
        assert self._get_route(route_id).is_list, f"Passed route is not a list"

        result = []

        params_ = {}
        if params:
            params_ = params.copy()
        params_["page"] = 1
        params_["limit"] = 100

        has_next = True

        while has_next:
            res = self.get(route_id, path_vars, params_)
            result.extend(res["_embedded"]["items"])

            if "next" in res["_links"]:
                params_["page"] += 1
            else:
                has_next = False

        return result

    # init ---------------------------------------------------------------------

    def __init__(self, host: str, client_id: str, secret: str, username: str, password: str) -> None:
        super().__init__()
        self._host = host
        self._client_id = client_id
        self._secret = secret
        self._username = username
        self._password = password

        self._init_routes()
        self._auth_init()

    def _init_routes(self) -> None:
        res = requests.get(f"{self._host}/api/rest/v1")
        assert res.status_code == 200, f"Wrong host: {self._host}"

        res_body = res.json()

        token_path = res_body["authentication"]["fos_oauth_server_token"]["route"]
        self._token_url = f"{self._host}{token_path}"

        res_routes: dict[str, dict] = res_body["routes"]
        routes: list[AkeneoRoute] = []
        for (route_id, route_details) in res_routes.items():
            path = route_details["route"]
            method = route_details["methods"][0]
            route = AkeneoRoute(route_id, path, method)
            routes.append(route)
        self._routes = routes

    # auth ---------------------------------------------------------------------

    def _auth(self, req_body: dict):
        auth = requests.auth.HTTPBasicAuth(self._client_id, self._secret)
        res = requests.post(self._token_url, req_body, auth=auth)
        assert res.status_code == 200, f"Http-Error: {res.status_code}\n{json.dumps(res.json())}"

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

    def _get_route(self, route_id: str) -> AkeneoRoute:
        for route in self._routes:
            if route.id == route_id:
                return route
