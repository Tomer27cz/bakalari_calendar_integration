import datetime
import logging
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from bakalari.bakalari_api import BakalariAPI

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class BakalariDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, api: BakalariAPI):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=datetime.timedelta(hours=1),
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        try:
            async with async_timeout.timeout(10):
                return await self.api.get_timetable(datetime.datetime.now())
        except Exception as e:
            raise UpdateFailed(f"Error communicating with API: {e}")




