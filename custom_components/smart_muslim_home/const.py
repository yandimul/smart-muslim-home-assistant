DOMAIN = "smart_muslim_home"
NAME = "Smart Muslim Home"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
DEFAULT_LATITUDE = -6.200000
DEFAULT_LONGITUDE = 106.816666

# AlAdhan method 20 is KEMENAG - Kementerian Agama Republik Indonesia.
KEMENAG_METHOD = 20
SCAN_INTERVAL_MINUTES = 30

PRAYERS = {
    "fajr": ("Subuh", "mdi:weather-sunset-up"),
    "sunrise": ("Terbit", "mdi:weather-sunny"),
    "dhuhr": ("Zuhur", "mdi:white-balance-sunny"),
    "asr": ("Asar", "mdi:weather-sunny"),
    "maghrib": ("Magrib", "mdi:weather-sunset-down"),
    "isha": ("Isya", "mdi:weather-night"),
}
