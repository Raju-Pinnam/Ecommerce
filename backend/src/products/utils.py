import os
import random

from django.utils.text import slugify
from AB_main.utils import random_string_generator

def filepath_split(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name, ext


def upload_file_path(instance, filepath):
    new_filename = random.randint(1, 582348942586)
    name, ext = filepath_split(filepath)
    title = instance.name
    title = slugify(title, allow_unicode=False)
    final_filename = f'{new_filename}{ext}'
    upload_path = f'products/{title}/{final_filename}'
    return upload_path


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{random_string_generator(size=5)}'
        return unique_slug_generator(instance, new_slug)
    return slug
