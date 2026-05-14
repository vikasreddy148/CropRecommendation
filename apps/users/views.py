from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    ContactForm
)
from .models import UserProfile


def home_view(request):
    """
    Home page view - shows dashboard if authenticated, otherwise landing page.
    """
    if request.user.is_authenticated:
        return dashboard_view(request)
    return landing_view(request)


def landing_view(request):
    """
    Landing page for non-authenticated users.
    """
    return render(request, 'landing.html')


@login_required
def dashboard_view(request):
    """
    Dashboard view for authenticated users.
    """
    # Import here to avoid circular imports
    from apps.farms.models import Farm, Field, CropHistory
    from apps.recommendations.models import Recommendation
    
    # Get user's farms
    farms = Farm.objects.filter(user=request.user)
    total_farms = farms.count()
    
    # Get total fields
    fields = Field.objects.filter(farm__user=request.user)
    total_fields = fields.count()
    
    # Get total recommendations
    recommendations = Recommendation.objects.filter(user=request.user)
    total_recommendations = recommendations.count()
    
    # Get total crop history records
    crop_history = CropHistory.objects.filter(field__farm__user=request.user)
    total_crop_history = crop_history.count()
    
    # Get recent recommendations (last 5)
    recent_recommendations = recommendations.order_by('-created_at')[:5]
    
    context = {
        'total_farms': total_farms,
        'total_fields': total_fields,
        'total_recommendations': total_recommendations,
        'total_crop_history': total_crop_history,
        'recent_recommendations': recent_recommendations,
    }
    
    return render(request, 'dashboard.html', context)


def register_view(request):
    """
    User registration view (Modal only).
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}! You can now log in.')
            next_url = request.GET.get('next', '/')
            if next_url == request.path:
                next_url = '/'
            return redirect(f"{next_url}?auth=login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    # Clean up field name for display
                    clean_field = field.replace('_', ' ').title()
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{clean_field}: {error}")
            
            referer = request.META.get('HTTP_REFERER', '/')
            if '/register/' in referer:
                referer = '/'
            
            # Preserve next parameter
            next_param = request.GET.get('next', '')
            query_string = f"?auth=register"
            if next_param:
                query_string += f"&next={next_param}"
                
            # Avoid appending multiple query strings
            if '?' in referer:
                return redirect(f"{referer.split('?')[0]}{query_string}")
            return redirect(f"{referer}{query_string}")
    else:
        next_param = request.GET.get('next', '')
        query_string = f"/?auth=register"
        if next_param:
            query_string += f"&next={next_param}"
        return redirect(query_string)


def login_view(request):
    """
    User login view (Modal only).
    """
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next page if specified, otherwise to dashboard
            next_url = request.GET.get('next', 'users:dashboard')
            if next_url == request.path:
                next_url = '/'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            
            referer = request.META.get('HTTP_REFERER', '/')
            if '/login/' in referer:
                referer = '/'
                
            # Preserve next parameter
            next_param = request.GET.get('next', '')
            query_string = f"?auth=login"
            if next_param:
                query_string += f"&next={next_param}"
                
            # Avoid appending multiple query strings
            if '?' in referer:
                return redirect(f"{referer.split('?')[0]}{query_string}")
            return redirect(f"{referer}{query_string}")
    else:
        # If it's a GET request (e.g. redirected by @login_required), redirect to home with modal trigger
        next_url = request.GET.get('next', '')
        redirect_url = f"/?auth=login"
        if next_url:
            redirect_url += f"&next={next_url}"
        return redirect(redirect_url)


@login_required
def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """
    User profile view and edit.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
def change_password_view(request):
    """
    Change password view.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('users:profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'users/change_password.html', {'form': form})


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


def about_us_view(request):
    """
    About Us page view.
    """
    return render(request, 'users/about_us.html')


def contact_us_view(request):
    """
    Contact Us page view with contact form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real application, you would send an email here
            # For now, we'll just show a success message
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('users:contact_us')
    else:
        # Pre-fill form if user is authenticated
        if request.user.is_authenticated:
            form = ContactForm(initial={
                'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email
            })
        else:
            form = ContactForm()
    
    return render(request, 'users/contact_us.html', {'form': form})
