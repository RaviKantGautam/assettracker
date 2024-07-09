from django.db import models

class AbstractBaseModel(models.Model):
    '''
    This is an abstract base model that provides common fields for all models in the project.
    '''

    # Common fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
        This class provides metadata for the model.
        '''
        abstract = True
        ordering = ['-created_at']