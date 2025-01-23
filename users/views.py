from django.shortcuts import render
from .forms import UserRegistrationForm

def register(request):
    """View to handle user registration."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            return redirect('homepage') 
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})