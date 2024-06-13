from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .validators import validate_icon_image_size, validate_image_file_exstension

# Function to determine the upload path for server icon images
def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icons/{filename}"

# Function to determine the upload path for server banner images
def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"

# Function to determine the upload path for category icon images
def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"

# Category model to represent categories
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category
    icon = models.FileField(
        upload_to=category_icon_upload_path,  # Path for uploading category icons
        null=True,
        blank=True,
    )

    # Override the save method to handle existing icon deletion
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)  # Get existing category
            if existing.icon != self.icon:  # If the icon has changed, delete the old one
                existing.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)  # Call the parent save method

    # Signal receiver to delete icon file when category is deleted
    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name  # String representation of the category

# Server model to represent servers
class Server(models.Model):
    name = models.CharField(max_length=100)  # Name of the server
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")  
    # Relationship: A server has one owner, represented by a foreign key to the user model.
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="server_category")  
    # Relationship: A server belongs to one category, represented by a foreign key to the Category model.
    
    description = models.CharField(max_length=250, blank=True, null=True)  # Optional description of the server
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)  
    # Relationship: A server can have multiple members, represented by a many-to-many relationship to the user model.

    def __str__(self):
        return f"{self.name}-{self.id}"  # String representation of the server

# Channel model to represent channels within servers
class Channel(models.Model):
    name = models.CharField(max_length=100)  # Name of the channel
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")  
    # Relationship: A channel has one owner, represented by a foreign key to the user model.
    
    topic = models.CharField(max_length=100)  # Topic of the channel
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")  
    # Relationship: A channel belongs to one server, represented by a foreign key to the Server model.
    
    banner = models.ImageField(
        upload_to=server_banner_upload_path,  # Path for uploading channel banners
        null=True,
        blank=True,
        validators=[validate_image_file_exstension],  # Validate image file extension
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,  # Path for uploading channel icons
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_exstension],  # Validate image size and file extension
    )

    # Override the save method to handle existing icon and banner deletion
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)  # Get existing channel
            if existing.icon != self.icon:  # If the icon has changed, delete the old one
                existing.icon.delete(save=False)
            if existing.banner != self.banner:  # If the banner has changed, delete the old one
                existing.banner.delete(save=False)
        super(Channel, self).save(*args, **kwargs)  # Call the parent save method

    # Signal receiver to delete icon and banner files when channel is deleted
    @receiver(models.signals.pre_delete, sender="server.Server")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name  # String representation of the channel
