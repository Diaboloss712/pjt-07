from django.http.response import JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.forms import AuthenticationForm  # AuthenticationForm import 추가

from .forms import CustomUserCreationForm, CustomUserChangeForm

# 로그인 처리
@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃 처리
@require_POST
def logout(request):
    auth_logout(request)
    return redirect('books:index')

# 회원가입 처리
def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            selected_categories = form.cleaned_data.get('interested_genres')
            if selected_categories:
                user.interested_genres.set(selected_categories)
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# 프로필 조회
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)  # 예외 처리 추가
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

# 팔로우/언팔로우 처리
@require_POST
@login_required
def follow(request, user_pk):
    if request.user.is_authenticated:
        User = get_user_model()
        person = User.objects.get(pk=user_pk)
        if request.user != person:
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
                is_follow = False
            else:
                person.followers.add(request.user)
                is_follow = True
            followers_count = person.followers.count()
            context = {
                'followed': is_follow,
                'followers_count': followers_count,
            }
            return JsonResponse(context)
    return redirect('accounts:profile', person.username)