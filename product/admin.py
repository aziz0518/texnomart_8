from django.contrib import admin
from product.models import Category, Product, Image, Attribute, AttributeValue, ProductAttribute, Comment


# admin.site.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug']
    prepopulated_fields = {'slug': ('product_name',)}


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):

    list_display = ['category_name', 'slug']
    populate_fields = {'slug': ('category_name',)}


admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Comment)