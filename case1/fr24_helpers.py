import requests
import json
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta, timezone

# Define the API base URL as a constant
API_BASE_URL = "https://fr24api.flightradar24.com/api"

# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points in kilometers."""
    R = 6371.0  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Fetch airport details
def get_airport_details(airport_code, headers):
    """Fetch detailed airport info from FR24 API.
    Cost: 50 credits per query ($0.015)
    Endpoint: /api/static/airports/{code}/full"""
    url = f"{API_BASE_URL}/static/airports/{airport_code}/full"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        credits = 50
        cost_per_credit = 0.0003
        total_cost = credits * cost_per_credit
        print(f"get_airport_details() API Cost: ${total_cost:.4f} ({credits} credits)")
        return data
    except Exception as e:
        print(f"Error fetching airport details: {e}")
        return None

# Get airline info using Airlines Light API
def get_airline_info(icao_code, headers):
    """Fetch airline information from FR24 API.
    Cost: 1 credit per query ($0.0003)
    Endpoint: /api/static/airlines/{icao}/light"""
    if not icao_code:
        return None
    url = f"{API_BASE_URL}/static/airlines/{icao_code}/light"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching airline info for {icao_code}: {e}")
        return None

# Fetch flight snapshot
def get_snapshot(timestamp, airport_code, headers, limit=1000, bounds=None, gspeed=None, altitude_ranges=None, categories='P,C,M,J,T'):
    """Fetch flight data at a specific timestamp.
    Cost: 8 credits per returned flight ($0.0024 per flight)
    Max cost with limit=1000: $2.40 per call
    Endpoint: /api/historic/flight-positions/full"""
    url = f"{API_BASE_URL}/historic/flight-positions/full"
    params = {
        'timestamp': timestamp,
        'airports': f'both:{airport_code}',
        'limit': limit,
        'categories': categories,
    }
    if altitude_ranges:
        if isinstance(altitude_ranges, str):
            params['altitude_ranges'] = altitude_ranges
        else:
            raise ValueError("altitude_ranges must be a string")
    if gspeed:
        if isinstance(gspeed, str):
            params['gspeed'] = gspeed
        else:
            raise ValueError("gspeed must be a string")
        
    if bounds:
        if isinstance(bounds, str):
            params['bounds'] = bounds
        else:
            raise ValueError("bounds must be a string")
        
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        #data = response.json().get('data', [])
        data = response.json()
        
        credits_per_flight = 8
        cost_per_credit = 0.0003
        total_flights = len(data)
        total_credits = total_flights * credits_per_flight
        total_cost = total_credits * cost_per_credit
        cost_info = {
            'flights_returned': total_flights,
            'total_credits': total_credits,
            'total_cost': total_cost
        }

        # Handle both list and dict responses
        if isinstance(data, list):
            return data, cost_info # Direct list of flights
        elif isinstance(data, dict):
            return data.get('data', []), cost_info  # Extract 'data' key if dict
        else:
            return [], cost_info  # Unexpected format, return empty list
        
    except Exception as e:
        print(f"Error fetching snapshot: {e}")
        return [], {'flights_returned': 0, 'total_credits': 0, 'total_cost': 0}

# Get airport coordinates
def calculate_bounds(lat, lon, radius_km=5):
    """Calculate bounding box around airport given a radius in km."""
    # Approximate conversions
    lat_degree = radius_km / 111.0  # 1° lat ~ 111 km
    lon_degree = radius_km / (111.0 * abs(np.cos(np.radians(lat))))  # Adjust for latitude

    north = lat + lat_degree
    south = lat - lat_degree
    west = lon - lon_degree
    east = lon + lon_degree

    return f"{north:.3f},{south:.3f},{west:.3f},{east:.3f}"


# Check if flight is within a circular area
def is_flight_in_circle(flight_lat, flight_lon, center_lat, center_lon, radius_km):
    """Check if a flight is within the specified circular area."""
    distance = haversine(flight_lat, flight_lon, center_lat, center_lon)
    return distance <= radius_km

# Calculate maximum possible distance an aircraft could travel
def calculate_max_distance(ground_speed_knots, time_delta_minutes):
    """Calculate the maximum possible distance an aircraft could travel."""
    if pd.isna(ground_speed_knots):
        return None
    speed_kmh = float(ground_speed_knots) * 1.852  # Convert knots to km/h
    hours = time_delta_minutes / 60
    return speed_kmh * hours

# Enhance dataframe with distance-related columns
def enhance_dataframe_with_distances(df, time_delta_minutes, center_lat, center_lon):
    """Add distance-related columns to the dataframe."""
    df['Start_end_Distance_km'] = df.apply(
        lambda row: haversine(row['Lat_start'], row['Lon_start'], row['Lat_end'], row['Lon_end'])
        if pd.notnull(row['Lat_start']) and pd.notnull(row['Lon_end']) else pd.NA,
        axis=1
    )
    df['Max_Possible_Distance_km_end'] = df.apply(
        lambda row: calculate_max_distance(row['Ground_Speed_end'], time_delta_minutes)
        if pd.notnull(row['Ground_Speed_end']) and row['Ground_Speed_end'] != 0 else pd.NA,
        axis=1
    )
    df['Distance_From_Airport_Start_km'] = df.apply(
        lambda row: haversine(center_lat, center_lon, row['Lat_start'], row['Lon_start'])
        if pd.notnull(row['Lat_start']) and pd.notnull(row['Lon_start']) else pd.NA,
        axis=1
    )
    df['Distance_From_Airport_End_km'] = df.apply(
        lambda row: haversine(center_lat, center_lon, row['Lat_end'], row['Lon_end'])
        if pd.notnull(row['Lat_end']) and pd.notnull(row['Lon_end']) else pd.NA,
        axis=1
    )
    return df

# Pivot dataframe to wide format
def pivot_to_wide(df, start_time, end_time):
    start_df = df[df['Timestamp'] == start_time].set_index('fr24_id')
    end_df = df[df['Timestamp'] == end_time].set_index('fr24_id')
    columns = ['Timestamp', 'Flight', 'Aircraft', 'Origin', 'Destination', 'Altitude', 
               'Ground_Speed', 'Vertical_Speed', 'Lat', 'Lon', 'Source', 'ETA', 'distance_to_airport', 'operating_as']
    start_df = start_df[columns].add_suffix('_start')
    end_df = end_df[columns].add_suffix('_end')
    merged_df = start_df.join(end_df, how='outer')
    merged_df.reset_index(inplace=True)
    return merged_df

# Detect arrivals
def clean_data_arrivals(df, airport_iata, center_lat, center_lon, radius_km, altitude_end=10, altitude_start=10):
    """Detect arrivals using original logic on pivoted dataframe."""
    arrivals_df = df[
        ((df['Altitude_end'] < altitude_end) | df['Altitude_end'].isna()) &
        (df['Destination_start'].str.contains(str(airport_iata), regex=False, na=False, case=False)) &
        ((df['Altitude_start'] >= altitude_start) | df['Altitude_start'].isna())
    ].copy()
    if arrivals_df.empty:
        print("No potential arrivals found in this interval.")
        return arrivals_df
    arrivals_df['Coord_end in Airport Bounds'] = arrivals_df.apply(
        lambda row: is_flight_in_circle(row['Lat_end'], row['Lon_end'], center_lat, center_lon, radius_km)
        if pd.notnull(row['Lat_end']) and pd.notnull(row['Lon_end']) else pd.NA,
        axis=1
    )
    arrivals_df = arrivals_df[arrivals_df['Coord_end in Airport Bounds'].isin([True, pd.NA])]
    return arrivals_df

# Detect departures
def clean_data_departures(df, airport_iata, center_lat, center_lon, radius_km, altitude_start=10):
    """Detect departures using original logic on pivoted dataframe."""
    departures_df = df[
        (df['Origin_start'].str.contains(airport_iata, regex=False, na=False, case=False) | df['Origin_start'].isna()) &
        (df['Origin_end'].str.contains(airport_iata, regex=False, na=False, case=False) | df['Origin_end'].isna()) &
        ((df['Altitude_start'] < altitude_start) | df['Altitude_start'].isna())
    ].copy()
    if departures_df.empty:
        print("No potential departures found in this interval.")
        return departures_df
    departures_df['Coord_start in Airport Bounds'] = departures_df.apply(
        lambda row: is_flight_in_circle(row['Lat_start'], row['Lon_start'], center_lat, center_lon, radius_km)
        if pd.notnull(row['Lat_start']) and pd.notnull(row['Lon_start']) else pd.NA,
        axis=1
    )
    departures_df['Distance_From_Airport_End_km'] = pd.to_numeric(
        departures_df['Distance_From_Airport_End_km'], errors='coerce'
    ).fillna(float('inf'))
    departures_df['Max_Possible_Distance_km_end'] = pd.to_numeric(
        departures_df['Max_Possible_Distance_km_end'], errors='coerce'
    ).fillna(float('inf'))
    departures_df = departures_df[
        ~((pd.notnull(departures_df['Distance_From_Airport_End_km'])) &
          (pd.notnull(departures_df['Max_Possible_Distance_km_end'])) &
          (departures_df['Distance_From_Airport_End_km'] >= departures_df['Max_Possible_Distance_km_end']))
    ]
    departures_df = departures_df[departures_df['Coord_start in Airport Bounds'].isin([True, pd.NA])]
    return departures_df