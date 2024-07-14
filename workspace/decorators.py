from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from news.models import Product


def login_required(login_url='/'):

    def inner_func_as_args(func):

        def inner_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Вы должны пройти аутентификацию!')
                return redirect(login_url)
            return func(request, *args, **kwargs)

        return inner_func

    return inner_func_as_args


def own_news(func):

    def inner_func(request, id, *args, **kwargs):
        user = request.user
        news = get_object_or_404(Product, id=id)
        if user != news.author:
            messages.warning(request, 'Вы не можете совершать никаких действий, это не ваши новости')
            return redirect('/workspace/')

        return func(request, id, *args, **kwargs)

    return inner_func