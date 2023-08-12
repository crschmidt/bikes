import datetime
import json

import requests


def get_all_paths():
    """Generate all possible paths.

    The service requires a pathfilter, but doesn't check the request against the 
    available paths for a particular counter. So we just generate all possible 
    paths to include.
    """
    path_filter = {'directions': [], 'offsets': []}
    for i in ['East', 'West', 'North', 'South', 'SouthWest', 'NorthWest', 'SouthEast', 'NorthEast', 'Unspecified']:
        path_filter['directions'].append(i)
        path_filter['offsets'].append({'direction': i, 'pathways': [
                                      "Bike Lane", "Crosswalk", "Roadway", "Sidewalk", "Bike Path", "Trail", "Combined"]})
    return path_filter


def fetch_site(site_id, date=datetime.date(2023, 1, 1)):

    url = "https://mhd.ms2soft.com/tdms.ui/nmds/analysis/GetLocationCount"
    # User-Agent filtering is so silly.
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    params = {
        'masterLocalId': site_id,
        'date': date.strftime("%m/%d/%Y"),
    }

    params['pathFiltersStr'] = json.dumps(get_all_paths())

    r = requests.post(url=url, data=params,
                      headers={'User-Agent': ua})

    d = json.loads(r.content)
    trips = {}
    for i in d['countData']['IntervalCounts']:
        mode, count = i['Mode'], i['Count']
        trips[mode] = trips.get(mode, 0) + count
    return trips


def run():
    print(fetch_site("5004_WB", datetime.date(2023, 8, 10)))


def run_all(date=datetime.date(2023, 8, 10)):
    d = json.load(open("dailycounters.json"))
    for i in d:
        print(i[1], fetch_site(i[0], date))


if __name__ == "__main__":
    d = datetime.datetime.now()-datetime.timedelta(days=2)
    run_all(d)
