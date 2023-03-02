import datetime
import os
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect

##########
#Constants
##########
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #For OAuth Over HTTP
client_auth = "credentials.json"
requirements = ['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/userinfo.profile','openid'] #Required Scopes
redir_link = 'http://127.0.0.1:8000/rest/v1/calendar/redirect' #Redirect as specified in the task description
###########################
#First view: Authentication
###########################
@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_auth, scopes=requirements)
    flow.redirect_uri = redir_link
    oauth_link, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
    request.session['state'] = state
    return Response({"oauth_link": oauth_link})
###############################################
#Second View: Grabbing Events from Calendar API
###############################################
@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_auth, scopes=requirements, state=state)
    flow.redirect_uri = redir_link
    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials
    request.session['credentials'] = credentials_json(credentials)
    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')
    credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    calendar_list = service.calendarList().list().execute()
    calendar_id = calendar_list['items'][0]['id']
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_raw  = service.events().list(calendarId='primary', maxResults=10, timeMin=now, singleEvents=True, orderBy='startTime').execute()
    events = events_raw.get('items',[])
    if not events:
        return Response({"Error": "User does not have any events!"})
        
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        return Response({"name":event['summary'],
                          "timings":start 
                        })


def credentials_json(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}
