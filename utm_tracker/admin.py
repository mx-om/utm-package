from django.contrib import admin

from .models import LeadSource


class LeadSourceAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = ("user", "medium", "source", "campaign", "timestamp","enrollment")
    search_fields = ("user__first_name", "user__last_name", "term", "content")
    list_filter = ("medium", "source", "timestamp")
    readonly_fields = ("created_at", "timestamp")

class LeadSourceUrlTracker(LeadSource):
    class Meta:
        proxy = True
        verbose_name = "Source URL Tracking"

class LeadSourceUrlTrackerAdmin(admin.ModelAdmin):
    # list_display = ('get_course','get_source','get_count_clicked','get_count_enrolled','get_count_pending')
    change_list_template= "utm_change_list.html"

    def changelist_view(self, request, extra_context=None):
        get_lead_data = LeadSource.objects.all()
        all_courses = get_lead_data.values('course_id').distinct()
        Overall_source_data = []
        for course in all_courses:
            all_source = get_lead_data.values('medium','source','campaign').distinct()
            for source in all_source:
                source_name = source['medium']+'__'+source['source']+'__'+source['campaign']
                count_clicked = get_lead_data.filter(medium=source['medium'],source=source['source'],campaign=source['campaign'],course_id=course['course_id']).count()
                count_enrolled = get_lead_data.filter(medium=source['medium'],source=source['source'],campaign=source['campaign'],course_id=course['course_id'],enrollment='Completed').count()
                count_pending = get_lead_data.filter(medium=source['medium'],source=source['source'],campaign=source['campaign'],course_id=course['course_id'],enrollment='Incomplete').count()

                source_count_data = {
                    'course_id':course['course_id'],
                    'source_name':source_name,
                    'count_clicked':count_clicked,
                    'count_enrolled':count_enrolled,
                    'count_pending':count_pending
                }
                Overall_source_data.append(source_count_data)
        extra_context = {'overall_clicks': get_lead_data.count(), 'overall_source_data':Overall_source_data}
        return super(LeadSourceUrlTrackerAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(LeadSource, LeadSourceAdmin)
admin.site.register(LeadSourceUrlTracker,LeadSourceUrlTrackerAdmin)
