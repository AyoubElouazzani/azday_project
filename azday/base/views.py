from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib import messages
from .models import Business , Review
from .forms import CustomUserCreationForm , BusinessForm 
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    businesses = Business.objects.all()
    context = {'businesses': businesses}
    return render(request,'base/index.html',context)


def business_profile(request, business_id):
    # Fetch the business details based on the ID
    business = get_object_or_404(Business, id=business_id)
    # Fetch reviews for the business (if a Review model exists)
    reviews = Review.objects.filter(business=business).order_by('-created_at')
    # Context to pass data to the template
    context = {
        'business': business,
        'reviews': reviews,
    }
    return render(request, 'base/business_detail.html', context)


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a 'home' page after login
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'base/signin.html')


def registerPage(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Error in registration. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'base/signup.html')



def logoutuser(request):
    logout(request)
    return redirect('home')



@login_required(login_url='login')
def business_create_view(request):
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect('home')  # Redirect to a list view or success page
    else:
        form = BusinessForm()

    return render(request, 'base/business_form.html', {'form': form})
