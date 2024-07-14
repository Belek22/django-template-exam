from django.db import models

class Product(models.Model):

    class Meta:
        verbose_name = 'протукт'
        verbose_name_plural = 'продукты'

    title = models.CharField(max_length=100, verbose_name='заголовок')
    price = models.FloatField(verbose_name='цена')
    image = models.ImageField(verbose_name = 'изображение', upload_to='news_images/', null=True)
    content = models.TextField(verbose_name='контент')
    category = models.ForeignKey('news.Category', on_delete=models.PROTECT, related_name='product', verbose_name='категория')
    tags = models.ManyToManyField('news.Tag', related_name='product', verbose_name='теги', blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='автор')

    def __str__(self):
        return f'{self.title}'
    
    
class Category(models.Model):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField(verbose_name='название', max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'
    

class Tag(models.Model):

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField(verbose_name='название', max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class ProductAttribute(models.Model):

    class Meta:
        verbose_name = 'атрибут новости'
        verbose_name_plural = 'атрибуты новостей'

    name = models.CharField(verbose_name='название', max_length=100)
    value = models.CharField(verbose_name='значение', max_length=100)
    product = models.ForeignKey('news.Product', on_delete=models.CASCADE, related_name='attributes', verbose_name='новость')

    def __str__(self):
        return f'{self.name} - {self.value}'


    
# class ProductImage(models.Model):
#
#     class Meta:
#         verbose_name = 'изображение продукта'
#         verbose_name_plural = 'изображения продуктов'
#
#     product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE , verbose_name='продукты')
#     image = models.ImageField(verbose_name='изображения', upload_to='news_images/')