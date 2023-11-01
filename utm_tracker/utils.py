
from .models import LeadSource


def update_leassourceenrollment(*args,**kwargs):
    import pdb;pdb.set_trace()
    lms_session_data= kwargs.get('lms_session_data')
    lms_course_enrollment = kwargs.get('lms_enrollment')
    if lms_course_enrollment:
        lms_course_mode= lms_course_enrollment.mode
        lms_course_user = lms_course_enrollment.user
        lms_course_course_id = str(lms_course_enrollment.course_id)
    
    if lms_session_data:
        lms_session_id = lms_session_data.COOKIES['lms_sessionid']
        get_leadsource_details = LeadSource.objects.filter(session_id= lms_session_id,course_id= lms_course_course_id)
        
    elif lms_course_mode== 'no-id-professional':
        get_leadsource_details = LeadSource.objects.filter(user= lms_course_user,course_id= lms_course_course_id)
        
    
    if get_leadsource_details:
            lead_source_data = get_leadsource_details.latest('created_at')
            lead_source_data.enrollment='COMPLETED'
            lead_source_data.save()
        