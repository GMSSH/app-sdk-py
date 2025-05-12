# -*- encoding: utf-8 -*-

from wtforms import Form, validators
from wtforms.fields import simple

import simplejrpc.config as setting
from simplejrpc.i18n import GI18n
from simplejrpc.i18n import T as i18n
from simplejrpc.interfaces import BaseValidator


class StringLangValidator(BaseValidator):
    """ """

    def __init__(self, lang="en"):
        self.lang = lang

    def validator(self, form, field):
        lang = field.data or self.lang
        GI18n(setting.PROJECT_I18n_PATH, lang)
        return lang


class StrRangeValidator(BaseValidator):
    """ """

    allows = []
    err_message = ""

    def __init__(self, allows, message=None):
        """ """
        self.allows = allows
        self.err_message = message or self.err_message

    def validator(self, form, field):
        if field.data not in self.allows:
            message = i18n.translate(self.err_message) if self.err_message else f"expected value {self.allows}"
            raise validators.ValidationError(message)


class IntLimitValidator:
    """ """

    min: int
    max: int
    err_message = ""

    def __init__(self, min=1, max=1000):
        self.max = max
        self.min = min

    def validator(self, form, field):
        """ """
        if field.data < self.min or field > self.max:
            """ """
            message = (
                i18n.translate_ctx(self.err_message, self.min, self.max)
                if self.err_message
                else f"expected value {[self.min,self.max]}"
            )
            raise validators.ValidationError(message)


class BaseForm(Form):
    lang = simple.StringField(validators=[StringLangValidator()])
