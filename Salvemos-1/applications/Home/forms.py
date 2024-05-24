from django import forms
#
from .models import Contact


class ContactForm(forms.ModelForm):
    """Formulario para la vista de contacto"""
    class Meta:
        model = Contact
        fields = (
            'full_name',
            'email',
            'message',
        )
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingresa tu nombre:',
                    'class': 'input__contact',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Ingresa tu correo:',
                    'class': 'input__contact',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'placeholder': 'Ingresa tu mensaje:',
                    'class': 'input__contact contact__input--area',
                }
            ),
        }
