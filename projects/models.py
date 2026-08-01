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

class Owner(models.Model):
	owner_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.name}'

class ArchitectDesigner(models.Model):
	a_d_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.name}'

class Project(models.Model):
	project_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100, default="")
	slug = models.CharField(max_length=100, default="", blank=True)

	desc = models.TextField(default="")
	
	owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
	architect_designer = models.ForeignKey(ArchitectDesigner, on_delete=models.SET_NULL, null=True)
	project_value = models.CharField(max_length=12, default="")
	start_date = models.DateField(default="", blank=True, null=True)
	completion_date = models.DateField(default="", blank=True, null=True)

	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

	listed = models.BooleanField(default=True)
	featured = models.BooleanField(default=True)
	additional_project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)

	photo_1 = models.ForeignKey('projects.ProjectPhoto', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_1')
	photo_2 = models.ForeignKey('projects.ProjectPhoto', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_2')
	photo_3 = models.ForeignKey('projects.ProjectPhoto', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_3')
	photo_4 = models.ForeignKey('projects.ProjectPhoto', on_delete=models.CASCADE, blank=True, default="", null=True, related_name='Photo_4')

	class Meta:
		ordering = ['project_id']

	def save(self, *args, **kwargs):
		if self.slug == "":
			self.slug = slugify(self.title)

		super().save(*args, **kwargs)
		if self.photo_1:
			self.photo_1.project = self
			self.photo_1.save()
		if self.photo_2:
			self.photo_2.project = self
			self.photo_2.save()
		if self.photo_3:
			self.photo_3.project = self
			self.photo_3.save()
		if self.photo_4:
			self.photo_4.project = self
			self.photo_4.save()

	def __str__(self):
		return f"{self.title}"


class Photo(models.Model):
	photo_id = models.AutoField(primary_key=True)

	file = models.ImageField(upload_to="projects_tmp")

	def delete(self, *args, **kwargs):
		print(f'deleting file when photo row is deleted')
		from django.core.files.storage import default_storage
		path = self.file.path
		print(f'delete path: {path}')
		default_storage.delete(path)
		print(f'file deleted')
		print(f'continue to deleting row')
		super().delete(*args, **kwargs)

	def __str__(self):
		return self.file.name

class ProjectPhoto(models.Model):
	photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
	order = models.IntegerField(default=1)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

	def rename_photo(self):
		file = self.photo.file
		filename, file_extension = os.path.splitext(file.path)
		new_filename = f"projects/{slugify(self.project.title)}-{self.photo.photo_id}{file_extension}"
		new_path = os.path.join(settings.MEDIA_ROOT, new_filename)

		print(f'checking if photo file needs to be moved and renamed from projects_tmp')
		print(f'self.file.path: {file.path} new_path: {new_path}')
		print(f"comparing the two to determine if we need to save...")
		if file.path == new_path:
			print("photo has already been saved. path: {file.path}")
		else:
			print(f'photo not yet saved')
			print(f"current filepath: {file.path}, new filepath: {new_path}")
			#print(f"os.rename file.path: {file.path} to new_path: {new_path}")
			#os.rename(file.path, new_path)
			print(f'changing file.name')
			file.name = new_filename
			print(f'setting self.photo.file as file and saving self.photo')
			self.photo.file = file
			self.save(update_fields=['photo'])
			print(f"current filepath (self.photo): {self.photo.file.path}, new filepath: {new_path}")

			print(f"saved photo to new path")

	def save(self, *args, **kwargs):
		if self.project:
			self.rename_photo()
		super().save(*args, **kwargs)


	def __str__(self):
		return f'{self.photo.file.name}'

	