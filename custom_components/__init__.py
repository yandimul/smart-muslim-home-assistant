from datetime import timedelta
import logging

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN, CONF_LATITUDE, CONF_LONGITUDE, KEMENAG_METHOD, SCAN_INTERVAL_MINUTES
)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    latitude = float(entry.data[CONF_LATITUDE])
    longitude = float(entry.data[CONF_LONGITUDE])

    async def async_update_data():
        today = dt_util.now().strftime("%d-%m-%Y")
        url = f"https://api.aladhan.com/v1/timings/{today}"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "method": KEMENAG_METHOD,
            "school": 0,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, params=params, timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    response.raise_for_status()
                    payload = await response.json()
            if payload.get("code") != 200 or "data" not in payload:
                raise UpdateFailed("AlAdhan returned an invalid response")
            data = payload["data"]
            data["smart_muslim_home_metadata"] = {
                "calculation_method": KEMENAG_METHOD,
                "calculation_method_name": "KEMENAG RI",
                "latitude": latitude,
                "longitude": longitude,
                "source": "AlAdhan API method 20",
            }
            return data
        except (aiohttp.ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"Unable to fetch Kemenag RI prayer times: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Smart Muslim Home (Kemenag RI)",
        update_method=async_update_data,
        update_interval=timedelta(minutes=SCAN_INTERVAL_MINUTES),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
