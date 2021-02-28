
# <FirstCodeSnippet>
from requests_oauthlib import OAuth2Session

from .auth_helper import get_token

graph_url = 'https://graph.microsoft.com/v1.0'


def get_user(token):
    graph_client = OAuth2Session(token=token)
    # Send GET to /me
    user = graph_client.get('{0}/me'.format(graph_url))
    # Return the JSON result
    return user.json()


# </FirstCodeSnippet>

# <GetCalendarSnippet>
def get_calendar_events(token):
    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results
    query_params = {
        '$select': 'subject,organizer,start,end',
        '$orderby': 'createdDateTime DESC'
    }

    # Send GET to /me/events
    events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)
    # Return the JSON result
    return events.json()


# </GetCalendarSnippet>

# <GetCalendarSnippet>
def get_users(req):

    token = get_token(req)
    graph_client = OAuth2Session(token=token)

    # Configure query parameters to
    # modify the results
    query_params = {
        '$select': 'subject,organizer,start,end',
        '$orderby': 'createdDateTime DESC'
    }
    if req.session.get('users') is None:
        # Send GET to /me/events
        users = graph_client.get('{0}/users'.format(graph_url))  # , params=query_params)
        # Return the JSON result
        users = users.json()
        for user in users['value']:
            if 'admin' in user['displayName']:
                user['isIssue'] = 'Generic user detected'
            else:
                user['selected'] = True

        users_by_key = {x['userPrincipalName']: x for x in users['value']}

        req.session['users_by_key'] = users_by_key
        req.session['users'] = users
        print('queried AD')
    else:
        users_by_key = req.session.get('users_by_key')
        users = req.session.get('users')

    return users
# </GetCalendarSnippet>
