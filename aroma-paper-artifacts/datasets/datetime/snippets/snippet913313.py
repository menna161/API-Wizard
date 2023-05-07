from pandas import DataFrame
from pandas import json_normalize
import requests
import datetime
from urllib.parse import urljoin
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from petpy.exceptions import PetfinderInvalidCredentials, PetfinderInsufficientAccess, PetfinderResourceNotFound, PetfinderUnexpectedError, PetfinderInvalidParameters, PetfinderRateLimitExceeded


@on_exception(expo, RateLimitException, max_tries=10)
@limits(calls=50, period=1)
@limits(calls=1000, period=86400)
def animals(self, animal_id=None, animal_type=None, breed=None, size=None, gender=None, age=None, color=None, coat=None, status=None, name=None, organization_id=None, location=None, distance=None, good_with_children=None, good_with_dogs=None, good_with_cats=None, house_trained=None, declawed=None, special_needs=None, before_date=None, after_date=None, sort=None, pages=1, results_per_page=20, return_df=False):
    "\n        Returns adoptable animal data from Petfinder based on specified criteria.\n\n        Parameters\n        ----------\n        animal_id : int, tuple or list of int, optional\n            Integer or list or tuple of integers representing animal IDs obtained from Petfinder. When\n            :code:`animal_id` is specified, the other function parameters are overridden. If :code:`animal_id`\n            is not specified, a search of animals on Petfinder matching given criteria is performed.\n        animal_type : {'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'}, str, optional\n            String representing desired animal type to search. If specified, must be one of 'dog', 'cat', 'rabbit',\n            'small-furry', 'horse', 'bird', 'scales-fins-other', or 'barnyard'.\n        breed: str, tuple or list of str, optional\n            String or tuple or list of strings of desired animal type breed to search. Available animal breeds in\n            the Petfinder database can be found using the :code:`breeds()` method.\n        size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional\n            String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one\n            of 'small', 'medium', 'large', or 'xlarge'.\n        gender : {'male', 'female', 'unknown'} str, tuple or list of str, optional\n            String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',\n            or 'unknown' if specified.\n        age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional\n            String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',\n            'young', 'adult', 'senior' if specified.\n        color : str, optional\n            String representing specified animal 'color' to search. Colors for each available animal type in the\n            Petfinder database can be found using the :code:`animal_types()` method.\n        coat : {'short', 'medium', 'long', 'wire', 'hairless', 'curly'}, str, tuple or list of str, optional\n            Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.\n        status : {'adoptable', 'adopted', 'found'} str, optional\n            Animal status to filter search results. If specified, must be one of 'adoptable', 'adopted', or 'found'.\n        name : str, optional\n            Searches for animal names matching or partially matching name.\n        organization_id : str, tuple or list of str, optional\n            Returns animals associated with given :code:`organization_id`. Can be a str or a tuple or list of str\n            representing multiple organizations.\n        location : str, optional\n            Returns results by specified location. Must be in the format 'city, state' for city-level results,\n            'latitude, longitude' for lat-long results, or 'postal code'.\n        distance : int, optional\n            Returns results within the distance of the specified location. If not given, defaults to 100 miles.\n            Maximum distance range is 500 miles.\n        good_with_children : bool, optional\n            Filters animals that have been designated as being good with children.\n        good_with_cats : bool, optional\n            Filters the returned animals by those who have been flagged as being good with cats.\n        good_with_dogs : bool, optional\n            Returns results restricted to animals who have been flagged as being good with dogs.\n        declawed : bool, optional\n            Filters results for animals that have been declawed.\n        special_needs : bool, optional\n            Returns animals that have special needs.\n        house_trained : bool, optional\n            If specified, only returns animals that are listed as house-trained.\n        before_date : str, datetime\n            Returns results that have been published before the specified datetime. Must be a valid ISO8601 date-time\n            string or a datetime object.\n        after_date : str, datetime\n            Returns results that have been published after the specified datetime. Must be a valid ISO8601 date-time\n            string or a datetime object.\n        sort : {'recent', '-recent', 'distance', '-distance'}, optional\n            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',\n            '-recent', 'distance', or '-distance'.\n        pages : int, default 1\n            Specifies which page of results to return. Defaults to the first page of results. If set to :code:`None`,\n            all results will be returned.\n        results_per_page : int, default 20\n            Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.\n        return_df : boolean, default False\n            If :code:`True`, the results will be coerced into a pandas DataFrame.\n\n        Returns\n        -------\n        dict or pandas DataFrame\n            Dictionary object representing the returned JSON object from the Petfinder API. If :code:`return_df=True`,\n            the results are returned as a pandas DataFrame.\n\n        Examples\n        --------\n        # Create an authenticated connection to the Petfinder API.\n        >>> pf = Petfinder(key=key, secret=secret)\n        # Getting first 20 results without any search criteria\n        >>> animals = pf.animals()\n        # Extracting data on specific animals with animal_ids\n        >>> animal_ids = []\n        >>> for i in animals['animals'][0:3]:\n        >>>    animal_ids.append(i['id'])\n        >>> animal_data = pf.animals(animal_id=animal_ids)\n        # Returning a pandas DataFrame of the first 150 animal results\n        >>> animals = pf.animals(results_per_page=50, pages=3, return_df=True)\n\n        "
    max_page_warning = False
    if (before_date is not None):
        if isinstance(before_date, str):
            try:
                before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                before_date = datetime.datetime.strptime(before_date, '%Y-%m-%d')
        before_date = before_date.astimezone().replace(microsecond=0).isoformat()
    if (after_date is not None):
        if isinstance(after_date, str):
            try:
                after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                after_date = datetime.datetime.strptime(after_date, '%Y-%m-%d')
        after_date = after_date.astimezone().replace(microsecond=0).isoformat()
    if ((after_date is not None) and (before_date is not None)):
        if (before_date < after_date):
            raise ValueError('before_date parameter must be more recent than after_date parameter.')
    if (animal_id is not None):
        url = urljoin(self._host, 'animals/{id}')
        if isinstance(animal_id, (tuple, list)):
            animals = []
            for ani_id in animal_id:
                r = self._get_result(url.format(id=ani_id), headers={'Authorization': ('Bearer ' + self._access_token)})
                animals.append(r.json()['animal'])
        else:
            r = self._get_result(url.format(id=animal_id), headers={'Authorization': ('Bearer ' + self._access_token)})
            animals = r.json()['animal']
    else:
        url = urljoin(self._host, 'animals/')
        if animal_type:
            url += '?type={}'.format(animal_type)
        params = _parameters(animal_type=animal_type, breed=breed, size=size, gender=gender, age=age, color=color, coat=coat, status=status, name=name, organization_id=organization_id, location=location, distance=distance, sort=sort, results_per_page=results_per_page, before_date=before_date, after_date=after_date, good_with_cats=good_with_cats, good_with_children=good_with_children, good_with_dogs=good_with_dogs, house_trained=house_trained, declawed=declawed, special_needs=special_needs)
        if (pages is None):
            params['limit'] = 100
            params['page'] = 1
            r = self._get_result(url, headers={'Authorization': ('Bearer ' + self._access_token)}, params=params)
            animals = r.json()['animals']
            max_pages = r.json()['pagination']['total_pages']
            for page in range(2, (max_pages + 1)):
                params['page'] = page
                r = self._get_result(url, headers={'Authorization': ('Bearer ' + self._access_token)}, params=params)
                if isinstance(r.json(), dict):
                    if ('animals' in r.json().keys()):
                        for i in r.json()['animals']:
                            animals.append(i)
        else:
            pages += 1
            params['page'] = 1
            r = self._get_result(url, headers={'Authorization': ('Bearer ' + self._access_token)}, params=params)
            animals = r.json()['animals']
            max_pages = r.json()['pagination']['total_pages']
            if (pages > int(max_pages)):
                pages = max_pages
                max_page_warning = True
            for page in range(2, pages):
                params['page'] = page
                r = self._get_result(url, headers={'Authorization': ('Bearer ' + self._access_token)}, params=params)
                if isinstance(r.json(), dict):
                    if ('animals' in r.json().keys()):
                        for i in r.json()['animals']:
                            animals.append(i)
    animals = {'animals': animals}
    if return_df:
        animals = _coerce_to_dataframe(animals)
    if max_page_warning:
        print('pages parameter exceeded maximum number of available pages available from the Petfinder API. As a result, the maximum number of pages {max_page} was returned'.format(max_page=max_pages))
    return animals
