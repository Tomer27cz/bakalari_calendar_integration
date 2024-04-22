"""Bakalari Integration"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from bakalari.bakalari_api import BakalariAPI
from bakalari.calendar import BakalariCalendar
from bakalari.coordinator import BakalariDataCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up warmup4ie from a config entry."""
    # Store an instance of the API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = BakalariAPI(hass, entry.data)
    coor = BakalariDataCoordinator(hass, hass.data[DOMAIN][entry.entry_id])

    await coor.async_config_entry_first_refresh()

    # async_add_entities([BakalariCalendar(coordinator)])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)

    return True












