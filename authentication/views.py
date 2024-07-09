from django.contrib.auth import logout
from django.shortcuts import redirect
from authentication.forms import UserAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


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
