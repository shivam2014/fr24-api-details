# Documentation of FR24 API Endpoints

This document provides a complete reference for the Flightradar24 (FR24) API endpoints. It covers the server overview, versioning requirements, sandbox environment, storage rules, and detailed information on each available endpoint including descriptions, HTTP methods, parameters, sample Python code examples, and expected responses.

---

 General information

A REST API granting you immediate access to real-time flight data, along with information about airports and airlines.
Live flight positions full

Returns real-time aircraft flight movement information including latitude, longitude, speed, and altitude alongside key flight and aircraft information such as origin, destination, callsign, registration and aircraft type.
Live flight positions light

Returns real-time aircraft flight movement information including latitude, longitude, speed, and altitude.
Historic flights positions full

Returns historical aircraft flight movement information including latitude, longitude, speed, and altitude alongside key flight and aircraft information such as origin, destination, callsign, registration and aircraft type. FR24 API provides access to historical flight data, dating back to May 11, 2016, depending on the user's subscription plan. 
Historic flight positions light

Returns historical aircraft flight movement information including latitude, longitude, speed and altitude. FR24 API provides access to historical flight data, dating back to May 11, 2016, depending on the user's subscription plan.
Flight tracks

Returns positional tracks of a specific flight.
Airports light

Returns airport name, ICAO and IATA codes.
Airports full

Returns detailed airport information: full name, ICAO and IATA codes, localization, elevation, country, city, state, timezone details.
Airlines light

Returns airline name, ICAO and IATA codes.
Usage

Generates a report summarizing how the API has been utilized over a specified period.
Server overview

User portal: https://fr24api.flightradar24.com

API URL: https://fr24api.flightradar24.com/api
API versioning

The header Accept-Version is required and needs to be provided with every request.

Accept-Version: v1
Sandbox environment

For testing purposes without consuming any credits, the FR24 API offers a sandbox environment with static data. To use the sandbox, prepend "sandbox" to the specific endpoint. Your sandbox key can be found in the Key management section.

Examples:
/api/sandbox/live/flight-positions/light?airports=LHR
/api/sandbox/static/airports/ARN/light

Sandbox endpoints return predefined static responses, which match the schema of production endpoints.
Storage rules

For all FR24 API endpoints: All data accumulated from the FR24 API should not be stored for more than 30 days from the date it was first received. After this period, all stored data must be permanently deleted. 
---

### 1. Airlines Light

**Endpoint:**  
```
GET /api/static/airlines/{icao}/light
```

**Description:**  
 Get basic airline information by ICAO code
 Returns airline name, ICAO, and IATA codes.

**Parameters:**

- `icao` (string, required): The ICAO code of the airline.

**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/static/airlines/afl/light"
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")

```

**Responses:**

Schema:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `name`    | string   | Name of the airline. |
| `iata`    | string or null | Airline IATA code. |
| `icao`    | string or null | Airline ICAO code. |


- **200** – Success.
example :
{
"name": "American Airlines",
"iata": "AA",
"icao": "AAL"
}

- **400** – Validation error
example :
{
  "message": "Validation failed",
  "details": "The icao is not a valid ICAO code."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}
- **404** – Not found
example :
{
  "message": "Not found",
  "details": "The airline with the given ICAO code was not found."
}

---
### 2. Airports light
 Get basic airline information by code
**Endpoint:**  
```
GET /api/static/airports/{code}/light 
```

**Description:**  
Returns the airport name, ICAO and IATA codes.


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/static/airports/WAW/light"
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")


```

**Responses:**

Schema:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `name`    | string   | Name of the airport. |
| `iata`    | string or null | Airport IATA code. |
| `icao`    | string or null | Airport ICAO code. |
| `lon`     | number   | Longitude expressed in decimal degrees. |
| `lat`     | number   | Latitude expressed in decimal degrees. |
| `elevation` | number | Airport elevation in feet. |
| `country` | object   | Country information. |
| `country.code` | string | ISO 3166-1 alpha-2 code of the country. |
| `country.name` | string | Name of the country. |
| `city`    | string   | City of the airport. |
| `state`   | string or null | The state where the airport is located. Only available for US, Canada, Brazil, and Australia. |
| `timezone` | object   | Timezone information. |
| `timezone.name` | string | Name of the timezone. |
| `timezone.offset` | integer | Offset from UTC in seconds. |


- **200** – Success.
example :
{
  "name": "Stockholm Arlanda Airport",
  "iata": "ARN",
  "icao": "ESSA"
}

- **400** – Validation error
example :
{
  "message": "Validation failed",
  "details": "The icao is not a valid ICAO code."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}
- **404** – Not found
example :
{
  "message": "Validation error",
  "details": "The airport with the given code was not found."
}

---
### 3. Live flight positions full
 Get real-time flight positions with detailed information

**Endpoint:**  
```
GET /api/live/flight-positions/full
```

Returns comprehensive real-time information on aircraft flight movements, including flight and aircraft details such as origin, destination, and aircraft type. At least one query parameter is required to retrieve data.


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/live/flight-positions/full"
params = {
  'bounds': '50.682,46.218,14.422,22.243'
}
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")


```

**REQUEST**

QUERY-STRING PARAMETERS:
| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `bounds`      | string   | Coordinates defining an area. Order: north, south, west, east (comma-separated float values). Up to 3 decimal points will be processed. | `42.473,37.331,-10.014,-4.115` |
| `flights`     | string   | Flight numbers (comma-separated values). | `CA4515,UA1742` |
| `callsigns`   | string   | Flight callsigns (comma-separated values). | `WJA329,WSW102` |
| `registrations` | string | Aircraft registration numbers (comma-separated values). | `D-AFAM,EC-MQM` |
| `painted_as`  | string   | Aircraft painted in an airline's livery, identified by ICAO code, but not necessarily operated by that airline. | `SAS,ART` |
| `operating_as` | string | Aircraft operating under an airline's call sign, identified by ICAO code, but not necessarily an aircraft belonging to that airline. | `SAS,ART` |
| `airports`    | string   | Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). To determine direction use format: `<direction>:<code>`. Available directions: `both`, `inbound`, `outbound`. | `LHR,SE,inbound:WAW,US,outbound:JFK,both:ESSA` |
| `routes`      | string   | Flights between different airports or countries. Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). | `SE-US,ESSA-JFK` |
| `aircraft`    | string   | Aircraft ICAO type codes (comma-separated values). Wildcards are supported at the beginning or end, but not both (e.g., `*320` or `A32*`, but not `*32`). | `B38M,A32*,*33` |
| `altitude_ranges` | string | Flight altitude ranges (comma-separated values) represent the aircraft’s barometric pressure altitude above mean sea level (AMSL), measured under standard atmospheric conditions (1013.25 hPa / 29.92 in. Hg.). Altitudes are expressed in feet, starting from 0, where 0 reflects ground level AMSL. | `0-3000,5000-7000` |
| `squawks`     | string   | Squawk codes in hex format (comma-separated values). | `6135,7070` |
| `categories`  | string   | Categories of Flights (comma-separated values). Available values: `P`, `C`, `M`, `J`, `T`, `H`, `B`, `G`, `D`, `V`, `O`, `N`. | `P,C` |
| `data_sources` | string  | Source of information about flights (comma-separated values). Available values: `ADSB`, `MLAT`, `ESTIMATED`. Empty parameter will include all sources. | `ADSB,MLAT,ESTIMATED` |
| `airspaces`   | string   | Flight information region in lower or upper airspace. | `ESAA,LFFF` |
| `gspeed`      | string   | Flight ground speed (in knots). Accepts single value or range. | `120-140` or `80` or `0-40` |
| `limit`       | integer  | Limit of results. Max value 30000. | `100` |

--


REQUEST HEADERS:

| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `Accept-Version`| string   | Specifies the FR24 API version. The currently available version is v1 | `v1` |

	 

**Responses:**

Schema:
Field        | Type            | Description
-------------|-----------------|---------------------------------------------------------------
data         | array of object | Container for flight objects.
fr24_id      | string          | Unique identifier assigned by Flightradar24 to each flight leg.
flight       | string┃null    | Commercial flight number.
callsign     | string┃null    | Callsign used by ATC (from the aircraft transponder).
lat          | number          | Latest latitude (in decimal degrees).
lon          | number          | Latest longitude (in decimal degrees).
track        | integer         | True track (0-360°; note that 0 can sometimes mean unknown).
alt          | integer         | Barometric pressure altitude (AMSL in feet).
gspeed       | integer         | Ground speed in knots.
vspeed       | integer         | Rate of ascent/descent (feet per minute).
squawk       | string          | 4-digit ATC identifying code (in octal).
timestamp    | date-time       | UTC timestamp (ISO 8601 format) of the flight position.
source       | string          | Data source of the provided flight position.
hex          | string┃null    | 24-bit Mode-S identifier in hexadecimal.
type         | string┃null    | Aircraft ICAO type code.
reg          | string┃null    | Aircraft registration from the Mode-S identifier.
painted_as   | string┃null    | ICAO code of the carrier (from FR24's database).
operating_as | string┃null    | ICAO code derived from the flight callsign.
orig_iata    | string┃null    | Origin airport IATA code.
orig_icao    | string┃null    | Origin airport ICAO code.
dest_iata    | string┃null    | Destination airport IATA code.
dest_icao    | string┃null    | Destination airport ICAO code.
eta          | string┃null    | Estimated time of arrival (ISO 8601 format).


- **200** – Success.
example :
{
  "data": [
    {
      "fr24_id": "321a0cc3",
      "flight": "AF1463",
      "callsign": "AFR1463",
      "lat": -0.08806,
      "lon": -168.07118,
      "track": 219,
      "alt": 38000,
      "gspeed": 500,
      "vspeed": 340,
      "squawk": 6135,
      "timestamp": "2023-11-08T10:10:00Z",
      "source": "ADSB",
      "hex": "394C19",
      "type": "A321",
      "reg": "F-GTAZ",
      "painted_as": "THY",
      "operating_as": "THY",
      "orig_iata": "ARN",
      "orig_icao": "ESSA",
      "dest_iata": "LHR",
      "dest_icao": "EGLL",
      "eta": "2023-11-08T16:12:24Z"
    }
  ]
}

- **400** – Validation error
example :
{
  "message": "Validation error",
  "details": "The registration is not a valid aircraft registration code."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}

---
### 4. Live flight positions light
 Get real-time flight positions
**Endpoint:**  
```
GET /api/live/flight-positions/light
```

Returns real-time information on aircraft flight movements including latitude, longitude, speed, and altitude. At least one query parameter is required to retrieve data.


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/live/flight-positions/light"
params = {
  'bounds': '50.682,46.218,14.422,22.243'
}
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")

```

**REQUEST**

QUERY-STRING PARAMETERS

| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `bounds`      | string   | Coordinates defining an area. Order: north, south, west, east (comma-separated float values). Up to 3 decimal points will be processed. | `42.473,37.331,-10.014,-4.115` |
| `flights`     | string   | Flight numbers (comma-separated values). | `CA4515,UA1742` |
| `callsigns`   | string   | Flight callsigns (comma-separated values). | `WJA329,WSW102` |
| `registrations` | string | Aircraft registration numbers (comma-separated values). | `D-AFAM,EC-MQM` |
| `painted_as`  | string   | Aircraft painted in an airline's livery, identified by ICAO code, but not necessarily operated by that airline. | `SAS,ART` |
| `operating_as` | string | Aircraft operating under an airline's call sign, identified by ICAO code, but not necessarily an aircraft belonging to that airline. | `SAS,ART` |
| `airports`    | string   | Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). To determine direction use format: `<direction>:<code>`. Available directions: `both`, `inbound`, `outbound`. | `LHR,SE,inbound:WAW,US,outbound:JFK,both:ESSA` |
| `routes`      | string   | Flights between different airports or countries. Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). | `SE-US,ESSA-JFK` |
| `aircraft`    | string   | Aircraft ICAO type codes (comma-separated values). Wildcards are supported at the beginning or end, but not both (e.g., `*320` or `A32*`, but not `*32`). | `B38M,A32*,*33` |
| `altitude_ranges` | string | Flight altitude ranges (comma-separated values) represent the aircraft’s barometric pressure altitude above mean sea level (AMSL), measured under standard atmospheric conditions (1013.25 hPa / 29.92 in. Hg.). Altitudes are expressed in feet, starting from 0, where 0 reflects ground level AMSL. | `0-3000,5000-7000` |
| `squawks`     | string   | Squawk codes in hex format (comma-separated values). | `6135,7070` |
| `categories`  | string   | Categories of Flights (comma-separated values). Available values: `P`, `C`, `M`, `J`, `T`, `H`, `B`, `G`, `D`, `V`, `O`, `N`. | `P,C` |
| `data_sources` | string  | Source of information about flights (comma-separated values). Available values: `ADSB`, `MLAT`, `ESTIMATED`. Empty parameter will include all sources. | `ADSB,MLAT,ESTIMATED` |
| `airspaces`   | string   | Flight information region in lower or upper airspace. | `ESAA,LFFF` |
| `gspeed`      | string   | Flight ground speed (in knots). Accepts single value or range. | `120-140` or `80` or `0-40` |
| `limit`       | integer  | Limit of results. Max value 30000. | `100` |


REQUEST HEADERS:
| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `Accept-Version`| string   | Specifies the FR24 API version. The currently available version is v1 | `v1` |

**Responses:**

Schema :
Field      | Type             | Description
-----------|------------------|-----------------------------------------------------------
data       | array of object  | Collection of flight data objects.
fr24_id    | string           | Unique identifier assigned by Flightradar24 to each flight leg.
hex        | string or null   | 24-bit Mode-S identifier in hexadecimal format.
callsign   | string or null   | Callsign used by ATC for a specific flight (as sent by aircraft transponder).
lat        | number           | Latest latitude in decimal degrees.
lon        | number           | Latest longitude in decimal degrees.
track      | integer          | True track over ground in degrees (0-360). Note: 0 may indicate unknown.
alt        | integer          | Barometric pressure altitude above mean sea level (AMSL) in feet.
gspeed     | integer          | Ground speed in knots.
vspeed     | integer          | Vertical speed in feet per minute.
squawk     | string           | 4-digit ATC code in octal format.
timestamp  | date-time        | Flight position timestamp in UTC (ISO 8601 format).
source     | string           | Data source of the flight position.


- **200** – Success.
example :
{
  "data": [
    {
      "fr24_id": "321a0cc3",
      "hex": "394C19",
      "callsign": "AFR1463",
      "lat": -0.08806,
      "lon": -168.07118,
      "track": 219,
      "alt": 38000,
      "gspeed": 500,
      "vspeed": 340,
      "squawk": 6135,
      "timestamp": "2023-11-08T10:10:00Z",
      "source": "ADSB"
    }
  ]
}

- **400** – Validation error
example :
{
  "message": "Validation error",
  "details": "The registration is not a valid aircraft registration code."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}


---
### 5. Historic flight positions full
 Get historical flight positions
 **Endpoint:**  
```
GET /api/historic/flight-positions/full
```

Returns comprehensive historical information on aircraft flight movements, including flight and aircraft details such as origin, destination, and aircraft type, dating back to May 11, 2016. At least one query parameter and a history snapshot timestamp are required to retrieve data


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/historic/flight-positions/full"
params = {
  'bounds': '50.682,46.218,14.422,22.243',
  'timestamp': '1702383145'
}
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")

```

**REQUEST**
QUERY-STRING PARAMETERS
| **Parameter**      | **Type**   | **Description**                                                                 | **Examples**                            |
|--------------------|------------|---------------------------------------------------------------------------------|-----------------------------------------|
| `timestamp`        | integer    | Unix timestamp representing the exact point in time for which you want to fetch flight positions. The timestamp must be later than May 11, 2016. | `1702383145`                           |
| `bounds`           | string     | Coordinates defining an area. Order: north, south, west, east (comma-separated float values). Up to 3 decimal points will be processed. | `42.473,37.331,-10.014,-4.115`         |
| `flights`          | string     | Flight numbers (comma-separated values).                                        | `CA4515,UA1742`                        |
| `callsigns`        | string     | Flight callsigns (comma-separated values).                                      | `WJA329,WSW102`                        |
| `registrations`    | string     | Aircraft registration numbers (comma-separated values).                         | `D-AFAM,EC-MQM`                        |
| `painted_as`       | string     | Aircraft painted in an airline's livery, identified by ICAO code, but not necessarily operated by that airline. | `SAS,ART`                              |
| `operating_as`     | string     | Aircraft operating under an airline's call sign, identified by ICAO code, but not necessarily an aircraft belonging to that airline. | `SAS,ART`                              |
| `airports`         | string     | Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). To determine direction use format: `<direction>:<code>`. Available directions: `both`, `inbound`, `outbound`. | `LHR,SE,inbound:WAW,US,outbound:JFK,both:ESSA` |
| `routes`           | string     | Flights between different airports or countries. Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). | `SE-US,ESSA-JFK`                       |
| `aircraft`         | string     | Aircraft ICAO type codes (comma-separated values). Wildcards are supported at the beginning or end, but not both (e.g., `*320` or `A32*`, but not `*32`). | `B38M,A32*,*33`                        |
| `altitude_ranges`  | string     | Flight altitude ranges (comma-separated values) representing the aircraft’s barometric pressure altitude above mean sea level (AMSL). | `0-3000,5000-7000`                     |
| `squawks`          | string     | Squawk codes in hex format (comma-separated values).                            | `6135,7070`                            |
| `categories`       | string     | Categories of flights (comma-separated values). Available values: `P`, `C`, `M`, `J`, `T`, `H`, `B`, `G`, `D`, `V`, `O`, `N`. | `P,C`                                  |
| `data_sources`     | string     | Source of information about flights (comma-separated values). Available values: `ADSB`, `MLAT`, `ESTIMATED`. Empty parameter will include all sources. | `ADSB,MLAT,ESTIMATED`                  |
| `gspeed`           | string     | Flight ground speed (in knots). Accepts single value or range.                 | `120-140`, `80`, `0-40`                |
| `limit`            | integer    | Limit of results. Max value 30000.                                              | `100`                                  |

| **Category** | **Description**                                                                                       | **Examples**                                                                                      |
|--------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **P**        | **PASSENGER**: Commercial aircraft primarily designed to carry passengers.                             | Boeing 737, Airbus A320, Embraer E190                                                             |
| **C**        | **CARGO**: Aircraft designed exclusively for transporting goods.                                       | Boeing 747-8F, Airbus A330-200F, Lockheed Martin C-130 Hercules                                    |
| **M**        | **MILITARY_AND_GOVERNMENT**: Aircraft operated by military or governmental agencies.                  | Lockheed Martin F-22 Raptor, Boeing KC-135 Stratotanker, Airbus A400M                             |
| **J**        | **BUSINESS_JETS**: Larger private aircraft used for business travel.                                  | Gulfstream G650, Bombardier Global 7500, Dassault Falcon 7X                                        |
| **T**        | **GENERAL_AVIATION**: Non-commercial transport flights, including private, ambulance, aerial survey, flight training, and instrument calibration aircraft. | Cessna 172, Piper PA-28, Beechcraft Bonanza                                                        |
| **H**        | **HELICOPTERS**: Rotary-wing aircraft used for various purposes, including transport, medical, and military operations. | Sikorsky UH-60 Black Hawk, Bell 206 JetRanger, Airbus H125                                        |
| **B**        | **LIGHTER_THAN_AIR**: Lighter-than-air aircraft, including gas-filled airships of all kinds.           | Zeppelin NT, Goodyear Blimp, Cameron Balloons G-250                                               |
| **G**        | **GLIDERS**: Unpowered aircraft that glide through the air, typically used for sport and recreation.  | Schempp-Hirth Discus, DG Flugzeugbau DG-1000, Schleicher ASW 27                                  |
| **D**        | **DRONES**: Uncrewed aircraft, ranging from small consumer drones to larger UAVs.                     | DJI Phantom 4, General Atomics MQ-9 Reaper, Northrop Grumman RQ-4 Global Hawk                     |
| **V**        | **GROUND_VEHICLES**: Transponder-equipped vehicles, such as push-back tugs, fire trucks, and operations vehicles. | Oshkosh Striker 1500, Rosenbauer Panther 6x6, E-One Typhoon 4x4                                  |
| **O**        | **OTHER**: Aircraft appearing on Flightradar24 not classified elsewhere (e.g., International Space Station, UFOs, Santa). | International Space Station, unidentified flying objects, festive aircraft like Santa's sleigh     |
| **N**        | **NON_CATEGORIZED**: Aircraft not yet placed into a category in the Flightradar24 database.             | Newly added aircraft awaiting classification, experimental aircraft not yet categorized            |


REQUEST HEADERS

| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `Accept-Version`| string   | Specifies the FR24 API version. The currently available version is v1 | `v1` |

**Responses:**

Schema:
Object: data (array of objects)

Field         | Type           | Description
--------------|----------------|--------------------------------------------------------------
fr24_id       | string         | Unique identifier assigned by Flightradar24 to each flight leg.
flight        | string or null | Commercial flight number.
callsign      | string or null | Callsign used by Air Traffic Control to denote a specific flight (as sent by aircraft transponder).
lat           | number         | Latest latitude expressed in decimal degrees.
lon           | number         | Latest longitude expressed in decimal degrees.
track         | integer        | True track (over ground) in degrees (0-360). Note: 0 can sometimes mean unknown.
alt           | integer        | Barometric pressure altitude above mean sea level (AMSL) at standard atmospheric pressure (1013.25 hPa / 29.92 in. Hg), in feet.
gspeed        | integer        | Speed relative to the ground in knots.
vspeed        | integer        | Rate of ascent or descent in feet per minute.
squawk        | string         | 4-digit unique identifying code for ATC in octal format.
timestamp     | date-time      | Timestamp of the flight position in UTC (ISO 8601 date format).
source        | string         | Data source of the provided flight position.
hex           | string or null | 24-bit Mode-S identifier in hexadecimal format.
type          | string or null | Aircraft ICAO type code.
reg           | string or null | Aircraft registration as matched from Mode-S identifier.
painted_as    | string or null | ICAO code of the carrier mapped from FR24's internal database.
operating_as  | string or null | ICAO code of the airline carrier derived from flight callsign.
orig_iata     | string or null | Origin airport IATA code.
orig_icao     | string or null | Origin airport ICAO code.
dest_iata     | string or null | Destination airport IATA code.
dest_icao     | string or null | Destination airport ICAO code.
eta           | string or null | Estimated time of arrival (ISO 8601 date format).



- **200** – Success.
example :
{
  "data": [
    {
      "fr24_id": "321a0cc3",
      "flight": "AF1463",
      "callsign": "AFR1463",
      "lat": -0.08806,
      "lon": -168.07118,
      "track": 219,
      "alt": 38000,
      "gspeed": 500,
      "vspeed": 340,
      "squawk": 6135,
      "timestamp": "2023-11-08T10:10:00Z",
      "source": "ADSB",
      "hex": "394C19",
      "type": "A321",
      "reg": "F-GTAZ",
      "painted_as": "THY",
      "operating_as": "THY",
      "orig_iata": "ARN",
      "orig_icao": "ESSA",
      "dest_iata": "LHR",
      "dest_icao": "EGLL",
      "eta": "2023-11-08T16:12:24Z"
    }
  ]
}

- **400** – Validation error
example :
{
  "message": "Validation error",
  "details": "The registration is not a valid aircraft registration code."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}


---
---
### 6. Historic flight positions light
 Get historical flight positions with basic details
  **Endpoint:**  
```
GET  /api/historic/flight-positions/light
```

Returns historical information on aircraft flight movements including latitude, longitude, speed, and altitude, dating back to May 11, 2016. At least one query parameter and a history snapshot timestamp are required to retrieve data.


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/historic/flight-positions/light"
params = {
  'bounds': '50.682,46.218,14.422,22.243',
  'timestamp': '1702383145'
}
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")


```

**REQUEST**
QUERY-STRING PARAMETERS

| **Parameter**      | **Type**   | **Description**                                                                 | **Examples**                            |
|--------------------|------------|---------------------------------------------------------------------------------|-----------------------------------------|
| `timestamp`        | integer    | Unix timestamp representing the exact point in time for which you want to fetch flight positions. The timestamp must be later than May 11, 2016. | `1702383145`                           |
| `bounds`           | string     | Coordinates defining an area. Order: north, south, west, east (comma-separated float values). Up to 3 decimal points will be processed. | `42.473,37.331,-10.014,-4.115`         |
| `flights`          | string     | Flight numbers (comma-separated values).                                        | `CA4515,UA1742`                        |
| `callsigns`        | string     | Flight callsigns (comma-separated values).                                      | `WJA329,WSW102`                        |
| `registrations`    | string     | Aircraft registration numbers (comma-separated values).                         | `D-AFAM,EC-MQM`                        |
| `painted_as`       | string     | Aircraft painted in an airline's livery, identified by ICAO code, but not necessarily operated by that airline. | `SAS,ART`                              |
| `operating_as`     | string     | Aircraft operating under an airline's call sign, identified by ICAO code, but not necessarily an aircraft belonging to that airline. | `SAS,ART`                              |
| `airports`         | string     | Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). To determine direction use format: `<direction>:<code>`. Available directions: `both`, `inbound`, `outbound`. | `LHR,SE,inbound:WAW,US,outbound:JFK,both:ESSA` |
| `routes`           | string     | Flights between different airports or countries. Airports specified by IATA or ICAO codes or countries specified by ISO 3166-1 alpha-2 codes (comma-separated values). | `SE-US,ESSA-JFK`                       |
| `aircraft`         | string     | Aircraft ICAO type codes (comma-separated values). Wildcards are supported at the beginning or end, but not both (e.g., `*320` or `A32*`, but not `*32`). | `B38M,A32*,*33`                        |
| `altitude_ranges`  | string     | Flight altitude ranges (comma-separated values) representing the aircraft’s barometric pressure altitude above mean sea level (AMSL). | `0-3000,5000-7000`                     |
| `squawks`          | string     | Squawk codes in hex format (comma-separated values).                            | `6135,7070`                            |
| `categories`       | string     | Categories of flights (comma-separated values). Available values: `P`, `C`, `M`, `J`, `T`, `H`, `B`, `G`, `D`, `V`, `O`, `N`. | `P,C`                                  |
| `data_sources`     | string     | Source of information about flights (comma-separated values). Available values: `ADSB`, `MLAT`, `ESTIMATED`. Empty parameter will include all sources. | `ADSB,MLAT,ESTIMATED`                  |
| `gspeed`           | string     | Flight ground speed (in knots). Accepts single value or range.                 | `120-140`, `80`, `0-40`                |
| `limit`            | integer    | Limit of results. Max value 30000.                                              | `100`                                  |


| **Category** | **Description**                                                                                       | **Examples**                                                                                      |
|--------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **P**        | **PASSENGER**: Commercial aircraft primarily designed to carry passengers.                             | Boeing 737, Airbus A320, Embraer E190                                                             |
| **C**        | **CARGO**: Aircraft designed exclusively for transporting goods.                                       | Boeing 747-8F, Airbus A330-200F, Lockheed Martin C-130 Hercules                                    |
| **M**        | **MILITARY_AND_GOVERNMENT**: Aircraft operated by military or governmental agencies.                  | Lockheed Martin F-22 Raptor, Boeing KC-135 Stratotanker, Airbus A400M                             |
| **J**        | **BUSINESS_JETS**: Larger private aircraft used for business travel.                                  | Gulfstream G650, Bombardier Global 7500, Dassault Falcon 7X                                        |
| **T**        | **GENERAL_AVIATION**: Non-commercial transport flights, including private, ambulance, aerial survey, flight training, and instrument calibration aircraft. | Cessna 172, Piper PA-28, Beechcraft Bonanza                                                        |
| **H**        | **HELICOPTERS**: Rotary-wing aircraft used for various purposes, including transport, medical, and military operations. | Sikorsky UH-60 Black Hawk, Bell 206 JetRanger, Airbus H125                                        |
| **B**        | **LIGHTER_THAN_AIR**: Lighter-than-air aircraft, including gas-filled airships of all kinds.           | Zeppelin NT, Goodyear Blimp, Cameron Balloons G-250                                               |
| **G**        | **GLIDERS**: Unpowered aircraft that glide through the air, typically used for sport and recreation.  | Schempp-Hirth Discus, DG Flugzeugbau DG-1000, Schleicher ASW 27                                  |
| **D**        | **DRONES**: Uncrewed aircraft, ranging from small consumer drones to larger UAVs.                     | DJI Phantom 4, General Atomics MQ-9 Reaper, Northrop Grumman RQ-4 Global Hawk                     |
| **V**        | **GROUND_VEHICLES**: Transponder-equipped vehicles, such as push-back tugs, fire trucks, and operations vehicles. | Oshkosh Striker 1500, Rosenbauer Panther 6x6, E-One Typhoon 4x4                                  |
| **O**        | **OTHER**: Aircraft appearing on Flightradar24 not classified elsewhere (e.g., International Space Station, UFOs, Santa). | International Space Station, unidentified flying objects, festive aircraft like Santa's sleigh     |
| **N**        | **NON_CATEGORIZED**: Aircraft not yet placed into a category in the Flightradar24 database.             | Newly added aircraft awaiting classification, experimental aircraft not yet categorized            |


REQUEST HEADERS
| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `Accept-Version`| string   | Specifies the FR24 API version. The currently available version is v1 | `v1` |

**Responses:**

Schema:
Object: data (array of objects)

Field         | Type           | Description
--------------|----------------|--------------------------------------------------------------
fr24_id       | string         | Unique identifier assigned by Flightradar24 to each flight leg.
flight        | string or null | Commercial flight number.
callsign      | string or null | Callsign used by Air Traffic Control to denote a specific flight (as sent by aircraft transponder).
lat           | number         | Latest latitude expressed in decimal degrees.
lon           | number         | Latest longitude expressed in decimal degrees.
track         | integer        | True track (over ground) in degrees (0-360). Note: 0 can sometimes mean unknown.
alt           | integer        | Barometric pressure altitude above mean sea level (AMSL) at standard atmospheric pressure (1013.25 hPa / 29.92 in. Hg), in feet.
gspeed        | integer        | Speed relative to the ground in knots.
vspeed        | integer        | Rate of ascent or descent in feet per minute.
squawk        | string         | 4-digit unique identifying code for ATC in octal format.
timestamp     | date-time      | Timestamp of the flight position in UTC (ISO 8601 date format).
source        | string         | Data source of the provided flight position.



- **200** – Success.
example :
{
  "data": [
    {
      "fr24_id": "321a0cc3",
      "hex": "394C19",
      "callsign": "AFR1463",
      "lat": -0.08806,
      "lon": -168.07118,
      "track": 219,
      "alt": 38000,
      "gspeed": 500,
      "vspeed": 340,
      "squawk": 6135,
      "timestamp": "2023-11-08T10:10:00Z",
      "source": "ADSB"
    }
  ]
}

- **400** – Validation error
example :
{
  "message": "Validation error",
  "details": "The registration is not a valid aircraft registration code."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}


---
---
### 7. Flight tracks
 Get positional tracks for a specific flight
 
 **Endpoint:**  
```
GET  /api/flight-tracks
```

Returns a flight with positional tracks for both live and historical flights based on the FR24 flight ID. Availability of historical data depends on the user's subscription plan, with a maximum limit of up to 3 years.


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/flight-tracks"
params = {
  'flight_id': '34242a02'
}
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")



```

**REQUEST**
QUERY-STRING PARAMETERS
| **Parameter** | **Type** | **Description**                                                                 | **Examples** |
|---------------|----------|---------------------------------------------------------------------------------|--------------|
| `flight_id`   | string   | Flightradar24 ID of the active flight in hexadecimal format.                    | `34242a02`   |

REQUEST HEADERS

| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `Accept-Version`| string   | Specifies the FR24 API version. The currently available version is v1 | `v1` |

**Responses:**

Response schema:

| **Field**     | **Type**            | **Description**                                              |
|---------------|---------------------|-----------------------------------------------------------------------------------------------------------|
| `fr24_id`     | string              | Unique identifier assigned by Flightradar24 to the flight leg.                                                                                                |
| `tracks`      | array of objects    | List of flight position data points.                                                                                                                          |
|   `timestamp`   | date-time           | Timestamp of the flight position expressed in UTC (ISO 8601 date format).                                                                                   |
|   `lat`         | number              | Latitude expressed in decimal degrees.                                                                                                                      |
|   `lon`         | number              | Longitude expressed in decimal degrees.                                                                                                                     |
|   `alt`         | integer             | Barometric pressure altitude above mean sea level (AMSL) in feet, reported at standard atmospheric pressure (1013.25 hPa / 29.92 in. Hg.).                   |
|   `gspeed`      | integer             | Ground speed of the aircraft expressed in knots.                                                                                                            |
|   `vspeed`      | integer             | Rate of ascent or descent in feet per minute.                                                                                                                |
|   `track`       | integer             | True track (over ground) expressed in integer degrees as 0-360. 0 can sometimes mean unknown.                                                              |
|   `squawk`      | string              | 4-digit unique identifying code for ATC in octal format.                                                                                                     |
|   `callsign`    | string / null       | The last known callsign used by Air Traffic Control for the flight.                                                                                           |
|   `source`      | string              | The data source of the flight position.                                                                                                                       |



- **200** – Success.
example :
[
  {
    "fr24_id": "35f2ffd9",
    "tracks": [
      {
        "timestamp": "2024-07-02T11:22:43Z",
        "lat": 62.97148,
        "lon": -26.25193,
        "alt": 33000,
        "gspeed": 505,
        "vspeed": 0,
        "track": 105,
        "squawk": "2566",
        "callsign": "THY10",
        "source": "ADSB"
      }
    ]
  }
]

- **400** – Validation error
example :
{
  "message": "Validation error",
  "details": "The flight id field is required."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}
- **402** – Payment Required
example :
{
  "message": "Forbidden",
  "details": "Credit limit reached. Please top up your account."
}
- **404** – Not found
example :
{
  "message": "Not found",
  "details": "The requested flight could not be found."
}

---

### 8. Usage
 Get info on API account usage 
 **Endpoint:**  
```
GET  /api/usage
```


**Sample Python Code:**
```python
import requests
import json

url = "https://fr24api.flightradar24.com/api/usage"
headers = {
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")


```

**REQUEST**
QUERY-STRING PARAMETERS

| **Parameter** | **Type** | **Description**                                                                 | **Examples** |
|---------------|----------|---------------------------------------------------------------------------------|--------------|
| `period`      | enum     | Defines the time period for the data query. Default is `24h`. Allowed values: `24h`, `7d`, `30d`, `1y`. | `30d`        |

REQUEST HEADERS
| **Parameter** | **Type** | **Description** | **Examples** |
|---------------|----------|-----------------|--------------|
| `Accept-Version`| string   | Specifies the FR24 API version. The currently available version is v1 | `v1` |

**Responses:**

Schema of responses:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `fr24_id` | string | Unique identifier assigned by Flightradar24 to the flight leg. |
| `timestamp` | date-time | Timestamp of the flight position expressed in UTC (ISO 8601 date format). |
| `lat` | number | Latest latitude expressed in decimal degrees. |
| `lon` | number | Latest longitude expressed in decimal degrees. |
| `alt` | integer | Barometric pressure altitude above mean sea level (AMSL) reported at a standard atmospheric pressure (1013.25 hPa / 29.92 in. Hg.) expressed in feet. |
| `gspeed` | integer | Speed relative to the ground expressed in knots. |
| `vspeed` | integer | The rate at which the aircraft is ascending or descending in feet per minute. |
| `track` | integer | True track (over ground) expressed in integer degrees as 0-360. Please note that 0 can in some cases mean unknown. |
| `squawk` | string | 4-digit unique identifying code for ATC expressed in octal format. |
| `callsign` | string or null | The last known callsign used by Air Traffic Control to denote a specific flight, as sent by the aircraft transponder. This callsign is consistent across all reported positions. |
| `source` | string | Data source of the provided flight position. |


- **200** – Success.
example :
{
  "data": [
    {
      "endpoint": "live/flight-positions/full?{filters}",
      "request_count": 1,
      "credits": 936
    }
  ]
}

- **400** – Validation error
example :
{
  "message": "Validation failed",
  "details": "The selected period is invalid."
}

- **401** – Unauthorized
example :
{
  "message": "Unauthenticated."
}


---
# Cost of FR24 Endpoints API
Endpoint                       | Cost factor         | Credits | Maximum $ cost (with $0.0003 per credit)
------------------------------|---------------------|---------|-----------------------------------------
Live flight positions - full  | Per returned flight | 8       | $0.0024
Live flight positions - light | Per returned flight | 6       | $0.0018
Historic flight positions - full | Per returned flight | 8    | $0.0024
Historic flight positions - light | Per returned flight | 6   | $0.0018
Flight tracks                 | Per returned flight | 40      | $0.012
Airports light                | Per query           | 1       | $0.0003
Airports full                 | Per query           | 50      | $0.015
Airlines light                | Per query           | 1       | $0.0003

## Cost examples
Querying 1,000 flights for Live flight positions - light:

    Credits Used: 6,000 credits (1,000 flights * 6 credits per flight)
    Cost: $1.80 (6,000 credits * $0.0003 per credit)

Querying 500 flights for Historic flight positions - full:

    Credits Used: 4,000 credits (500 flights * 8 credits per flight)
    Cost: $1.20 (4,000 credits * $0.0003 per credit)

Querying 100 airports for Airports full data:

    Credits Used: 5,000 credits (100 queries * 50 credits per query)
    Cost: $1.50 (5,000 credits * $0.0003 per credit)

Credit usage optimization
Maximize your subscription credits:

    Plan your API usage to fully utilize your monthly subscription credits before they expire.
    Regularly monitor your credit balance and consumption rate.

Efficient use of top-up credits:

    Purchase top-up credits in increments that match your anticipated needs to avoid holding excess credits that may expire.
    Utilize Automated top up feature to automatically top-up your account when credit balance is low.

Using limit to control credit costs

Utilize the limit parameter in your API calls to restrict the amount of data retrieved and therefore limit the number of credits consumed. This is particularly useful for large datasets where you only need a subset of the data, allowing you to manage your credit usage more effectively.

The limit parameter is applicable only for flight-positions endpoints

## Example of limit param usage

The limit parameter is used to restrict the number of results returned by an API call, thereby controlling credit usage. Below is an example Python script that demonstrates how to use the limit parameter to restrict the number of results returned by an API call.

**Sample Python Code:**
```python
import requests
import json

# Define the API token and endpoint URL
API_TOKEN = '<your_api_token>'
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/historic/flight-positions/full'
# Define the headers, including the Authorization header with your API token
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {API_TOKEN}',
    'Accept-Version': 'v1'
}
# Define any query parameters
params = {
    'bounds': '50.682,46.218,14.422,22.243',
    'timestamp': '1702383145',
    'limit': 10
}
# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"
# Make the GET request to the API
response = requests.get(url, headers=headers, params=params)
# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    response_data = response.json()
    print("Response Data:")
    print(json.dumps(response_data, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Calculation of the cost of the call

Given:

    Credits per returned flight: 8 credits
    Price per credit: $0.0003 (assuming the highest price per credit)

Assume the API returns 10 results as specified by the limit parameter.

    Number of results returned: 10
    Total credits used: 10 results * 8 credits per result = 80 credits
    Total cost of the call: 80 credits * $0.0003 per credit = $0.024

Therefore, if the API returns 10 results, the total cost of the call would be $0.024.

It's important to note that the cost is determined by the number of returned entities, not by the specified limit.

## Exploring the calculated cost

After making the API call, you can explore the calculated cost using the /usage endpoint and in the Usage Metrics tab. Here is an example of calling the /usage endpoint to get the usage details:

**Sample Python Code:**
```python
import requests
import json
# Define the API token and endpoint URL
API_TOKEN = '<your_api_token>'
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/usage'
# Define the headers, including the Authorization header with your API token
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {API_TOKEN}',
    'Accept-Version': 'v1'
}
# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"
# Make the GET request to the API
response = requests.get(url, headers=headers)
# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    usage_data = response.json()
    print("Usage Data:")
    print(json.dumps(usage_data, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

Example of output:
{
    "data": [{
    "endpoint": "historic/flight-positions/full?{filters}",
        "request_count": 1,
        "credits": 80
    }]
}

Please note that the usage endpoint has a rate limit of 1 call per minute. Additionally, you can check the Usage metrics tab in your account dashboard to view detailed insights into your credit usage, as shown in the screenshot below.


---

For the most up-to-date and complete list of endpoints, please refer to the official FR24 API documentation at [FR24 API Documentation](https://fr24api.flightradar24.com/docs/endpoints/overview).

