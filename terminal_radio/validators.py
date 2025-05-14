from prompt_toolkit.validation import ValidationError, Validator
import re


class YesNoValidator(Validator):

    def validate(self, document):
        text: str = document.text.lower()

        if text not in ('y', 'n'):
            raise ValidationError(message="Answer should be 'y' or 'n'")


class StationNameValidator(Validator):

    def validate(self, document):
        text: str = document.text

        if len(text) == 0:
            raise ValidationError(
                message="Station name should be at least one character"
            )


class StationUrlValidator(Validator):

    def validate(self, document):

        text: str = document.text

        if not self.is_valid_url(text):
            raise ValidationError(
                message="URL is not a valid URL"
            )

    def is_valid_url(self, text) -> bool:
        pattern = (
            "^https?:\\/\\/(?:www\\.)?"
            "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\"
            ".[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@"
            ":%_\\+.~#?&\\/=]*)$"
        )

        regex_result = re.search(pattern, text)
        return bool(regex_result)
