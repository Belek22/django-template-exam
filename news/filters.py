import django_filters
from django import forms

from django.contrib.auth.models import User

from news.models import Product, Category, Tag


class ProductFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'mb-3 mt-1'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-select w-full mb-3 border border-gray-500 rounded-md'}))
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-select w-full border border-gray-500 rounded-md'}))

    class Meta:
        model = Product
        fields = ('tags', 'category', 'author')