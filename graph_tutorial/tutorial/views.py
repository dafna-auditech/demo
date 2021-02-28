from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .email_helper import send_users_report_email, send_users_control_email
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, \
    get_token
from tutorial.graph_helper import get_user, get_calendar_events, get_users
import dateutil.parser


# <HomeViewSnippet>
def home(request):
    context = initialize_context(request)

    return render(request, 'tutorial/home.html', context)


# </HomeViewSnippet>

# <InitializeContextSnippet>
def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


# </InitializeContextSnippet>

# <SignInViewSnippet>
def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url(request)
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


# </SignInViewSnippet>

# <SignOutViewSnippet>
def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))


# </SignOutViewSnippet>

# <CallbackViewSnippet>
def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_user(token)

    # Save token and user
    store_token(request, token)
    store_user(request, user)

    return HttpResponseRedirect(reverse('home'))
# </CallbackViewSnippet>


def users(request):
    context = initialize_context(request)

    users = get_users(request)
    context['usersList'] = users['value']

    # return JsonResponse(users)
    return render(request, 'tutorial/users.html', context)


def email_users_report(request):
    context = initialize_context(request)
    response = send_users_report_email(request)
    context['email'] = {'type': 'Users report',
               'status_code':response._status_code}
               # 'content':response._status_code}
    return render(request, 'tutorial/email-sent.html', context)
    # return HttpResponse()  # ,safe=False)


def email_users_control(request):
    context = initialize_context(request)
    response = send_users_control_email(request)
    context['email'] = {'type': 'Users-Control report',
               'status_code':response._status_code}
    return render(request, 'tutorial/email-sent.html', context)
    # return HttpResponse()  # ,safe=False)


def approve(request):
    if request.method== 'GET':
        context = initialize_context(request)

        # token = get_token(request)
        users = get_users(request)
        users_by_key = request.session['users_by_key']
        context['usersList'] = list(users_by_key.values())

        return render(request, 'tutorial/approve.html', context)
    elif request.method == 'POST':
        if request.POST.get('action') == 'Save':
            context = initialize_context(request)
            get_users(request)
            users_by_key = request.session['users_by_key']
            for key,user in users_by_key.items():
                if key in request.POST:
                    if request.POST[key] == 'on':
                        users_by_key[key]['selected'] = True
                else:
                    users_by_key[key]['selected'] = False
            request.session['users_by_key'] = users_by_key
            context['usersList'] = list(users_by_key.values())
            return render(request, 'tutorial/approve.html', context)
        else:
            return redirect('users-control-email')