from django.contrib.auth import logout
from django.shortcuts import redirect
from authentication.forms import UserAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model

user = get_user_model()


class UserLoginView(LoginView):
    '''
    Display the login form and handle the login action.
    '''
    authentication_form = UserAuthenticationForm
    template_name = 'login.html'


class UserLogoutView(TemplateView):
    '''
    View for logging out the user.
    '''
    def get(self, request):
        # Logout the user
        logout(request)
        return redirect('login')
    

class ValidateSessionToken(View):
    '''
    Class for validating session token and returning response in JSON format.
    '''

    def get(self, request):
        # Get the session token from the request
        session_token = request.GET.get('session_token')

        # Check if the session token exists in the Django session table
        session = Session.objects.filter(session_key=session_token).first()

        if session:
            # Check if the session has expired
            if session.expire_date > timezone.now():
                # Session token is valid
                response_data = {
                    'valid': True,
                    'message': 'Session token is valid.',
                    'expires': session.expire_date
                }
            else:
                # Session token has expired
                response_data = {
                    'valid': False,
                    'message': 'Session token has expired.'
                }
        else:
            # Session token does not exist
            response_data = {
                'valid': False,
                'message': 'Invalid session token.'
            }

        # Return the response in JSON format
        return JsonResponse(response_data)


class ContinueSession(View):
    def get(self):
        session_id = self.request.GET.get('sessionId')
        try:
            session = Session.objects.get(session_key=session_id)
            session_data = session.get_decoded()
            user_id = session_data.get('_auth_user_id')
            # Re-authenticate the user
            user = user.objects.get(id=user_id)
            self.request.user = user
            # Redirect to the desired page
            return redirect('/')
        except Session.DoesNotExist:
            return redirect('login')
