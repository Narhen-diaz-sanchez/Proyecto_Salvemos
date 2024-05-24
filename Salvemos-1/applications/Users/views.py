""""Vistas de la aplicación Users"""
# Imports Django
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .functions import *

from django.views.generic import (
    View,
    ListView,
    DeleteView
)

from django.views.generic.edit import (
    FormView
)
# Imports propios
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm,
)
#
from .models import User, Favorites
from applications.Posts.models import Posts
#


class UserRegisterView(FormView):
    """Vista para registrar un usuario"""
    template_name = 'Users/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('Users_app:user-login')

    def form_valid(self, form):
        # Se crea el código de verificación
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            name=form.cleaned_data['name'],
            last_name=form.cleaned_data['last_name'],
            is_foundation=form.cleaned_data['is_foundation'],
            genero=form.cleaned_data['genero'],
            date_birth=form.cleaned_data['date_birth'],
            codregistro=codigo,
        )
        # Enviar email al usuario
        asunto = 'Email de confirmación'
        message = 'Tu código de registro para salvemos ' + codigo
        from_email = 'lermasama@gmail.com'
        send_mail(asunto, message, from_email, [form.cleaned_data['email'], ])
        # Una vez confirmado redirigir a pantalla de confirmación

        return HttpResponseRedirect(
            reverse(
                'Users_app:user-verification',
                kwargs={'pk': usuario.id}
            )
        )


class LoginUser(FormView):
    """"Vista para iniciar sesión"""
    template_name = 'Users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('Posts_app:Posts-lista')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    """Vista para cerrar sesión"""

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'Users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    """Vista para actualizar la contraseña"""
    template_name = 'users/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('Users_app:user-login')
    login_url = reverse_lazy('Users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class UserPageListView(LoginRequiredMixin, ListView):
    """Vista mostrar la cuenta de un usuario"""
    template_name = "Users/profile.html"
    context_object_name = 'profileuser'
    login_url = reverse_lazy('Users_app:user-login')

    def get_queryset(self):
        return Favorites.objects.posts_user(self.request.user)


class addfavoritosView(View):
    """Vista para añadir un favorito"""

    def post(self, request, *args, **kwargs):
        # se recupera el usuario
        usuario = self.request.user
        # se recupera la entrada o pk
        post = Posts.objects.get(id=self.kwargs['pk'])
        # se registra el objeto favorito
        Favorites.objects.create(
            user=usuario,
            post=post,
        )

        return HttpResponseRedirect(reverse('Users_app:user-profile'))


class FavoritosDeleteView(DeleteView):
    """Vista para eliminar un favorito"""
    model = Favorites
    success_url = reverse_lazy('Users_app:user-profile')


class CodVerificationView(FormView):
    """Vista para ingresar el código de verificación"""
    template_name = 'Users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('Users_app:user-login')

    # Se sobreescribe get_form_kwargs para que envíe nuevos kwargs al
    # formulario y poder recuperar el id de la url
    def get_form_kwargs(self):
        kwargs = super(CodVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodVerificationView, self).form_valid(form)
