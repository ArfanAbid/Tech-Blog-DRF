from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

# Base models in Django are used to define common fields and behaviors that you want to share across multiple models.
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True   # means they won't create database tables on their own. Instead, they serve as templates for other models to inherit from.


class BlogModel(BaseModel):
    user_id =models.ForeignKey(User, on_delete=models.CASCADE,related_name="blog")
    ownerName=models.CharField(max_length=100)
    title=models.CharField(max_length=500)
    content=models.TextField()
    image=models.ImageField(upload_to="blog_images")

    def __str__(self):
        return self.title
