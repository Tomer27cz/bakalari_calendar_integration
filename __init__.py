"""Bakalari Integration"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .bakalari_api import BakalariAPI
from .coordinator import BakalariDataCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up warmup4ie from a config entry."""
    # Store an instance of the API object for your platforms to access
    hass.data.setdefault(DOMAIN, {})
    # hass.data[DOMAIN][entry.entry_id] = dict(entry.data)

    hass.data[DOMAIN][entry.entry_id] = {
        'url': entry.data['url'],
        'username': entry.data['username'],
        'password': entry.data['password']
    }

    hass.data[DOMAIN][entry.entry_id]['api'] = BakalariAPI(hass, entry.data)
    hass.data[DOMAIN][entry.entry_id]['coordinator'] = BakalariDataCoordinator(hass, hass.data[DOMAIN][entry.entry_id]['api'])

    await hass.data[DOMAIN][entry.entry_id]['coordinator'].async_config_entry_first_refresh()

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)

    return True












