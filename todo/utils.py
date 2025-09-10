from django.utils.text import slugify

def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # slug already exists → add a number
        new_slug = f"{slug}-{qs.count()+1}"
        return slugify_instance_title(instance, save=save, new_slug=new_slug)
    
    instance.slug = slug
    if save:
        instance.save()
    return instance
