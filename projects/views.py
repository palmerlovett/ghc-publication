from django.shortcuts import render
from django.utils.safestring import mark_safe

# Create your views here.
def index(request):
	from .models import Project
	projects = Project.objects.filter(parent_project__isnull=True)
	context = {
		'title': 'Projects',
		'desc': 'Construction projects completed by Guy Hopkins Construction.',
		'pageclass': 'projects',
		'projects': projects
	}
	return render(request, 'projects/index.html', context)

def project(request, project_slug=None):
	from .models import Project
	project = Project.objects.get(slug=project_slug)
	next_project = Project.objects.filter(parent_project__isnull=True, project_id__gt=project.project_id).order_by('project_id').first()
	prev_project = Project.objects.filter(parent_project__isnull=True, project_id__lt=project.project_id).order_by('project_id').first()
	first = Project.objects.filter(parent_project__isnull=True, project_id__gt=0).order_by('project_id').first()
	last = Project.objects.filter(parent_project__isnull=True, project_id__gt=0).order_by('project_id').last()
	if next_project is None:
		next_project = first
	if prev_project is None:
		prev_project = last

	child_project = Project.objects.filter(parent_project__project_id=project.project_id).first()



	context = {
		'project_slug': project_slug,
		'next': next_project,
		'prev': prev_project,
		'project': project,
		'title': project.title,
		'desc': f'{project.title} details and specifications',
		'pageclass': 'projects project',
		'child_project': child_project
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