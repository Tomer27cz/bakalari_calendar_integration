import datetime
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.calendar import CalendarEntity, CalendarEvent

_LOGGER = logging.getLogger(__name__)

class BakalariCalendar(CoordinatorEntity, CalendarEntity):

    async def async_get_events(self,
                               hass: HomeAssistant,
                               start_date: datetime.datetime,
                               end_date: datetime.datetime
                               ) -> list[CalendarEvent]:

        _LOGGER.error(f"async_get_events coordinator.data {self.coordinator.data}")
        raise ValueError("async_get_events not implemented")

        pass
    #     """Get all events in a specific time range."""
    #     events = []
    #     for event in self._events:
    #         if event['start'] >= from_date and event['end'] <= to_date:
    #             events.append(event)
    #     return events
    #
    #
    # async def async_added_to_hass(self):
    #     """When entity is added to hass."""
    #     await super().async_added_to_hass()
    #     self._session = async_get_clientsession(self.hass)
    #
    # async def async_update(self):
    #     """Get the latest data and updates the states."""
    #     self._events = await self._fetch_events()













