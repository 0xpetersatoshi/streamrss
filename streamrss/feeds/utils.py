from datetime import datetime
from time import mktime, struct_time

import dateutil.parser
import pytz


def strptime_to_utc(dtimestr: str) -> datetime:
    """Convert datetime string to datetime object with UTC timezone.
    
    :param dtimestr: The datetime string
    
    Returns a datetime object
    """
    d_object = dateutil.parser.parse(dtimestr)
    return _datetime_to_utc(d_object)


def struct_time_to_datetime(t: struct_time) -> datetime:
    """
    Converts time.struct_time objects to datetime objects.

    :param t: A time.struct_time object
    """
    return _datetime_to_utc(datetime.fromtimestamp(mktime(t)))


def _datetime_to_utc(d_object: datetime) -> datetime:
    """Add UTC timezone to datetime object"""
    if d_object.tzinfo is None:
        return d_object.replace(tzinfo=pytz.UTC)
    else:
        return d_object.astimezone(tz=pytz.UTC)


def write_bookmark(state: dict, feed_id: str, val: str) -> dict:
    """Write a bookmark to the state object.
    
    :param state: A dictionary holding a datestring bookmark for a feed
    :param feed_id: The name/id of a feed to track
    :param val: The datetime string value to set as the bookmark

    Returns The updated state object
    """
    if not state.get("bookmarks"):
        state["bookmarks"] = {}
    state["bookmarks"][feed_id] = val
    return state


def get_bookmark(state: dict, feed_id: str) -> str:
    """Get a bookmark from the state object.
    
    :param state: A dictionary holding a datestring bookmark for a feed
    :param feed_id: The name/id of a feed to track

    Returns a bookmark for a provided feed
    """
    return state.get('bookmarks', {}).get(feed_id, {})
