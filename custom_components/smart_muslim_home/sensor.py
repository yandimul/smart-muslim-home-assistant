from datetime import datetime, time, timedelta
import re

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, PRAYERS


def _clean_time(value):
    """Remove timezone suffixes and annotations returned by the API."""
    match = re.search(r"\d{1,2}:\d{2}", str(value))
    if not match:
        return None
    return match.group(0)


def _today_time(value):
    clean = _clean_time(value)
    if clean is None:
        return None
    hour, minute = map(int, clean.split(":"))
    now = dt_util.now()
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


class SmartMuslimSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, icon, value_fn, attr_fn=None):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_icon = icon
        self._value_fn = value_fn
        self._attr_fn = attr_fn

    @property
    def native_value(self):
        return self._value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self):
        if self._attr_fn:
            return self._attr_fn(self.coordinator.data)
        return {}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for api_key, (label, icon) in PRAYERS.items():
        entities.append(SmartMuslimSensor(
            coordinator, f"prayer_{api_key}", label,
            icon,
            lambda data, k=api_key: _clean_time(data["timings"].get(k, "")),
            lambda data: {
                "metode_kalkulasi": data.get("smart_muslim_home_metadata", {}).get("calculation_method"),
                "sumber_kalkulasi": data.get("smart_muslim_home_metadata", {}).get("source"),
                "latitude": data.get("smart_muslim_home_metadata", {}).get("latitude"),
                "longitude": data.get("smart_muslim_home_metadata", {}).get("longitude"),
            }
        ))

    def hijri_value(data):
        hijri = data.get("date", {}).get("hijri", {})
        return hijri.get("date", "Tidak tersedia")

    def hijri_attrs(data):
        hijri = data.get("date", {}).get("hijri", {})
        return {
            "hari": hijri.get("weekday", {}).get("ar"),
            "tanggal": hijri.get("day"),
            "bulan": hijri.get("month", {}).get("en"),
            "bulan_arab": hijri.get("month", {}).get("ar"),
            "tahun": hijri.get("year"),
            "tanggal_hijriah_lengkap": (
                f"{hijri.get('day', '')} {hijri.get('month', {}).get('en', '')} {hijri.get('year', '')}"
            ).strip(),
            "catatan": "Tanggal Hijriah dari AlAdhan dapat berbeda dari penetapan resmi Indonesia.",
            "sumber_kalkulasi_waktu_salat": data.get("smart_muslim_home_metadata", {}).get("calculation_method_name"),
            "metode_kalkulasi": data.get("smart_muslim_home_metadata", {}).get("calculation_method"),
        }

    entities.append(SmartMuslimSensor(
        coordinator, "hijri_date", "Tanggal Hijriah", "mdi:calendar-star",
        hijri_value, hijri_attrs
    ))

    def next_prayer(data):
        timings = data.get("timings", {})
        now = dt_util.now()
        candidates = []
        for key, (label, _) in PRAYERS.items():
            if key == "sunrise":
                continue
            prayer_time = _today_time(timings.get(key, ""))
            if prayer_time and prayer_time > now:
                candidates.append((prayer_time, label))
        if not candidates:
            return "Subuh"
        return min(candidates, key=lambda item: item[0])[1]

    def next_attrs(data):
        timings = data.get("timings", {})
        now = dt_util.now()
        candidates = []
        for key, (label, _) in PRAYERS.items():
            if key == "sunrise":
                continue
            prayer_time = _today_time(timings.get(key, ""))
            if prayer_time and prayer_time > now:
                candidates.append((prayer_time, label))
        if candidates:
            prayer_time, label = min(candidates, key=lambda item: item[0])
        else:
            # After Isha, the next prayer is tomorrow's Fajr; approximate its time by adding one day.
            fajr = _today_time(timings.get("fajr", ""))
            prayer_time = (fajr + timedelta(days=1)) if fajr else None
            label = "Subuh"
        return {
            "next_prayer_name": label,
            "next_prayer_time": prayer_time.isoformat() if prayer_time else None,
            "minutes_until": max(0, int((prayer_time - now).total_seconds() // 60)) if prayer_time else None,
        }

    entities.append(SmartMuslimSensor(
        coordinator, "next_prayer", "Salat Berikutnya", "mdi:mosque",
        next_prayer, next_attrs
    ))

    def is_ramadan(data):
        hijri = data.get("date", {}).get("hijri", {})
        return "Ya" if str(hijri.get("month", {}).get("number")) == "9" else "Tidak"

    entities.append(SmartMuslimSensor(
        coordinator, "is_ramadan", "Sedang Ramadan", "mdi:moon-waning-crescent",
        is_ramadan
    ))

    async_add_entities(entities)
