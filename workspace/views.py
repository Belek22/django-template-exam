from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from news.models import Product, Category, Tag
from workspace.forms import ProductForm, LoginForm, RegisterForm, ChangeProfileForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from workspace.decorators import login_required, own_news
from news.filters import ProductFilter
from django.db.models import Q
from django.contrib.auth.hashers import make_password


@login_required(login_url='/auth/login/')
def workspace(request):
    news = Product.objects.filter(author=request.user).order_by('title')

    search = request.GET.get('search')

    if search:
        news = news.filter(
            Q(title__icontains=search) |
            Q(category__name__icontains=search)
        )

    filter_set = ProductFilter(request.GET, queryset=news)
    paginator = Paginator(filter_set.qs, 6)
    page = int(request.GET.get('page', 1))
    news = paginator.get_page(page)

    return render(request, 'workspace/index.html', {'news': news, 'filter': filter_set})


@login_required()
def create_news(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, f'Продукт "{news.title}" успешно создан!')
            return redirect('/workspace/')
        messages.error(request, f'Исправьте ошибки ниже')

    return render(request, 'workspace/create_news.html', {'form': form})


@login_required()
@own_news
def update_news(request, id):
    news = Product.objects.get(id=id)
    form = ProductForm(instance=news)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, f'Продукт "{news.title}" успешно изменен!')
            return redirect('/workspace/')
        messages.error(request, f'Исправьте ошибки ниже')

    return render(request, 'workspace/update_news.html', {'form': form, 'news': news})


@login_required()
@own_news
def delete_news(request, id):
    news = get_object_or_404(Product, id=id)
    name = news.title
    news.delete()
    messages.success(request, f'Продукт "{name}" успешно удален!')
    return redirect('/workspace/')


def login_profile(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    message = None

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request,
                                 f'Добро пожаловать в рабочее пространство "{user.first_name} {user.last_name}"')
                return redirect('/workspace/')

            else:
                messages.error(request, f'Пользователь не существует или пароль неверен')

    return render(request, 'auth/login.html', {'form': form, 'message': message})


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать в рабочее пространство "{user.first_name} {user.last_name}"')
            return redirect('/workspace/')

        messages.error(request, f'Исправьте ошибки ниже')

    return render(request, 'auth/register.html', {'form': form})


@login_required()
def change_profile(request):
    form = ChangeProfileForm(instance=request.user)

    if request.method == 'POST':
        form = ChangeProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваш профиль успешно изменен!')
            return redirect('/workspace/')

        messages.error(request, f'Исправьте ошибки ниже')

    return render(request, 'auth/change_profile.html', {'form': form})


@login_required()
def change_password(request):
    form = ChangePasswordForm()

    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user = request.user
            # user.password = make_password(new_password)
            user.set_password(new_password)
            user.save()

            login(request, user)

            messages.success(request, f'Ваш пароль был изменен!')
            return redirect('/workspace/')

        messages.error(request, f'Ваш пароль не верный или не совподает')

    return render(request, 'auth/change_password.html', {'form': form})
