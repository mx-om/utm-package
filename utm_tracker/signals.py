from django.dispatch import receiver
from common.djangoapps.student.models import CourseEnrollment
from common.djangoapps.student.signals import ENROLLMENT_TRACK_UPDATED,ENROLLMENT_UPDATED_SESSION
from django.db.models.signals import post_save

from .utils import *
@receiver(ENROLLMENT_UPDATED_SESSION)
# @receiver(post_save,sender=CourseEnrollment)
def update_enrollment_utm(sender,**kwargs):
    lms_session_data = kwargs.get('request')
    lms_session_enrollment= kwargs.get('enrollment')
    update_leassourceenrollment(lms_session_data=lms_session_data,lms_session_enrollment=lms_session_enrollment)
    