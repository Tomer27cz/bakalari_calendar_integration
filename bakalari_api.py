import datetime
import time
import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

class BakalariAPI:
    def __init__(self, hass, entry_data):
        self.hass = hass
        self._url = entry_data['url']
        self._username = entry_data['username']
        self._password = entry_data['password']
        self._access_token = entry_data['access_token']
        self._refresh_token = entry_data['refresh_token']
        self._expires_at = int(time.time()) + entry_data['expires_in']

    async def _refresh_token(self):
        """Refresh the access token."""
        _LOGGER.info("Refreshing token")

        post_url = f"{self._url}/api/login"
        content_type = 'application/x-www-form-urlencoded'
        client_id = 'ANDR'

        body = f"client_id={client_id}&grant_type=refresh_token&refresh_token={self._refresh_token}"
        headers = {'Content-Type': content_type}

        async with async_get_clientsession(self.hass) as session:
            async with session.post(post_url, headers=headers, data=body) as response:
                if response.status != 200:
                    _LOGGER.error(f"Failed to refresh token: {response.status} {await response.text()}")
                    await self._re_login()

            response = await response.json()
            self._access_token = response.get('access_token')
            self._refresh_token = response.get('refresh_token')
            self._expires_at = int(time.time()) + response.get('expires_in')

    async def _re_login(self):
        """Re-login to the API."""
        _LOGGER.info("Re-logging in")

        post_url = f"{self._url}/api/login"
        content_type = 'application/x-www-form-urlencoded'
        client_id = 'ANDR'

        body = f"client_id={client_id}&grant_type=password&username={self._username}&password={self._password}"
        headers = {'Content-Type': content_type}

        async with async_get_clientsession(self.hass) as session:
            async with session.post(post_url, headers=headers, data=body) as response:
                if response.status != 200:
                    _LOGGER.error(f"Failed to re-login: {response.status} {await response.text()}")
                    raise ValueError("Failed to re-login")

                response = await response.json()
                self._access_token = response.get('access_token')
                self._refresh_token = response.get('refresh_token')
                self._expires_at = int(time.time()) + response.get('expires_in')

    async def _fetch_get(self, url, headers, post_name):
        """Fetch a post request."""
        async with async_get_clientsession(self.hass) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 401:
                    await self._refresh_token()
                    return await self._fetch_get(url, headers, post_name)

                if response.status != 200:
                    msg = f"Failed to fetch get ({post_name}): {response.status} {await response.text()}"

                    _LOGGER.error(msg)

                    raise ValueError(msg)

                return await response.json()

    async def get_permanent_time_table(self):
        """Get the permanent time table."""
        url = f"{self._url}/api/3/timetable/permanent"
        headers = {
            'Authorization': f"Bearer {self._access_token}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return await self._fetch_get(url, headers, "permanent time table")

    async def get_timetable(self, date: datetime.datetime):
        """Get the timetable for a specific date."""
        url = f"{self._url}/api/3/timetable/actual?date={date.strftime('%Y-%m-%d')}"
        headers = {
            'Authorization': f"Bearer {self._access_token}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return await self._fetch_get(url, headers, "timetable")
