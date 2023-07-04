# from django.core.validators import RegexValidator
# from django.forms import MultiValueField, CharField
#
#
# class PhoneField(MultiValueField):
#     def __init__(self, **kwargs):
#         # Define one message for all fields.
#         error_messages = {
#             "incomplete": "Enter a country calling code and a phone number.",
#         }
#         # Or define a different message for each field.
#         fields = (
#             CharField(
#                 error_messages={"incomplete": "Enter a country calling code."},
#                 validators=[
#                     RegexValidator(r"^[0-9]+$", "Enter a valid country calling code."),
#                 ],
#             ),
#             CharField(
#                 error_messages={"incomplete": "Enter a phone number."},
#                 validators=[RegexValidator(r"^[0-9]+$", "Enter a valid phone number.")],
#             ),
#             CharField(
#                 validators=[RegexValidator(r"^[0-9]+$", "Enter a valid extension.")],
#                 required=False,
#             ),
#         )
#         super().__init__(
#             error_messages=error_messages,
#             fields=fields,
#             require_all_fields=False,
#             **kwargs
#         )
