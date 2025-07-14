from django.utils.text import slugify

def slug_field(field:str):
    return slugify(field) if len(field) <=40 else slugify(field[:40])