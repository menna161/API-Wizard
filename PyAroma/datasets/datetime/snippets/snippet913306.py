from pandas import DataFrame
from pandas import json_normalize
import requests
import datetime
from urllib.parse import urljoin
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from petpy.exceptions import PetfinderInvalidCredentials, PetfinderInsufficientAccess, PetfinderResourceNotFound, PetfinderUnexpectedError, PetfinderInvalidParameters, PetfinderRateLimitExceeded


def _parameters(breed=None, size=None, gender=None, color=None, coat=None, animal_type=None, location=None, distance=None, state=None, country=None, query=None, sort=None, name=None, age=None, good_with_children=None, good_with_dogs=None, good_with_cats=None, declawed=None, house_trained=None, special_needs=None, before_date=None, after_date=None, animal_id=None, organization_id=None, status=None, results_per_page=None, page=None):
    "\n    Internal function for determining which parameters have been passed and aligning them to their respective\n    Petfinder API parameters.\n\n    Parameters\n    ----------\n    breed: str, tuple or list of str, optional\n        String or tuple or list of strings of desired animal type breed to search.\n    size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional\n        String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one\n        of 'small', 'medium', 'large', or 'xlarge'.\n    gender: {'male', 'female', 'unknown'} str, tuple or list of str, optional\n        String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',\n        or 'unknown'.\n    color : str, optional\n        String representing specified animal 'color' to search. Colors for each available animal type in the\n        Petfinder database can be found using the :code:`animal_types()` method.\n    coat : {'short', 'medium', 'long', 'wire', 'hairless', 'curly'}, str, tuple or list of str, optional\n        Desired coat(s) to return. Must be of 'short', 'medium', 'long', 'wire', 'hairless', or 'curly'.\n    animal_type : {'dog', 'cat', 'rabbit', 'small-furry', 'horse', 'bird', 'scales-fins-other', 'barnyard'}, str, optional\n        String representing desired animal type to search. Must be one of 'dog', 'cat', 'rabbit', 'small-furry',\n        'horse', 'bird', 'scales-fins-other', or 'barnyard'.\n    location : str, optional\n        Returns results by specified location. Must be in the format 'city, state' for city-level results,\n        'latitude, longitude' for lat-long results, or 'postal code'.\n    distance : int, optional\n        Returns results within the distance of the specified location. If not given, defaults to 100 miles.\n        Maximum distance range is 500 miles.\n    state : str, optional\n        Filters the results by the selected state. Must be a two-letter state code abbreviation of the state\n        name, such as 'WA' for Washington or 'NY' for New York.\n    country : {'US', 'CA'}, optional\n        Filters results to specified country. Must be a two-letter abbreviation of the country and is limited\n        to the United States and Canada.\n    query : str, optional\n        Search matching and partially matching name, city or state.\n    sort : {'recent', '-recent', 'distance', '-distance'}, optional\n            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',\n            '-recent', 'distance', or '-distance'.\n    name : str, optional\n        Name of animal or organization to search.\n    age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional\n        String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',\n        'young', 'adult', 'senior'.\n    good_with_cats: bool, optional\n        Filters returned animal results to animals that are designated as good with cats. Must be a boolean value\n        (True, False) or a value that can be coerced to a boolean (1, 0).\n    good_with_children: bool, optional\n        Filters returned animal results to animals that are designated as good with children. Must be a boolean value\n        (True, False) or a value that can be coerced to a boolean (1, 0).\n    good_with_dogs: bool, optional\n        Filters returned animal results to animals that are designated as good with dogs. Must be a boolean value\n        (True, False) or a value that can be coerced to a boolean (1, 0).\n    before_date: str, datetime, optional\n        Returns results with a `published_at` datetime before the specified time. Must be a string in the form of\n        'YYYY-MM-DD' or 'YYYY-MM-DD H:M:S' or a datetime object.\n    after_date: str, datetime, optional\n        Returns results with a `published_at` datetime after the specified time. Must be a string in the form of\n        'YYYY-MM-DD' or 'YYYY-MM-DD H:M:S' or a datetime object.\n    animal_id : int, tuple or list of int, optional\n        Integer or list or tuple of integers representing animal IDs obtained from Petfinder.\n    organization_id : str, tuple or list of str, optional\n        Returns animals associated with given :code:`organization_id`. Can be a str or a tuple or list of str\n        representing multiple organizations.\n    status : {'adoptable', 'adopted', 'found'} str, optional\n        Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.\n    results_per_page : int, default 20\n        Number of results to return per page. Defaults to 20 results and cannot exceed 100 results per page.\n    page : int, default 1\n        Specifies which page of results to return. Defaults to the first page of results. If set to :code:`None`,\n        all results will be returned.\n\n    Returns\n    -------\n    dict\n        Dictionary representing aligned parameters and headers for ingestion into the Petfinder API.\n\n    "
    if isinstance(age, (list, tuple)):
        age = ','.join(age).replace(' ', '')
    if isinstance(gender, (list, tuple)):
        gender = ','.join(gender).replace(' ', '')
    if isinstance(status, (list, tuple)):
        status = ','.join(status).replace(' ', '')
    if isinstance(animal_type, (list, tuple)):
        animal_type = ','.join(animal_type).replace(' ', '')
    if isinstance(size, (list, tuple)):
        size = ','.join(size).replace(' ', '')
    if isinstance(coat, (list, tuple)):
        coat = ','.join(coat).replace(' ', '')
    if (good_with_cats is not None):
        good_with_cats = int(good_with_cats)
    if (good_with_children is not None):
        good_with_children = int(good_with_children)
    if (good_with_dogs is not None):
        good_with_dogs = int(good_with_dogs)
    if (declawed is not None):
        declawed = int(declawed)
    if (house_trained is not None):
        house_trained = int(house_trained)
    if (special_needs is not None):
        special_needs = int(special_needs)
    _check_parameters(animal_types=animal_type, size=size, gender=gender, age=age, coat=coat, status=status, distance=distance, sort=sort, limit=results_per_page, good_with_cats=good_with_cats, good_with_children=good_with_children, good_with_dogs=good_with_dogs, declawed=declawed, house_trained=house_trained, special_needs=special_needs)
    args = {'breed': breed, 'size': size, 'gender': gender, 'age': age, 'color': color, 'coat': coat, 'animal_type': animal_type, 'location': location, 'distance': distance, 'state': state, 'country': country, 'query': query, 'sort': sort, 'name': name, 'animal_id': animal_id, 'organization': organization_id, 'good_with_cats': good_with_cats, 'good_with_children': good_with_children, 'good_with_dogs': good_with_dogs, 'house_trained': house_trained, 'special_needs': special_needs, 'declawed': declawed, 'before': before_date, 'after': after_date, 'status': status, 'limit': results_per_page, 'page': page}
    args = {key: val for (key, val) in args.items() if (val is not None)}
    return args
