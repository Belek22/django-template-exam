from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from news.models import Product, Category
from django.db.models import Q
from news.filters import ProductFilter

def main(request):
    query = request.GET.get('search')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query)
        )

    filter_set = ProductFilter(request.GET, queryset=products)

    paginator = Paginator(filter_set.qs, 6)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()

    return render(request, 'index.html', {'news': page_obj, 'filter': filter_set})


def detail_news(request, pk):
    news = get_object_or_404(Product, pk=pk)
    return render(request, 'detail_news.html', {'news': news})


def news_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    news = Product.objects.filter(category=category).order_by('title')

    paginator = Paginator(news, 8)
    page = int(request.GET.get('page', 1))
    news = paginator.get_page(page)

    return render(request, 'index.html', {'news': news, 'category': category})