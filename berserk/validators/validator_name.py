from typing import Any
import re

from django.core.exceptions import ValidationError  
from django.utils.translation import gettext as _


class Validator_name:
    def __init__(self, max_len=33, min_len=3) -> None:
        self.max_len = max_len
        self.min_len = min_len
    
    def validator_name(self, username, *args: Any, **kwargs: Any) -> Any: 
        list_char_name = [str(i) for i in str(username)]
        if len(list_char_name) < self.min_len or len(list_char_name) > self.max_len:
            raise ValidationError('the username must contain from 3 to 33 characters')
        str_username = str(username)
        regex = r'^[a-zA-Z0-9-_]+$',
        if re.match(regex, str_username):
            pass
        else:
            raise ValidationError('the usernsme must contain from 3 to 33 characters')
        
    def get_help_text(self):
        return _('the usernsme must contain from 3 to 33 characters')