
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from product.models import Category, Product
from django.dispatch import receiver
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL, BASE_DIR
import os
import json


@receiver(pre_save, sender=Category)
def pre_save_category(sender, instance, **kwargs):
    print('before save category')


@receiver(post_save, sender=Category)
def post_save_category(sender, instance, created, **kwargs):
    if created:
        print('category created')
        subject = 'Category created'
        message = 'Category created successfully and verificated from Admin << Asadbek >>'
        from_email = DEFAULT_FROM_EMAIL
        to = 'asadjon752@gmail.com'
        send_mail(subject, message, from_email, [to,], fail_silently=False)
    else:
        print('category updated')


@receiver(pre_delete, sender=Category)
def pre_delete_category(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'core/delete_categories', f'category_{instance.id}.json')

    category_data = {
        'id': instance.id,
        'category_name': instance.category_name,
        'slug': instance.slug
    }


    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file, indent=4)

    print('Category saved json file before deleted')


@receiver(pre_save, sender=Product)
def pre_save_product(sender, instance, **kwargs):
    print('before save product')


@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print('Product created')
        subject = 'Product created'
        message = 'Category created successfully and verificated from Admin << Asadbek >>'
        from_email = DEFAULT_FROM_EMAIL
        to = 'jasurmavloonov24@gmail.com'
        send_mail(subject, message, from_email, [to, ], fail_silently=False)
    else:
        print('Product updated')


@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'core/delete_products', f'category_{instance.id}.json')

    product_data = {
        'id': instance.id,
        'product_name': instance.product_name,
        'slug': instance.slug
    }


    with open(file_path, 'w') as json_file:
        json.dump(product_data, json_file, indent=4)

    print('Product saved json file before deleted')
