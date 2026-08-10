from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import Project
from django.db.models import Q

# Create your views here.
def index(request, category=None, owner=None, designer=None):
	from .models import Project, Category
	projects = Project.objects.filter(parent_project__isnull=True, listed=True)
	cats = Category.objects.all()
	this_filter = False
	if category:
		from .models import Category
		projects = projects.filter(category__slug=category)
		pretext = "Category"
		this_filter = Category.objects.get(slug=category)
	if designer:
		from .models import ArchitectDesigner
		projects = projects.filter(architect_designer__slug=designer)
		pretext = "Architect / Engineer"
		this_filter = ArchitectDesigner.objects.get(slug=designer)
	if owner:
		from .models import Owner
		projects = projects.filter(Q(owner__slug=owner) | Q(second_owner__slug=owner))
		pretext = "Owner"
		this_filter = Owner.objects.get(slug=owner)

	if this_filter:
		filter_title = f"{pretext}: {this_filter.name}"
	else:
		filter_title = ""

	context = {
		'title': 'Projects',
		'desc': 'Construction projects completed by Guy Hopkins Construction.',
		'pageclass': 'projects',
		'projects': projects,
		'filter': this_filter,
		'filter_title': filter_title,
		'cats': cats,
	}
	return render(request, 'projects/index.html', context)

def project(request, project_slug=None):
	project = Project.objects.get(slug=project_slug)
	next_project = Project.objects.filter(parent_project__isnull=True, project_id__gt=project.project_id).order_by('project_id').first()
	prev_project = Project.objects.filter(parent_project__isnull=True, project_id__lt=project.project_id).order_by('project_id').first()
	first = Project.objects.filter(parent_project__isnull=True, listed=True, project_id__gt=0).order_by('project_id').first()
	last = Project.objects.filter(parent_project__isnull=True, listed=True, project_id__gt=0).order_by('project_id').last()
	if next_project is None:
		next_project = first
	if prev_project is None:
		prev_project = last

	child_project = Project.objects.filter(parent_project__project_id=project.project_id).first()

	if project.owner:
		owners_projects = Project.objects.filter(owner=project.owner).only('title')
		if owners_projects.count() > 1:
			project.owner.filter = True
	if project.second_owner:
		owners_projects = Project.objects.filter(owner=project.second_owner).only('title')
		if owners_projects.count() > 1:
			project.second_owner.filter = True
	if project.architect_designer:
		archs_projects = Project.objects.filter(architect_designer=project.architect_designer).only('title')
		if archs_projects.count() > 1:
			project.architect_designer.filter = True


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

#@login_required
#def add(request):
#	context = {
#		'title': 'Add Project',
#		'desc': 'project desc',
#		'pageclass': 'add-project',
#	}
#	if request.method == "GET":
#		return render(request, 'projects/add-edit.html', context)
#	elif request.method == "POST":
#		return render(request, 'projects/edit-complete', context)
#
#@login_required
#def edit(request, project_slug=None):
#	project = Project.objects.get(slug=project_slug)
#	context = {
#		'title': f'Edit Project: {project.title}',
#		'project_title': project.title,
#		'desc': 'editor for a Guy Hopkins ',
#		'pageclass': 'add-project',
#	}
#	if request.method == "GET":
#		return render(request, 'projects/add-edit.html', context)
#	elif request.method == "POST":
#		return render(request, 'projects/edit-complete', context)