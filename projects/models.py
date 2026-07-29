from django.db import models

# Create your models here.

class ArchitectDesigner(models.Model):
	architect_designer_id = models.AutoField(primary_key=True)
	architect = models.CharField(max_length=100)
	designer = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.architect} / {self.designer}'


class Project(models.Model):
	project_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	desc = models.TextField()
	
	owner = models.CharField(max_length=140)
	architect_engineer = models.CharField(max_length=140)
	project_value = models.IntegerField()
	start_date = models.DateField()
	completion_date = models.DateField()

	additional_content = models.TextField()

	def __str__(self):
		return self.title


class Photo(models.Model):
	photo_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name