from django.shortcuts import render, HttpResponse


def category_list(request):

    context = {}
    context['categories'] = [
        'Category 1',
        'Category 2',
        'Category 3'
    ]
    context['username'] = 'Vasya'
    return render(request, 'categories/categories_list.html', context)


def category_detail(request, category_id=None):

    context = {}
    context['category'] = {
        'name': 'Category 1',
        'id' : category_id,
    }
    context['username'] = 'Vasya'
    return render(request, 'categories/category_data.html', context)
