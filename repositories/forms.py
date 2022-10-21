from django import forms

from .models import Locker, Folder, Document


class LockerForm(forms.ModelForm):
    class Meta:
        model = Locker
        fields = ('name', 'description')


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ('name', 'locker')


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('name', 'document_type', 'folder', 'source')
