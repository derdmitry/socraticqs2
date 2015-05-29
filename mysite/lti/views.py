import pickle
import oauth2
import json
import logging
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from ims_lti_py.tool_provider import DjangoToolProvider
from django.shortcuts import render_to_response, redirect

from lti import app_settings as settings
from lti.models import LTIUser, CourseRef


ROLES_MAP = {
    'Instructor': 'prof',
    'Leaner': 'student',
}

MOODLE_PARAMS = (
    'user_id',
    'context_id',
    'lis_person_name_full',
    'lis_person_name_given',
    'lis_person_name_family',
    'tool_consumer_instance_guid',
    'lis_person_contact_email_primary',
    'tool_consumer_info_product_family_code',
)

LOGGER = logging.getLogger('lti_debug')


@csrf_exempt
def lti_init(request, unit_id=None):
    """LTI init view

    Analyze LTI POST request to start LTI session.

    :param unit_id: unit id from lunch url
    """
    if settings.LTI_DEBUG:
        LOGGER.info(request.META)
        LOGGER.info(request.POST)
    session = request.session
    # Code from ims_lti_py_django example
    session.clear()
    try:
        consumer_key = settings.CONSUMER_KEY
        secret = settings.LTI_SECRET

        tool = DjangoToolProvider(consumer_key, secret, request.POST)
        is_valid = tool.is_valid_request(request)
        session['target'] = '_blank'
    except (oauth2.MissingSignature,
            oauth2.Error,
            KeyError,
            AttributeError) as e:
        is_valid = False
        session['message'] = "{}".format(e)

    session['is_valid'] = is_valid
    session['LTI_POST'] = pickle.dumps({k: v for (k, v) in request.POST.iteritems()})

    if settings.LTI_DEBUG:
        LOGGER.info('session: is_valid = {}'.format(session.get('is_valid')))
        if session.get('message'):
            LOGGER.info('session: message = {}'.format(session.get('message')))
    if not is_valid:
        return render_to_response('lti/error.html', RequestContext(request))

    return lti_redirect(request, unit_id)


def lti_redirect(request, unit_id=None):
    """Create user and redirect to Course

    |  Create LTIUser with all needed link to Django user
    |  and/or UserSocialAuth.
    |  Finally login Django user and redirect to Course

    :param unit_id: unit id from lunch url
    """
    request_dict = pickle.loads(request.session['LTI_POST'])

    context_id = request_dict.get('context_id')
    course_ref = CourseRef.objects.filter(context_id=context_id).first()
    consumer_name = request_dict.get('tool_consumer_info_product_family_code', 'lti')
    user_id = request_dict.get('user_id', None)
    roles = ROLES_MAP.get(request_dict.get('roles', None), 'student')

    if not user_id:
        return render_to_response('lti/error.html', RequestContext(request))

    if course_ref:
        course_id = course_ref.course.id
    else:
        return redirect(reverse('ct:home'))

    user, created = LTIUser.objects.get_or_create(user_id=user_id,
                                                  consumer=consumer_name,
                                                  course_id=course_id)
    extra_data = {k: v for (k, v) in request_dict.iteritems()
                  if k in MOODLE_PARAMS}
    user.extra_data = json.dumps(extra_data)
    user.save()

    if not user.is_linked:
        user.create_links()

    user.login(request)
    user.enroll(roles, course_id)

    if user.is_enrolled(roles, course_id):
        # Redirect to course or unit page considering users role
        if not unit_id:
            dispatch = 'ct:course_student'
            if roles == 'prof':
                dispatch = 'ct:course'
            return redirect(reverse(dispatch, args=(course_id,)))
        else:
            dispatch = 'ct:study_unit'
            if roles == 'prof':
                dispatch = 'ct:unit_tasks'
            return redirect(reverse(dispatch, args=(course_id, unit_id)))
    else:
        return redirect(reverse('ct:home'))
