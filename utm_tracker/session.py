import logging
from typing import Any, List

from django.contrib.sessions.backends.base import SessionBase
from django.utils.timezone import now as tz_now
from common.djangoapps.student.models import CourseEnrollment
from .models import LeadSource
from .types import UtmParamsDict
from django.core.exceptions import ObjectDoesNotExist
SESSION_KEY_UTM_PARAMS = "utm_params"

logger = logging.getLogger(__name__)


def strip_timestamps(params_list: List[UtmParamsDict]) -> List[UtmParamsDict]:
    """
    Return a copy of the session params without timestamps.

    The stashed params include a timestamp, which we need to pop as it
    will change on each request, and we don't want that.

    """
    return [{k: v for k, v in p.items() if k != "timestamp"} for p in params_list]


def stash_utm_params(session: SessionBase, params: UtmParamsDict) -> bool:
    """
    Add new utm_params to the list of utm_params in the session.

    If the params dict is empty ({}), or already stashed in the session,
    then it's ignored.

    Returns True if the params are stored.

    """
    if not params:
        return False

    session.setdefault(SESSION_KEY_UTM_PARAMS, [])
    if params in strip_timestamps(session[SESSION_KEY_UTM_PARAMS]):
        return False
    # cast to str so that it can be serialized in session; value is
    # recast to datetime automatically when the object is created.
    params["timestamp"] = tz_now().isoformat()
    session[SESSION_KEY_UTM_PARAMS].append(params)
    # because we are adding to a list, we are not actually changing the
    # session object itself, so we need to force it to be saved.
    session.modified = True
    return True


def pop_utm_params(session: SessionBase) -> List[UtmParamsDict]:
    """Pop the list of utm_param dicts from a session."""
    return session.pop(SESSION_KEY_UTM_PARAMS, [])

def dump_utm_params(user: Any, session: SessionBase,session_cookies:Any,) -> List[LeadSource]:
    """
    Flush utm_params from the session and save as LeadSource objects.

    Calling this function will remove all existing utm_params from the
    current session.

    Returns a list of LeadSource objects created - one for each utm_params
    dict found in the session.

    """
    created = []
    # import pdb;pdb.set_trace()
    session_id= "None"
    if session_cookies['lms_sessionid']:
        session_id= session_cookies['lms_sessionid']
    course_id = session.pop('course_id', [])
    if course_id:
        try:
            CourseEnrollment.objects.get(user_id=user.id,course_id=course_id)
            logger.info("This course is already enrolled by user %s: in course %s", user, course_id)
        except ObjectDoesNotExist:
            
            for params in pop_utm_params(session):
                try:
                    # check for duplicate entry
                    lead_source = LeadSource.objects.filter(session_id= session_id,course_id=course_id).first()
                    if not lead_source:

                        created.append(LeadSource.objects.create_from_utm_params(user, params,session_id,course_id))
                except ValueError as ex:
                    msg = str(ex)
                    logger.debug("Unable to save utm_params %s: %s", params, msg)
        except Exception as e:
            logger.error("!!!! Error  %s", e)
    return created