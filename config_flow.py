import logging

from homeassistant import config_entries, core
from homeassistant.const import CONF_URL, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

async def validate_auth(url: str, username: str, password: str, hass: core.HomeAssistant) -> dict:
    """Validate the user input allows us to connect."""
    post_url = f"{url}/api/login"
    content_type = 'application/x-www-form-urlencoded'
    client_id = 'ANDR'  # Android

    body = f"client_id={client_id}&grant_type=password&username={username}&password={password}"
    headers = {'Content-Type': content_type}

    async with async_get_clientsession(hass) as session:
        async with session.post(post_url, headers=headers, data=body) as response:
            if response.status != 200:
                _resp = await response.json()
                _error = _resp.get('error_description', 'Authentication failed (no error description)')
                raise ValueError(_error)
            return await response.json()

class BakalariTestConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """BakalariTest config flow."""

    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface."""
        errors = {}
        if user_input is not None:
            # await self.async_set_unique_id(user_input[CONF_USERNAME])
            # self._abort_if_unique_id_configured()

            try:
                response = await validate_auth(user_input[CONF_URL], user_input[CONF_USERNAME], user_input[CONF_PASSWORD], self.hass)

                data = {
                    'url': user_input[CONF_URL],  # 'https://bakalari.example.com
                    'username': user_input[CONF_USERNAME],  # 'username'
                    'password': user_input[CONF_PASSWORD],  # 'password'
                    'access_token': response.get('access_token'),
                    'refresh_token': response.get('refresh_token'),
                    'expires_in': response.get('expires_in'),
                }

                return self.async_create_entry(title=user_input[CONF_USERNAME], data=data)
            except ValueError as e:
                errors["base"] = str(e)

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )
