# -*- coding: utf-8 -*-
from django.db import models

from separatedvaluesfield.models import SeparatedValuesField, TextSeparatedValuesField


class Project(models.Model):
    name = models.CharField(max_length=150)
    languages = SeparatedValuesField(max_length=150, choices=(('en', 'English'),
                                                              ('fr', 'French')), blank=True)


class RequiredProject(models.Model):
    name = models.CharField(max_length=150)
    languages = SeparatedValuesField(max_length=150, choices=(('en', 'English'),
                                                              ('fr', 'French')))


class ProjectCastInt(models.Model):
    name = models.CharField(max_length=150)
    languages = SeparatedValuesField(
        max_length=150,
        cast=int,
        choices=(
            (1, 'English'),
            (2, 'French')))


class ProjectCastString(models.Model):
    name = models.CharField(max_length=150)
    languages = SeparatedValuesField(
        max_length=150,
        choices=(
            ('1', 'English'),
            ('2', 'French')))


class ProjectText(models.Model):
    name = models.CharField(max_length=150)
    languages = TextSeparatedValuesField(choices=(('en', 'English'),
                                                  ('fr', 'French')), blank=True)
