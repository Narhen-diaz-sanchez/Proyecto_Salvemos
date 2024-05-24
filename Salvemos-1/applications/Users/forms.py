from django import forms
from django.contrib.auth import authenticate
#
from .models import User


class UserRegisterForm(forms.ModelForm):
    """Formulario para registrar un usuario"""
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ingresa una contraseña',
                'class': 'input__login',
            }
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Escribe nuevamente la contraseña',
                'class': 'input__login',
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'email',
            'name',
            'last_name',
            'is_foundation',
            'genero',
            'date_birth',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico',
                    'class': 'input__login',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingresa tu nombre',
                    'class': 'input__login',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingresa tus apellidos',
                    'class': 'input__login',
                }
            ),
            'genero': forms.Select(
                attrs={
                    'placeholder': 'Genero',
                    'class': 'input__login',
                }
            ),
            'date_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'is_foundation': forms.CheckboxInput(
            ),
        }
    # Valida si las contraseñas son iguales

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    """Formulario para iniciar sesión"""
    email = forms.CharField(
        # label='E-mail',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa tu correo electrónico',
                'class': 'input__login',
            }
        )
    )
    password = forms.CharField(
        # label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ingresa tu contraseña',
                'class': 'input__login',
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError(
                'Los datos de usuario no son correctos')

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):
    """Formulario para actualizar la contraseña"""
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual',
                'class': 'input__login',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva',
                'class': 'input__login',
            }
        )
    )


class VerificationForm(forms.Form):
    """Formulario para la validar el código de verificación"""
    codregistro = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingresa tu código de verificación',
                'class': 'input__login',
            }
        )
    )

    # se sobreescribre __init__ para recuperar los
    # kwargs adicionales enviados desde las views
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        """Esta función valida que el códig de registro le pertenezca al usuario
        llamando al manager cod_validation que devuelve True si es valido"""
        # se recupera el código para realizar la validación
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificamos si el codigo y el id de usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El código es incorrecto')
        else:
            raise forms.ValidationError('El código es incorrecto')
