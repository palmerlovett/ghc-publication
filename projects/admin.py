from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Photo, Project, Category, ArchitectDesigner, Owner
from django import forms
from django.conf import settings

from django.db.models import Q

class ProjectOwnerFilter(admin.SimpleListFilter):
	"""Custom admin filter to check both owner and second_owner fields."""
	title = 'Project Owner'  # The sidebar header name
	parameter_name = 'any_owner'  # The URL query parameter

	def lookups(self, request, model_admin):
		"""Returns a list of tuples containing (owner_id, owner_display_name)."""
		owners = Owner.objects.all()
		return [(owner.owner_id, str(owner)) for owner in owners]

	def queryset(self, request, queryset):
		"""Filters the project list using an OR query on both owner fields."""
		if self.value():
			return queryset.filter(
				Q(owner_id=self.value()) | Q(second_owner_id=self.value())
			)
		return queryset


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'desc_head')
	list_filter = ("category", "architect_designer", ProjectOwnerFilter, "featured", "listed")

	def get_queryset(self, request):
		return super().get_queryset(request).select_related('owner', 'second_owner')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('photo_id', 'file')

@admin.register(ArchitectDesigner)
class ArchitectDesignerAdmin(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
	list_display = ('name',)