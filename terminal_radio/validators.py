import re
from prompt_toolkit.validation import ValidationError, Validator


class YesNoValidator(Validator):
    """Validator for Yes/No Input

    Args:
        Validator (Validator): prompt_toolkit Validator
    """

    def validate(self, document):
        """Validate a yes/no input from a user

        Args:
            document (_type_): document (Document): A prompt_toolkit Document

        Raises:
            ValidationError: Error raised if the user enters anything
            other than 'y' or 'n'
        """
        text: str = document.text.lower()

        if text not in ('y', 'n'):
            raise ValidationError(message="Answer should be 'y' or 'n'")


class StationNameValidator(Validator):
    """Validator for Station Name

    Args:
        Validator (Validator): prompt_toolkit Validator
    """

    def validate(self, document):
        """Validate a station's name submitted by a user

        Args:
            document (Document): A prompt_toolkit Document

        Raises:
            ValidationError: Error raised if the name is invalid
        """
        text: str = document.text

        if len(text) == 0:
            raise ValidationError(
                message="Station name should be at least one character"
            )


class StationUrlValidator(Validator):
    """Validator for URLs

    Args:
        Validator (Validator): prompt_toolkit Validator
    """

    def validate(self, document):
        """Validate a station's source/image url

        Args:
            document (Document): A prompt_toolkit Document

        Raises:
            ValidationError: Error raised if the user does not
            enter a valid url that matches the regex
        """

        text: str = document.text

        if not self.is_valid_url(text) and text != "":
            raise ValidationError(
                message="URL is not a valid URL"
            )

    def is_valid_url(self, text: str) -> bool:
        """Check URL validity using regex

        Args:
            text (str): The URL input by the user

        Returns:
            bool: Is the URL valid
        """
        pattern = (
            "^https?:\\/\\/(?:www\\.)?"
            "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\"
            ".[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@"
            ":%_\\+.~#?&\\/=]*)$"
        )

        regex_result = re.search(pattern, text)
        return bool(regex_result)
