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
		help_text="For future filters on the projects index (optional)")

	featured = models.BooleanField(default=False,
		help_text="In the list of projects to be featured on the homepage (the first five featured will show)")

	listed = models.BooleanField(default=True,
		help_text="Whether or not this page is listed on the Projects index page (it will still accessible by url)")



	photo_1 = models.ForeignKey('projects.Photo', on_delete=models.SET_NULL, blank=True, default="", null=True, related_name='Photo_1',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")
	photo_2 = models.ForeignKey('projects.Photo', on_delete=models.SET_NULL, blank=True, default="", null=True, related_name='Photo_2',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")
	photo_3 = models.ForeignKey('projects.Photo', on_delete=models.SET_NULL, blank=True, default="", null=True, related_name='Photo_3',
		help_text="Choose an existing photo or add and upload a new one with the plus button (optional)")
	photo_4 = models.ForeignKey('projects.Photo', on_delete=models.SET_NULL, blank=True, default="", null=True, related_name='Photo_4',
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
		if self.parent_project:
			addition = ', {self.desc_head} addition'
			return f"{self.title}{addition}"
		return self.title


class Photo(models.Model):
	from imagefield.fields import ImageField
	from django.core.files.storage import FileSystemStorage

	# Force the storage class to use your absolute path explicitly
	#custom_storage = FileSystemStorage(
	#	location=settings.MEDIA_ROOT,  # Pins it to /home/runner/workspace/media/
	#	base_url=settings.MEDIA_URL
	#)
	photo_id = models.AutoField(primary_key=True)
	file = ImageField(upload_to="",
		#storage=custom_storage,
		formats={"thumb": ["default", ("crop", (300, 200))],
						 "desktop": ["default", ("thumbnail", (660, 999))],},
						 auto_add_fields=True)

	def generate_file_slug(self, project_title=None, format=None):
		filename, file_extension = os.path.splitext(self.file.path)
		new_filename = f"projects/{slugify(project_title)}-{self.photo_id}"
		if (format): new_filename += f".{format}"
		new_filename += f"{file_extension}"
		new_path = os.path.join(settings.MEDIA_ROOT, new_filename.lstrip('/'))

		return new_path

	@property
	def thumb_path(self):
		if self.file:
			# 1. Ask django-imagefield for the raw internal storage path
			relative_path = self.file.process('thumb')
			# 2. Return the absolute server filesystem location
			return os.path.join(settings.MEDIA_ROOT, relative_path.lstrip('/'))
		return None

	@property
	def desktop_path(self):
		if self.file:
			# 1. Ask django-imagefield for the raw internal storage path
			relative_path = self.file.process('desktop').lstrip('/')
			# 2. Return the absolute server filesystem location
			return os.path.join(settings.MEDIA_ROOT, relative_path.lstrip('/'))
		return None

	@property
	def thumb_url(self):
		name, ext = os.path.splitext(self.file.name)
		return f"{name}.thumb{ext}"

	@property
	def desktop_url(self):
		name, ext = os.path.splitext(self.file.name)
		return f"{name}.desktop{ext}"


	def rename_photo(self, project_title):
		from django.core.files.base import ContentFile
		file = self.file
		print(f'')
		print(f'file.path: {file.path}, file.url: {file.url}, file.thumb: {file.thumb}, file.desktop: {file.desktop}')
		print(f'')


		old_thumb_path = self.thumb_path
		print(f"old_thumb_path: {old_thumb_path}")
		new_thumb_path = self.generate_file_slug(project_title, 'thumb')
		print(f'changing file.thumb')
		print('moving thumb w/os.rename {old_thumb}, {new_thumb_path}')
		os.rename(old_thumb_path, new_thumb_path)


		old_desktop_path = self.desktop_path
		print(f"old_desktop_path: {old_desktop_path}")
		new_desktop_path = self.generate_file_slug(project_title, 'desktop')
		print(f"moving file w/os.rename {old_desktop_path}, {new_desktop_path}")
		os.rename(old_desktop_path, new_desktop_path)


		new_path = self.generate_file_slug(project_title)
		os.rename(self.file.path, new_path)
		new_name = new_path.replace(settings.MEDIA_ROOT, "")
		Photo.objects.filter(pk=self.pk).update(file=new_name)
		self.file.name = new_name

#		print(f'setting self.photo.file as file and saving self.photo')
#		self.file = file
		print(f'self.file.desktop {self.file.desktop}')

		#print(f"os.rename file.path: {file.path} to new_path: {new_path}")
		print(f'')
		#print(f'file.path: {file.path}, file.url: {file.url}, file.thumb: {file.thumb}, file.desktop: {file.desktop}')
		print(f'')

	def delete(self, *args, **kwargs):
		print(f'deleting file when photo row is deleted')
		from django.core.files.storage import default_storage
		path = self.file.path
		print(f'delete path: {path}')
		default_storage.delete(path)
		print(f'file deleted')
		print(f'continue to deleting row')
		super().delete(*args, **kwargs)

#	def save(self, *args, **kwargs):
#		super().save(*args, **kwargs)


	def __str__(self):
		return self.file.name
	