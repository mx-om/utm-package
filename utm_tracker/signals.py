from django.dispatch import receiver
from common.djangoapps.student.models import CourseEnrollment
from common.djangoapps.student.signals import ENROLLMENT_TRACK_UPDATED,ENROLLMENT_UPDATED_SESSION
from django.db.models.signals import post_save
from crum import get_current_request
from .utils import *

@receiver(ENROLLMENT_UPDATED_SESSION)
# @receiver(post_save,sender=CourseEnrollment)
def update_enrollment_utm(sender,**kwargs):
    # import pdb; pdb.set_trace()
    lms_session_data = kwargs.get('request')
    lms_enrollment= kwargs.get('enrollment')
    login_user = get_current_request().user.id
    learner_user_id = lms_enrollment.user_id
    if login_user == learner_user_id:
        update_leassourceenrollment(lms_session_data=lms_session_data,lms_enrollment=lms_enrollment)
    return True
    