# Separate outdoor rides and indoor rides

Frustrated that Strava combines the data from your virtual rides with your real rides?
Now you can separate the year-to-date totals for these activity types!

## Installation and usage

### Prerequisite

- Create a [Strava App](https://www.strava.com/settings/api)
- [Authorize](https://developers.strava.com/docs/authentication/#tokenexchange) a Strava user to obtain a `refresh_token`

### Afterwards

- Clone this repository & install dependencies:

```bash
git clone https://github.com/michaeljgallagher/strava_data && cd strava_data
pip install -r requirements.txt
```

- Update `settings.py` with your `CLIENT_ID`, `CLIENT_SECRET`, and `REFRESH_TOKEN` (obtained from authorization)
- Run `strava_data.py`:

```bash
python strava_data.py
```

The distance can be displayed in kilometers rather than miles by adding `-m` or `--metric` as an argument:

```bash
python strava_data.py -m
# or
python strava_data.py --metric
```

## Optional arguments

```bash
usage: strava_data.py [-h] [-m]

Separate and aggregate Rides and Virtual Rides from Strava

optional arguments:
  -h, --help    show this help message and exit
  -m, --metric  Display distance in kilometers rather than miles
```

## TODO

- Add command line arguments to specify a range of dates
- Add option to export data
