# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.test import TestCase

from .models import (Project,
                     RequiredProject,
                     ProjectCastInt,
                     ProjectCastString)


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

        valid_data = {'name': 'Weekly', 'languages': ['']}
        form = ProjectForm(data=valid_data)
        self.assertTrue(form.is_valid())

        valid_data = {'name': 'Daily', 'languages': ['en', 'fr']}
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
            'languages': ['fake']
        })

        self.assertFalse(form.is_valid())
        self.assertIn('languages', form.errors)

        required_form = RequiredProjectForm(data={
            'name': 'Weekly',
        })

        self.assertFalse(required_form.is_valid())
        self.assertIn('languages', required_form.errors)

    def test_cast_model(self):

        #
        # A single tring
        #

        project = ProjectCastInt(name='project')
        self.assertEqual(project.languages, None)

        langs = "1,2"
        project.languages = langs
        project.save()
        self.assertEqual(project.languages, [1, 2])

        # Now let's fetch it again
        project = ProjectCastInt.objects.all()[0]
        self.assertEqual(project.languages, [1, 2])

        project.delete()

        project = ProjectCastString(name='project')
        self.assertEqual(project.languages, None)

        langs = "1,2"
        project.languages = langs
        project.save()
        self.assertEqual(project.languages, ['1', '2'])

        # Now let's fetch it again
        project = ProjectCastString.objects.all()[0]
        self.assertEqual(project.languages, ['1', '2'])

        project.delete()

        #
        # List of Integers
        #

        project = ProjectCastInt(name='project')
        self.assertEqual(project.languages, None)

        project.languages = ['1', '2']
        project.save()
        self.assertEqual(project.languages, [1, 2])

        # Now let's fetch it again
        project = ProjectCastInt.objects.all()[0]
        self.assertEqual(project.languages, [1, 2])

        project.delete()

        project = ProjectCastInt(name='project')
        self.assertEqual(project.languages, None)
        project.languages = [1, 2]
        project.save()
        self.assertEqual(project.languages, [1, 2])

        # Now let's fetch it again
        project = ProjectCastInt.objects.all()[0]
        self.assertEqual(project.languages, [1, 2])

        project.delete()

        # List of strings

        project = ProjectCastString(name='project')
        self.assertEqual(project.languages, None)

        project.languages = ['1', '2']
        project.save()
        self.assertEqual(project.languages, ['1', '2'])

        # Now let's fetch it again
        project = ProjectCastString.objects.all()[0]
        self.assertEqual(project.languages, ['1', '2'])

        project.delete()

        project = ProjectCastString(name='project')
        self.assertEqual(project.languages, None)
        project.languages = [1, 2]
        project.save()
        self.assertEqual(project.languages, ['1', '2'])

        # Now let's fetch it again
        project = ProjectCastString.objects.all()[0]
        self.assertEqual(project.languages, ['1', '2'])

        project.delete()

    def test_cast_validation(self):

        # Integers

        class ProjectCastIntForm(forms.ModelForm):
            class Meta:
                model = ProjectCastInt
                exclude = ()

        form = ProjectCastIntForm(data={
            'name': 'Weekly',
            'languages': ['1', '2'],
        })

        self.assertTrue(form.is_valid())

        form = ProjectCastIntForm(data={
            'name': 'Weekly',
            'languages': [1, 2],
        })

        self.assertTrue(form.is_valid())

        # Strings

        class ProjectCastStringForm(forms.ModelForm):
            class Meta:
                model = ProjectCastString
                exclude = ()

        form = ProjectCastStringForm(data={
            'name': 'Weekly',
            'languages': ['1', '2'],
        })

        self.assertTrue(form.is_valid())

        form = ProjectCastStringForm(data={
            'name': 'Weekly',
            'languages': ['1', '2'],
        })

        self.assertTrue(form.is_valid())
