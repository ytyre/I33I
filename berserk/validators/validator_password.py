from typing import Any
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class Validator_passwod:
    def __init__(self, min_len=6, max_len=25, 
                 symbols=['/', '*', '#','$','&','_'],) -> None:
        self.min_len = min_len
        self.max_len = max_len
        self.symbols = symbols

    def validate(self, password1, password2, *args: Any, **kwargs: Any) -> Any:
        list_char_password = [str(i) for i in str(password1)]
        if len(list_char_password) < self.min_len or len(list_char_password) > self.max_len:
            raise ValidationError('the password must contain from 6 to 25 characters')
        pass1 = str(password1)
        pass2 = str(password2)
        regex = r'^[a-zA-Z0-9-_&*$]+$'
        if re.match(regex, pass1):
            if re.match(regex, pass2):
                pass
        else:
            raise ValidationError('the usernsme must contain from 3 to 33 characters')

    def get_help_text(self):
        pass
    

