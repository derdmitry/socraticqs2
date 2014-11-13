from django.conf.urls import patterns, include, url
from ct.views import *

urlpatterns = patterns('',
    url(r'^$', main_page, name='home'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^courses/(?P<course_id>\d+)/$', course, name='course'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/$',
        unit_concepts, name='unit_concepts'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/lessons/(?P<ul_id>\d+)/concepts/$',
        ul_concepts, name='ul_concepts'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<concept_id>\d+)/concepts/$',
        concept_concepts, name='concept_concepts'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<concept_id>\d+)/lessons/$',
        concept_lessons, name='concept_lessons'),
    url(r'^courses/(?P<course_id>\d+)/units/(?P<unit_id>\d+)/concepts/(?P<concept_id>\d+)/errors/$',
        concept_errors, name='concept_errors'),
    url(r'^concepts/(?P<concept_id>\d+)/edit/$', edit_concept,
        name='edit_concept'),
    # deprecated
    url(r'^teach/$', teach, name='teach'),
    url(r'^live/$', live_session, name='live'),
    url(r'^live/start/$', live_start, name='livestart'),
    url(r'^live/control/$', live_control, name='control'),
    url(r'^live/end/$', live_end, name='end'),
    url(r'^courses/(?P<course_id>\d+)/study/$', course_study,
        name='course_study'),
    url(r'^courselets/(?P<courselet_id>\d+)/$', courselet, name='courselet'),
    url(r'^courselets/(?P<courselet_id>\d+)/concept/$', courselet_concept,
        name='courselet_concept'),
    url(r'^concepts/$', concepts, name='concepts'),
    url(r'^questions/$', questions, name='questions'),
    url(r'^questions/(?P<ct_id>\d+)/$', question, name='question'),
    url(r'^questions/(?P<ct_id>\d+)/studylist/$', flag_question,
        name='flag_question'),
    url(r'^questions/(?P<ct_id>\d+)/respond/$', respond, name='respond'),
    url(r'^questions/(?P<ct_id>\d+)/concept/$', question_concept,
        name='question_concept'),
    url(r'^course/questions/(?P<cq_id>\d+)/$', course_question,
        name='course_question'),
    url(r'^course/questions/(?P<cq_id>\d+)/respond/$', respond_cq,
        name='respond_cq'),
    url(r'^course/questions/(?P<cq_id>\d+)/concept/$', cq_concept,
        name='cq_concept'),
    url(r'^course/lessons/(?P<cl_id>\d+)/$', course_lesson,
        name='course_lesson'),
    url(r'^resp/(?P<resp_id>\d+)/assess/$', assess, name='assess'),
    url(r'^lessons/(?P<lesson_id>\d+)/$', lesson, name='lesson'),
    url(r'^lessons/(?P<lesson_id>\d+)/concept/$', lesson_concept,
        name='lesson_concept'),
    url(r'^err/(?P<em_id>\d+)/$', error_model, name='error_model'),
    url(r'^err/(?P<em_id>\d+)/remedy/$', remedy_page, name='remedy'),
    url(r'^err/(?P<em_id>\d+)/remediate/$', submit_remedy, name='remediate'),
    url(r'^remediations/(?P<rem_id>\d+)/$', remediation, name='remediation'),
    url(r'^gloss/(?P<glossary_id>\d+)/write/$', glossary_page,
        name='write_glossary'),
    url(r'^gloss/(?P<glossary_id>\d+)/new_term/$', submit_term,
        name='new_term'),

)

