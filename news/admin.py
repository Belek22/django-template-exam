from django.contrib import admin
from .models import Product, ProductAttribute, Category, Tag
from django.utils.safestring import mark_safe

class ProductAttributeTabularInline(admin.TabularInline):
    model = ProductAttribute
#
# class ProductImageTabularInline(admin.TabularInline):
#     model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'author')
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    list_filter = ('category', 'tags', 'author')
    # readonly_fields = ('get_full_image',)
    filter_horizontal = ('tags',)
    inlines = [ProductAttributeTabularInline,]

    @admin.display(description='Изображение')
    def get_image(self, product: Product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="150px">')

    # @admin.display(description='Изображение')
    # def get_full_image(self, product: Product):
    #     product_image = product.images.first()
    #     return mark_safe(f'<img src="{product_image.image.url}" width="20%">')
    #

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
