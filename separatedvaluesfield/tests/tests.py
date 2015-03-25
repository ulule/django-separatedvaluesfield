# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase

from .models import (Project,
                     RequiredProject,
                     ProjectCast)


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
                exclude = ()

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

    def test_errors(self):
        class ProjectForm(forms.ModelForm):
            class Meta:
                model = Project
                exclude = ()

        class RequiredProjectForm(forms.ModelForm):
            class Meta:
                model = RequiredProject
                exclude = ()

        form = ProjectForm(data={
            'name': 'Weekly',
            'languages': [u'fake']
        })

        self.assertFalse(form.is_valid())
        self.assertIn('languages', form.errors)

        required_form = RequiredProjectForm(data={
            'name': 'Weekly',
        })

        self.assertFalse(required_form.is_valid())
        self.assertIn('languages', required_form.errors)

    def test_cast_model(self):
        project = ProjectCast(name='project')
        self.assertEqual(project.languages, None)

        langs = [u'1', u'2']
        project.languages = langs
        project.save()

        self.assertEqual(project.languages, [1, 2])

        langs = [1, 2]
        project.languages = langs
        project.save()

        self.assertEqual(project.languages, [1, 2])

    def test_cast_validation(self):
        class ProjectCastForm(forms.ModelForm):
            class Meta:
                model = ProjectCast
                exclude = ()

        form = ProjectCastForm(data={
            'name': 'Weekly',
            'languages': [u'1', u'2'],
        })

        self.assertTrue(form.is_valid())

        form = ProjectCastForm(data={
            'name': 'Weekly',
            'languages': [1, 2],
        })

        self.assertTrue(form.is_valid())
