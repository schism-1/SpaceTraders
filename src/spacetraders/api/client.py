import requests
import time
from datetime import datetime
from .exceptions import SpaceTradersError, TokenInvalidError, CooldownError

class SpaceTradersClient:
    def __init__(self, token):
        self.base_url = "https://api.spacetraders.io/v2"
        self.headers = {"Authorization": f"Bearer {token}"}
        self.request_delay = 0.5

    def _request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"

        while True:
            response = requests.request(method, url, headers=self.headers, json=data, params=params)

            # Handling rate limiting
            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get("Retry-After", 1))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                continue

            # Handling errors
            if not response.ok:
                error_json = response.json().get('error', {})
                error_code = error_json.get('code')
                message = error_json.get('message', 'Unknown Error')

                # Map error 401 to TokenInvalidError
                if response.status_code == 401:
                    raise TokenInvalidError(message)
                
                # Map error 4000 to cooldown error
                if error_code == 4000:
                    data = error_json.get('data', {})
                    seconds = data.get('cooldown', {}).get('remainingSeconds', 0)
                    raise CooldownError(message, remaining_seconds=seconds)
                
                # If none of these, raise generic SpaceTradersError
                raise SpaceTradersError(message, code=error_code, data=error_json.get('data'))
            
            # Success
            time.sleep(self.request_delay)
            return response.json()
        
    def get_my_ships(self):
        return self._request("GET", "/my/ships")
    
    def orbit_ship(self, ship_symbol):
        return self._request("POST", f"/my/ships/{ship_symbol}/orbit")