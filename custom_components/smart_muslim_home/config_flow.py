import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE

from .const import DOMAIN, DEFAULT_LATITUDE, DEFAULT_LONGITUDE


class SmartMuslimHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure Smart Muslim Home using KEMENAG RI calculation."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id("smart_muslim_home")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Smart Muslim Home (Kemenag RI)", data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_LATITUDE, default=DEFAULT_LATITUDE): vol.Coerce(float),
            vol.Required(CONF_LONGITUDE, default=DEFAULT_LONGITUDE): vol.Coerce(float),
        })
        return self.async_show_form(step_id="user", data_schema=schema)
