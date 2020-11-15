import requests
from time import time
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


def get_activities(access_token):
    """
    Return all 'Ride' and 'VirtualRide' activities.
    Only scraping 'moving_time' and 'distance' from each activity
    """

    # access_token = get_access_token()
    URL = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {'before': int(time()), 'after': 1577836800, 'per_page': 30, 'page': 1}
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


def time_parser(seconds):
    """
    Input: int, time in seconds
    Returns: str of form: hours, minutes, seconds
    """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}h {minutes}m {seconds}s'


def display_stats(activity_data):
    """
    Prints the aggregated data
    """

    count_indoor, time_indoor, distance_indoor = activity_data['VirtualRide'].values()
    count_outdoor, time_outdoor, distance_outdoor = activity_data['Ride'].values()

    print()
    print('Indoor rides YTD:')
    print(f'Rides: {count_indoor}')
    print(f'Miles (virtual): {meters_to_miles(distance_indoor)}')
    print(f'Time: {time_parser(time_indoor)}')
    print('--------------------------')
    print('Outdoor rides YTD:')
    print(f'Rides: {count_outdoor}')
    print(f'Miles (virtual): {meters_to_miles(distance_outdoor)}')
    print(f'Time: {time_parser(time_outdoor)}')
    print('--------------------------')
    print('Cumulative YTD:')
    print(f'Rides: {count_indoor+count_outdoor}')
    print(f'Miles (virtual & actual): {meters_to_miles(distance_indoor+distance_outdoor)}')
    print(f'Time: {time_parser(time_outdoor+time_indoor)}')
    print()


def main():
    # Retrieve user access token
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    # Retrieve user activities
    activities = get_activities(access_token)

    # Aggregate activity data
    activity_data = aggregate_data(activities)

    # Display aggregated ata
    display_stats(activity_data)


if __name__ == '__main__':
    main()
