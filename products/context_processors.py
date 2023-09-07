from .models import Category


def category(self):
    category = Category.objects.all()
    context = {
        'category_list': category
    }
    return context