from django import forms
from django.test import TestCase

from .models import Project


class SeparatedValuesFieldTests(TestCase):
    def test_basics(self):
        project = Project(name='monthly')
        self.assertEqual(project.languages, None)

        langs = ['en', 'fr']

        project.languages = langs
        project.save()

        self.assertEqual(project.languages, langs)

        class ProjectForm(forms.ModelForm):
            class Meta:
                model = Project

        form = ProjectForm()
        self.assertFalse(form.fields['languages'].required)

        valid_data = {'name': 'Weekly', 'languages': [u'']}
        form = ProjectForm(data=valid_data)
        self.assertTrue(form.is_valid())

        valid_data = {'name': 'Daily', 'languages': [u'en', u'fr']}
        form = ProjectForm(data=valid_data)
        self.assertTrue(form.is_valid())

        instance = form.save()

        self.assertEqual(instance.languages, langs)
