from .forms import UserLoginForm, UserRegistrationForm

def auth_forms(request):
    """
    Context processor to provide login and registration forms globally.
    Allows authentication modals to be rendered on any page.
    """
    return {
        'login_form': UserLoginForm(),
        'register_form': UserRegistrationForm()
    }
