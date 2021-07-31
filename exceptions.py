# CUSTOM EXCEPTIONS AND WARNINGS
#
# NOTE: This file is *not* intended to be run on its own and won't do anything
#
# (c) by Benjamin Grau 2021


# TODO: Better messages / Create default messages

# == Config ==

class InvalidValueInConfigError(Exception):
    """Exception raised for an invalid value while checking the config 
    file"""

    def __init__(self, value, 
                 message: str = ''):
        self.value = value
        self.message = message

    def __str__(self) -> str:
        return f'Error'

class InvalidTypeInConfigError(Exception):
    """Exception raised for a wrong type in the config file"""

    def __init__(self, key: str, expectedType, gottenType, 
                 message: str = ''):
        self.key = key
        self.expectedType = expectedType
        self.gottenType = gottenType
        self.message = message

    def __str__(self) -> str:
        return f'Error'

# == Generate ==

# -- Warnings --
class UnusedPlaceholderInTemplateWarning(Warning):
    """Warning raised for an placeholder that has a value assigned 
    but is not used in the template"""
    
    def __init__(self, placeholder: str, 
                 message: str = ''):
        self.placeholder = placeholder
        self.message = message

    def __str__(self) -> str:
        return message

class NoPlaceholderForValueWarning(Warning):
    """Warning raised for an value (in the meta data) that isn't 
    utilized by any placeholder in the template"""
    
    def __init__(self, name: str, 
                 message: str = ''):
        self.name = name
        self.message = message

    def __str__(self):
        return message