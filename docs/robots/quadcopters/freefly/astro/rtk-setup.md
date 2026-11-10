---
title: RTK Setup
author: Max Gardenswartz
updated: 2026-11-06
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  How to point an Astro at our RTK corrections. The Astros use their NTRIP client app with the RTKLib caster.
---

--8<-- "rtk-intro.md"

## Which Astros Are Set Up

| Astro | Works with the Emlid RS3 base station |
|---|---|
| astro1 | Yes, configured; works immediately |
| astro2 | Yes, configured; works immediately |
| astro3 | Not set up |

!!! note "No License Is Needed"
    A license is not required to use third-party RTK corrections, such as the ones from our Emlid RS3 ground station. The Auterion RTK license is only for Auterion's own corrections.

Before this, read [RTK Setup](../../../../hardware/rtk-setup.md): the ground station must be on.

## The NTRIP Client App

Each Astro runs an `ntrip-client` app. Open the Astro's dashboard in a browser (see [Astro Overview](overview.md#astro-dashboard)), go to **Apps**, and click **Settings** on `ntrip-client`.

![The Apps page of an Astro dashboard listing app-base-v2, ntrip-client with a Settings button, astro_mavros, camera-distance-sensor and payload-manager-env.](../../../../images/freefly/astro-ntrip-apps.jpg){ width="60%" }

## Settings

![The NTRIP client settings page showing the third-party RTK section filled in, with the username and password hidden.](../../../../images/freefly/astro-ntrip-settings.jpg){ width="60%" }

| Setting | Value |
|---|---|
| Stream RTK corrections | On |
| Bypass GCS for RTK Corrections | On |
| Third-party RTK | On |
| Use NTRIP 2.0 | On |
| Enable TLS | Off |
| Host | The discovery server |
| Port | 2101 |
| Mountpoint | `BASE` |
| Username and password | In `.env.example` of [homebrew_docker](https://github.com/UFL-Autonomy-Park/homebrew_docker/blob/main/.env.example) |

The username and password are not sensitive. They are in the `.env.example` file of `homebrew_docker`.

## Checking That It Works

An easier way: click the GPS icon in the **Fly** tab of AMC to check the RTK fix.

When it works, the app's status page says it is connected, with the distance to the base station, and that it is using a third-party RTK correction service.

![The NTRIP client status page showing Connected with the distance to the base station and the message Using third-party RTK correction service.](../../../../images/freefly/astro-ntrip-status.jpg){ width="60%" }
