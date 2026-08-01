from django.shortcuts import render


def home(request):
    from projects.models import Project
    featured = Project.objects.filter(featured=True, parent_project__isnull=True)[:5]
    context = {
        'title': 'Home',
        'desc': 'Welcome to Guy Hopkins Construction Co., Inc.',
        'pageclass': 'homepage',
        'featured': featured,
    }
    return render(request, 'web/pages/home.html', context)


def about(request):
    context = {
        'title': 'About',
        'desc': 'Learn about Guy Hopkins Construction Co., Inc.',
        'pageclass': 'about',
    }
    return render(request, 'web/pages/about.html', context)


def services(request):
    context = {
        'title': 'Services',
        'desc': 'Services offered by Guy Hopkins Construction Co., Inc.',
        'pageclass': 'services',
    }
    return render(request, 'web/pages/services.html', context)


def contact(request):
    context = {
        'title': 'Contact',
        'desc': 'Contact Guy Hopkins Construction Co., Inc.',
        'pageclass': 'contact',
    }
    return render(request, 'web/pages/contact.html', context)
