# Smart Muslim Home (Kemenag RI)

Custom Home Assistant integration for prayer times and Hijri date.

## Calculation method
This integration explicitly requests **AlAdhan API method `20` = KEMENAG, Kementerian Agama Republik Indonesia**. It does not use the Singapore method. Asar uses the standard/Shafi calculation (`school=0`).

> Important: This is a third-party API implementation of the Kemenag calculation profile, not a direct connection to an official Kemenag timetable feed. Local official schedules may include location-specific adjustments or ihtiyath, so compare against the Bimas Islam/Kemenag timetable for your city before relying on notifications. Hijri dates can also differ from Indonesia's official isbat decision.

## Features
- Prayer-time sensors: Subuh, Terbit, Zuhur, Asar, Magrib, Isya
- Hijri date sensor and attributes
- Next prayer sensor and minutes remaining
- Ramadan flag
- UI configuration for latitude and longitude
- Calculation method metadata on prayer sensors

## Install via HACS
1. Upload this repository to GitHub.
2. In HACS > Integrations > menu > Custom repositories, add this repository URL and choose **Integration**.
3. Download and restart Home Assistant.
4. Settings > Devices & services > Add integration > **Smart Muslim Home**.
5. Enter your home latitude and longitude.

## API
Uses `https://api.aladhan.com/v1/timings/{date}` with `method=20` (KEMENAG RI). Internet access is required.


## Bahasa
Form konfigurasi mendukung bahasa Indonesia (`id.json`) dan Inggris (`en.json`). Bahasa yang ditampilkan Home Assistant mengikuti bahasa profil pengguna di **Settings > Profile > Language**. Nama sensor yang disediakan integrasi ini sudah menggunakan istilah Indonesia.
