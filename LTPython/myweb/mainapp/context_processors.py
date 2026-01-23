from .models import Category

def categories_processor(request):
    """Make categories available in all templates"""
    return {
        'listCategory': Category.objects.all()
    }