from django.shortcuts import render

# Create your views here.
def index(request):
	from .models import Project
	projects = Project.objects.all()
	context = {
		'title': 'Projects',
		'desc': 'Construction projects completed by Guy Hopkins Construction.',
		'pageclass': 'projects',
		'projects': projects
	}
	return render(request, 'projects/index.html', context)

def project(request, project_slug=None):
	context = {
		'project_slug': project_slug,
		'title': project_slug,
		'desc': 'project desc',
		'pageclass': 'project',
	}
	return render(request, 'projects/project.html', context)


def add(request):
	context = {
		'desc': 'project desc',
		'pageclass': 'add-project',
	}
	if request.method == "GET":
		return render(request, 'projects/add-edit.html', context)
	elif request.method == "POST":
		return render(request, 'projects/edit-complete', context)

def edit(request, project_slug=None):

	context = {
		'project_title': project_slug,
		'desc': 'project desc',
		'pageclass': 'add-project',
	}
	if request.method == "GET":
		return render(request, 'projects/add-edit.html', context)
	elif request.method == "POST":
		return render(request, 'projects/edit-complete', context)