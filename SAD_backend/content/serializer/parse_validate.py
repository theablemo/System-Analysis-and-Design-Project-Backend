from backend.exception_handler import ApiException
from django.utils.translation import ugettext_lazy as _
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def name_validate(name):
    name = name.strip() if name else ''
    if len(name) == 0:
        raise ValidationError(_('cant be empty'))
    regex1 = re.compile(r'(?u)^[ \D]+$')
    regex2 = re.compile('(?u)^[ |‌|\w]+$')  # include zero-width space
    if not regex1.match(name):
        raise ValidationError(_('cant contain numbers'))
    if not regex2.match(name):
        raise ValidationError(_('cant contain special characters'))
    return name


def is_password_strong(password):
    return len(password) > 5


def parse_validate_name(first_name, kind='first'):
    try:
        return name_validate(first_name)
    except ValidationError as e:
        raise ApiException(_("name ") + e.message,
                           code='InvalidName', description=f'{kind}_name validation failed')
