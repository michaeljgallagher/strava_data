import argparse
import requests
from datetime import datetime
from settings import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


def get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN):
    """
    Return the temporary access token
    """

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token',
        'f': 'json'
    }
    res = requests.post('https://www.strava.com/oauth/token', data=payload)
    if res.status_code == 200:
        return res.json()['access_token']
    else:
        raise RuntimeError(res.text)


def get_activities(access_token, start_date=datetime(2021, 1, 1), end_date=datetime.today()):
    """
    Return all 'Ride' and 'VirtualRide' activities.
    Only scraping 'moving_time' and 'distance' from each activity
    """

    URL = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': 'Bearer ' + access_token}
    # currently defaults to activities from beginning of 2020
    params = {'before': int(end_date.timestamp()), 'after': int(start_date.timestamp()), 'per_page': 30, 'page': 1}
    activities = []
    while True:
        res = requests.get(URL, headers=headers, params=params)
        params['page'] += 1
        if res.status_code == 200:
            if len(res.json()) == 0:
                break

            for activity in res.json():
                if activity['type'] in {'Ride', 'VirtualRide'}:  # Only want rides and virtual rides
                    activities.append({
                        # Only need type, distance, and time
                        'type': activity['type'],
                        'distance': activity['distance'],
                        'moving_time': activity['moving_time']
                    })
        else:
            raise RuntimeError(res.text)
    
    return activities


def aggregate_data(activities):
    """
    Aggregates the data from user activities
    'time' is in seconds, 'distance' is in meters
    """

    data = {
        'Ride': {'count': 0, 'time': 0, 'distance': 0},
        'VirtualRide': {'count': 0, 'time': 0, 'distance': 0}
    }
    for activity in activities:
        data[activity['type']]['count'] += 1
        data[activity['type']]['time'] += activity['moving_time']
        data[activity['type']]['distance'] += activity['distance']
    
    return data


def meters_to_miles(distance):
    """
    Convert meters to miles (2 decimal places)
    """

    return round(distance * 0.00062137119, 2)


def meters_to_kms(distance):
    """
    Convert meters to kilometers (2 decimal places)
    """
    return round(distance * 0.001, 2)


def time_parser(seconds):
    """
    Input: int, time in seconds
    Returns: str of form: hours, minutes, seconds
    """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}h {minutes}m {seconds}s'


def display_stats(activity_data, metric=False, start_date=datetime(2021, 1, 1), end_date=datetime.today()):
    """
    Prints the aggregated data
    """
    count_indoor, time_indoor, distance_indoor = activity_data['VirtualRide'].values()
    count_outdoor, time_outdoor, distance_outdoor = activity_data['Ride'].values()
    
    if metric:
        distance_indoor = meters_to_kms(distance_indoor)
        distance_outdoor = meters_to_kms(distance_outdoor)
        units = 'kilometers'
    else:
        distance_indoor = meters_to_miles(distance_indoor)
        distance_outdoor = meters_to_miles(distance_outdoor)
        units = 'miles'
    
    begin = start_date.isoformat()[:10]
    end = end_date.isoformat()[:10]

    print('\n\n')
    print(f'Activities from \033[1m{begin}\033[0m to \033[1m{end}\033[0m')
    print()
    print('\033[1mIndoor stats\033[0m')
    print(f'Rides: {count_indoor}')
    print(f'Distance (virtual): {distance_indoor} {units}')
    print(f'Time: {time_parser(time_indoor)}')
    print()
    print('\033[1mOutdoor stats\033[0m')
    print(f'Rides: {count_outdoor}')
    print(f'Distance (actual): {distance_outdoor} {units}')
    print(f'Time: {time_parser(time_outdoor)}')
    print()
    print('\033[1mCumulative stats\033[0m')
    print(f'Rides: {count_indoor+count_outdoor}')
    print(f'Distance (virtual & actual): {round(distance_indoor+distance_outdoor ,2)} {units}')
    print(f'Time: {time_parser(time_outdoor+time_indoor)}')
    print()


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Separate and aggregate Rides and Virtual Rides from Strava')
    parser.add_argument('-m', '--metric', action='store_true', help='Display distance in kilometers rather than miles')
    parser.add_argument('-s', '--start', action='store', default=datetime(2021, 1, 1), type=datetime.fromisoformat, help='Specify start date (YYYY-MM-DD)')
    parser.add_argument('-e', '--end', action='store', default=datetime.today(), type=datetime.fromisoformat, help='Specify end date (YYYY-MM-DD)')
    args = parser.parse_args()

    # Retrieve user access token
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    # Retrieve user activities
    print('Fetching ride data...')
    activities = get_activities(access_token, args.start, args.end)

    # Aggregate activity data
    activity_data = aggregate_data(activities)

    # Display aggregated data
    display_stats(activity_data, metric=args.metric, start_date=args.start, end_date=args.end)


if __name__ == '__main__':
    main()
