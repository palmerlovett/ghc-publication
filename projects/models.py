from django.db import models
from django.conf import settings
import os
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=35)

	def __str(self):
		return f'{self.name}'

	class Meta:
		ordering = ['name']
		verbose_name_plural = "categories"

class Owner(models.Model):
	owner_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.name}'

	class Meta:
		ordering = ['name']

class ArchitectDesigner(models.Model):
	a_d_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.name}'

	class Meta:
		ordering = ['name']

class Project(models.Model):
	project_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100, default="",
		help_text="The title of this project (required)")

	parent_project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True,
		limit_choices_to={"parent_project": None},
		help_text="If this is the second phase of a previous project, please select the previous project above (optional: use this or a slug)")
	slug = models.CharField(max_length=100, default="", blank=True,
		help_text='Creates the url of your project, guyhopkins.com/projects/your-project-slug (optional: leave blank when a Parent Project is selected) ')

	desc_head = models.CharField(max_length=100, blank=True, null=True,
		help_text="The header above the project description. Especially useful with parent and child projects (optional)")
	desc = models.TextField(default="", blank=True, null=True,
		help_text="The full description of this project (optional)")
	
	owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True,
		help_text="The owner of the finished project (optional)")
	second_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True, related_name="second_owner",
		help_text="A second owner (optional)")
	architect_designer = models.ForeignKey(ArchitectDesigner, on_delete=models.SET_NULL, null=True, blank=True,
		help_text="Architect or Design firm (optional)")
	project_value = models.CharField(max_length=12, default="", null=True, blank=True,
		help_text="Please use commas and no dollar sign")
	start_date = models.DateField(default="", blank=True, null=True)
	completion_date = models.DateField(default="", blank=True, null=True)

	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
		help_text="for future filters on the projects index (optional)")

	featured = models.BooleanField(default=False,
		help_text="in the list of projects to be featured on the homepage (the first five featured will show)")

	photo_1 = models.ForeignKey('projects.Photo', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_1',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")
	photo_2 = models.ForeignKey('projects.Photo', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_2',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")
	photo_3 = models.ForeignKey('projects.Photo', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_3',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")
	photo_4 = models.ForeignKey('projects.Photo', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_4',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")

	class Meta:
		ordering = ['project_id']

	def save(self, *args, **kwargs):
		if self.slug:
			self.slug = slugify(self.slug)

		super().save(*args, **kwargs)
		
		if self.slug:
			if self.photo_1:
				self.photo_1.rename_photo(project_title=self.title)
			if self.photo_2:
				self.photo_2.rename_photo(project_title=self.title)
			if self.photo_3:
				self.photo_3.rename_photo(project_title=self.title)
			if self.photo_4:
				self.photo_4.rename_photo(project_title=self.title)

	def __str__(self):
		addition = ", addition" if self.parent_project else ""
		return f"{self.title}{addition}"


class Photo(models.Model):
	photo_id = models.AutoField(primary_key=True)
	file = models.ImageField(upload_to="projects_tmp")

	def rename_photo(self, project_title):
		file = self.file
		filename, file_extension = os.path.splitext(file.path)
		new_filename = f"projects/{slugify(project_title)}-{self.photo_id}{file_extension}"
		new_path = os.path.join(settings.MEDIA_ROOT, new_filename)

		print(f'checking if photo file needs to be moved and renamed from projects_tmp')
		print(f'self.file.path: {file.path} new_path: {new_path}')
		print(f"comparing the two to determine if we need to save...")
		if file.path == new_path:
			print("photo has already been saved. path: {file.path}")
		else:
			print(f'photo not yet saved')
			print(f"current filepath: {file.path}, new filepath: {new_path}")
			print(f"os.rename file.path: {file.path} to new_path: {new_path}")
			os.rename(file.path, new_path) #not needed ??, self.photo.save(update_fields) works better
			print(f'changing file.name')
			file.name = new_filename
			print(f'setting self.photo.file as file and saving self.photo')
			self.file = file
			self.save(update_fields=['file'])
			print(f"current filepath (self.photo): {self.file.path}, new filepath: {new_path}")

			print(f"saved photo to new path")

	def delete(self, *args, **kwargs):
		print(f'deleting file when photo row is deleted')
		from django.core.files.storage import default_storage
		path = self.file.path
		print(f'delete path: {path}')
		default_storage.delete(path)
		print(f'file deleted')
		print(f'continue to deleting row')
		super().delete(*args, **kwargs)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)


	def __str__(self):
		return self.file.name
	