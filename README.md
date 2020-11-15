# Separate outdoor rides and indoor rides

Frustrated that Strava combines the data from your virtual rides with your real rides?
Now you can separate the year-to-date totals for these activity types!

## Installation and usage

### Prerequisite:

 - Create a [Strava App](https://www.strava.com/settings/api)
 - [Authorize](https://developers.strava.com/docs/authentication/#tokenexchange) a Strava user to obtain a `refresh_token`

### Afterwards:

```bash
# Clone this repository
git clone https://github.com/michaeljgallagher/strava_data && cd strava_data

# Install dependencies
pip install -r requirements.txt
```

Update `settings.py` with your `CLIENT_ID`, `CLIENT_SECRET`, and `REFRESH_TOKEN` (obtained from authorization)

```bash
# run strava_data.py
python strava_data.py
```

## TODO

- Add command line arguments to specify a range of dates
- Add option to export data