django-separatedvaluesfield
===========================

.. image:: https://secure.travis-ci.org/thoas/django-separatedvaluesfield.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-separatedvaluesfield

Custom field for Django to separate multiple values in database
with a separator and retrieve them as list.

Compatibility
-------------

This library is compatible with:

- python2.6, django1.4
- python2.6, django1.5
- python2.6, django1.6
- python2.7, django1.4
- python2.7, django1.5
- python2.7, django1.6
- python3.3, django1.5
- python3.3, django1.6

Installation
------------

1. Download the package on GitHub_ or simply install it via PyPi
2. Add ``SeparatedValuesField`` to your Django model ::

    # models.py
    from django.db import models

    from separatedvaluesfield.models import SeparatedValuesField


    class Project(models.Model):
        name = models.CharField(max_length=150)
        languages = SeparatedValuesField(max_length=150, choices=(('en', 'English'),
                                                                  ('fr', 'French')), token=',')


3. Sync your database using ``syncdb`` command from django command line


The ``SeparatedValuesField`` behaves like a ``CharField`` which separates values with
a token (default is ``,``).

This field is transformed as a MultipleChoiceField_ when you are
creating a ``forms.ModelForm`` with your model.


Usage
-----

::

    In [1]: from myapp.models import Project

    In [2]: project = Project(name='Foo', languages=['fr', 'en'])

    In [3]: project.save() # save 'fr,en' in database for the column "languages"

    In [4]: project.pk
    1

    In [5]: project = Project.objects.get(pk=1)

    In [6]: project.languages
    ['fr', 'en']


.. _GitHub: https://github.com/thoas/django-separatedvaluesfield
.. _MultipleChoiceField: https://docs.djangoproject.com/en/dev/ref/forms/fields/#multiplechoicefield
