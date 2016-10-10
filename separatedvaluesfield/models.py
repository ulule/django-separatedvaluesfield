# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import validators
from django.core import exceptions
from django.db import models
from django.forms.fields import MultipleChoiceField
from django.utils import six
from django.utils.text import capfirst


class Creator(object):
    """
    A placeholder class that provides a way to set the attribute on the model.
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class SeparatedValuesField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        self.cast = kwargs.pop('cast', six.text_type)
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super(SeparatedValuesField, self).contribute_to_class(cls, name, **kwargs)

        setattr(cls, self.name, Creator(self))

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self.choices and value:
            choices = []

            for option_key, option_value in self.choices:
                if isinstance(option_value, (list, tuple)):
                    # This is an optgroup, so look inside the group for
                    # options.
                    for optgroup_key, optgroup_value in option_value:
                        choices.append(optgroup_key)
                else:
                    choices.append(option_key)

            # If we have integers, convert them first to be sure we only compare
            # right types
            choices = [self.cast(choice) for choice in choices]

            for val in value:
                if val and val not in choices:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % val)

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])

    def to_python(self, value):
        if not value:
            return None

        values = value
        if isinstance(value, six.string_types):
            values = value.split(self.token)

        return [self.cast(v) for v in values]

    def get_db_prep_value(self, value, *args, **kwargs):
        if not value:
            return ''

        assert(isinstance(value, list) or isinstance(value, tuple))

        return self.token.join(['%s' % s for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def formfield(self, form_class=MultipleChoiceField, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()

        if self.choices:
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)

            for k in list(kwargs):
                if k not in ('choices', 'required',
                             'widget', 'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial'):
                    del kwargs[k]
        defaults.update(kwargs)
        return form_class(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^separatedvaluesfield\.models\.SeparatedValuesField"])
except ImportError:
    pass
