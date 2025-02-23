import pandas as pd

# Load the CSVs (replace with your actual file paths)
flight_departures = pd.read_csv('./Outputs/flight_departures.csv')
all_departures_df = pd.read_csv('./Outputs/all_departures_df.csv')
flight_arrivals = pd.read_csv('./Outputs/flight_arrivals.csv')
all_arrivals_df = pd.read_csv('./Outputs/all_arrivals_df.csv')

# Step 1: Enhanced normalization function
def normalize_flight_code(flight_str, source='flight_departures'):
    if pd.isna(flight_str):
        return None
    flight_str = str(flight_str).replace(' ', '').replace('*', '')
    # Handle D8* prefix (e.g., D8*5701 -> D85701)
    if flight_str.startswith('D8') and len(flight_str) > 3:
        flight_str = 'D8' + flight_str[3:]
    # Normalize HP* and APF* to a consistent form (use HP* as the standard)
    if flight_str.startswith('APF'):
        flight_str = 'HP' + flight_str[3:]
    elif flight_str.startswith('HP'):
        flight_str = 'HP' + flight_str[2:]  # Already in HP form, just ensure consistency
    return flight_str

# Normalize flight_departures
flight_departures['Flight_normalized'] = flight_departures['Flight'].apply(
    lambda x: normalize_flight_code(x, source='flight_departures')
)

# Normalize all_departures_df
all_departures_df['Flight_start_normalized'] = all_departures_df['Flight_start'].apply(
    lambda x: normalize_flight_code(x, source='all_departures')
)
all_departures_df['Flight_end_normalized'] = all_departures_df['Flight_end'].apply(
    lambda x: normalize_flight_code(x, source='all_departures')
)

# Normalize flight_arrivals
flight_arrivals['Flight_normalized'] = flight_arrivals['Flight'].apply(
    lambda x: normalize_flight_code(x, source='flight_arrivals')
)

# Normalize all_arrivals_df
all_arrivals_df['Flight_start_normalized'] = all_arrivals_df['Flight_start'].apply(
    lambda x: normalize_flight_code(x, source='all_arrivals')
)
all_arrivals_df['Flight_end_normalized'] = all_arrivals_df['Flight_end'].apply(
    lambda x: normalize_flight_code(x, source='all_arrivals')
)

# Step 2: Unified flight columns
# For departures
all_departures_df['Flight_unified'] = all_departures_df['Flight_start_normalized'].fillna(
    all_departures_df['Flight_end_normalized']
)
# For arrivals
all_arrivals_df['Flight_unified'] = all_arrivals_df['Flight_start_normalized'].fillna(
    all_arrivals_df['Flight_end_normalized']
)

# Step 3: Comparison
# Departures comparison
flight_departures_subset = flight_departures[['Flight_normalized', 'Departure Time', 'Arrival Time', 
                                            'Destination Code', 'Airline', 'Destination Full']]
all_departures_subset = all_departures_df[['Flight_unified', 'Destination_end']].dropna(subset=['Flight_unified'])

# Arrivals comparison
flight_arrivals_subset = flight_arrivals[['Flight_normalized', 'Departure Time', 'Arrival Time', 
                                        'Origin Code', 'Airline', 'Origin Full']]
all_arrivals_subset = all_arrivals_df[['Flight_unified', 'Origin_end']].dropna(subset=['Flight_unified'])

# Find common flights for both departures and arrivals
common_flights = flight_departures_subset.merge(
    all_departures_subset,
    left_on='Flight_normalized',
    right_on='Flight_unified',
    how='inner'
)

common_flights_arrivals = flight_arrivals_subset.merge(
    all_arrivals_subset,
    left_on='Flight_normalized',
    right_on='Flight_unified',
    how='inner'
)

# Flights only in flight_departures/arrivals
only_in_flight_departures = flight_departures_subset[
    ~flight_departures_subset['Flight_normalized'].isin(all_departures_subset['Flight_unified'])
]

only_in_flight_arrivals = flight_arrivals_subset[
    ~flight_arrivals_subset['Flight_normalized'].isin(all_arrivals_subset['Flight_unified'])
]

# Flights only in all_departures/arrivals_df
only_in_all_departures = all_departures_subset[
    ~all_departures_subset['Flight_unified'].isin(flight_departures_subset['Flight_normalized'])
]

only_in_all_arrivals = all_arrivals_subset[
    ~all_arrivals_subset['Flight_unified'].isin(flight_arrivals_subset['Flight_normalized'])
]

# Step 4: Format the output
# Departures output
common_output = common_flights[['Flight_normalized', 'Departure Time', 'Arrival Time', 
                              'Destination Code', 'Airline', 'Destination Full']]
common_output['Status'] = 'Common'

only_in_flight_departures_output = only_in_flight_departures.copy()
only_in_flight_departures_output['Status'] = 'Only in flight_departures'

only_in_all_departures_output = only_in_all_departures[['Flight_unified']].copy()
only_in_all_departures_output['Departure Time'] = 'N/A'
only_in_all_departures_output['Arrival Time'] = 'N/A'
only_in_all_departures_output['Destination Code'] = all_departures_df['Destination_end'].fillna('N/A')
only_in_all_departures_output['Airline'] = 'N/A'
only_in_all_departures_output['Destination Full'] = 'N/A'
only_in_all_departures_output['Status'] = 'Only in all_departures_df'
only_in_all_departures_output.columns = ['Flight_normalized', 'Departure Time', 'Arrival Time', 
                                        'Destination Code', 'Airline', 'Destination Full', 'Status']

# Arrivals output
common_output_arrivals = common_flights_arrivals[['Flight_normalized', 'Departure Time', 'Arrival Time', 
                                                'Origin Code', 'Airline', 'Origin Full']]
common_output_arrivals['Status'] = 'Common'

only_in_flight_arrivals_output = only_in_flight_arrivals.copy()
only_in_flight_arrivals_output['Status'] = 'Only in flight_arrivals'

only_in_all_arrivals_output = only_in_all_arrivals[['Flight_unified']].copy()
only_in_all_arrivals_output['Departure Time'] = 'N/A'
only_in_all_arrivals_output['Arrival Time'] = 'N/A'
only_in_all_arrivals_output['Origin Code'] = all_arrivals_df['Origin_end'].fillna('N/A')
only_in_all_arrivals_output['Airline'] = 'N/A'
only_in_all_arrivals_output['Origin Full'] = 'N/A'
only_in_all_arrivals_output['Status'] = 'Only in all_arrivals_df'
only_in_all_arrivals_output.columns = ['Flight_normalized', 'Departure Time', 'Arrival Time', 
                                      'Origin Code', 'Airline', 'Origin Full', 'Status']

# Combine results
# Departures
final_comparison = pd.concat([common_output, only_in_flight_departures_output, 
                            only_in_all_departures_output], ignore_index=True)

# Arrivals
final_comparison_arrivals = pd.concat([common_output_arrivals, only_in_flight_arrivals_output, 
                                     only_in_all_arrivals_output], ignore_index=True)

# Rename Flight_normalized back to Flight
final_comparison = final_comparison.rename(columns={'Flight_normalized': 'Flight'})
final_comparison_arrivals = final_comparison_arrivals.rename(columns={'Flight_normalized': 'Flight'})

# Save and display
print("Departures Comparison Table:")
print(final_comparison)
final_comparison.to_csv('./Outputs/flight_comparison_departures.csv', index=False)

print("\nArrivals Comparison Table:")
print(final_comparison_arrivals)
final_comparison_arrivals.to_csv('./Outputs/flight_comparison_arrivals.csv', index=False)