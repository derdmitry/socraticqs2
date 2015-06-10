from django.conf.urls import url, patterns


urlpatterns = patterns(
    '',
    url(r'(^$|^unit/(?P<unit_id>\d+)/$)', 'lti.views.lti_init', name='lti_init'),
    url(r'^choice_course_source/$', 'lti.views.choice_course_source', name='choice_course_source'),
)
