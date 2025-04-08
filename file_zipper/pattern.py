# Uppercase followed by uppercase letter or number.
airline_iata_pattern = r'[A-Z][A-Z0-9]'

# Three uppercase characters
airline_icao_pattern = r'[A-Z]{3}'

# One to four digits optionally followed by an upper case letter.
flight_number_pattern = r'\d{1,4}[A-Z]?'

iata_station_pattern = r'[A-Z]{3}'
