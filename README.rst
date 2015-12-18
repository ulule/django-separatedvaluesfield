django-separatedvaluesfield
===========================

.. image:: https://secure.travis-ci.org/thoas/django-separatedvaluesfield.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-separatedvaluesfield

Alternative to CommaSeparatedIntegerField_ built-in field that supports
MultipleChoiceField_, custom separator and returns values as list.

Installation
------------

Install package from PyPi_::

    pip install django-separatedvaluesfield

Or download the archive from GitHub_ and proceed to a manual installation::

    curl -L https://github.com/thoas/django-separatedvaluesfield/tarball/master | tar zx
    cd thoas-django-separatedvaluesfield
    python setup.py install

Add ``SeparatedValuesField`` to your Django model:

.. code:: python

    # models.py
    from django.db import models

    from separatedvaluesfield.models import SeparatedValuesField

    class Project(models.Model):
        name = models.CharField(max_length=150)
        languages = SeparatedValuesField(
            max_length=150,
            token=',',
            choices=(
                ('en', 'English'),
                ('fr', 'French')))

If your choices values are not strings, add the ``cast`` option with the type
you want to apply on values (defaults to ``django.utils.six.text_type``):

.. code:: python

    # models.py
    from django.db import models

    from separatedvaluesfield.models import SeparatedValuesField

    class Project(models.Model):
        name = models.CharField(max_length=150)
        languages = SeparatedValuesField(
            max_length=150,
            cast=int,
            token=',',
            choices=(
                (1, 'English'),
                (2, 'French')))

If you are running Django <= 1.6, synchronize your database using ``syncdb``::

    python manage.py syncdb

If you are running Django >= 1.7, synchronize your database using ``migrate``::

    python manage.py migrate

The ``SeparatedValuesField`` behaves like a ``CharField`` which separates values with
a token (default is ``,``).

This field is transformed as a MultipleChoiceField_ when you are
creating a ``forms.ModelForm`` with your model.

Usage
-----

.. code:: pycon

    >>> from myapp.models import Project
    >>> project = Project(name='Project with strings', languages=['fr', 'en'])
    >>> project.save() # save 'fr,en' in database for the column "languages"
    >>> project.pk
    1

    >>> project = Project.objects.get(pk=1)
    >>> project.languages
    ['fr', 'en']

    # If you added "cast" option to the field to cast to 'int'
    >>> project = Project(name='Project with integers', languages=[u'1', u'2'])
    >>> project.save() # save '1,2' in database for the column "languages"
    >>> project = Project.objects.get(pk=1)
    >>> project.languages
    [1, 2]

Contribute
----------

1. Fork the repository
2. Clone your fork
3. Create a dedicated branch (never ever work in ``master``)
4. Create your development environment with ``make dev``
5. Activate your environment with ``source .venv/bin/activate``
6. Make modifications
7. Write tests and execute them with ``make test``
8. Be sure all test pass with ``tox``
9. If all tests pass, submit a pull request

.. _CommaSeparatedIntegerField: https://docs.djangoproject.com/en/dev/ref/models/fields/#commaseparatedintegerfield
.. _PyPi: https://pypi.python.org/
.. _GitHub: https://github.com/thoas/django-separatedvaluesfield
.. _MultipleChoiceField: https://docs.djangoproject.com/en/dev/ref/forms/fields/#multiplechoicefield
