# Задачи

1. **Создать модель AbstractUser**  
    AbstractUser - это базовый класс для создания пользовательских моделей в Django. Он предоставляет все основные поля и методы для работы с пользователями, такие как аутентификация, управление паролями и разрешениями. Используя AbstractUser, вы можете расширять и настраивать пользовательскую модель в соответствии с требованиями вашего проекта.

2. **Реализовать логику Регистрации, Авторизации и Выхода из Аккаунта**
     - **Регистрация**: Создайте форму регистрации, которая будет собирать данные пользователя, такие как имя, адрес электронной почты и пароль. После успешной регистрации пользователь должен быть перенаправлен на страницу входа.
     - **Авторизация**: Реализуйте форму входа, которая будет проверять учетные данные пользователя и, в случае успеха, перенаправлять его на страницу входа.
     - **Выход из аккаунта**: Добавьте возможность выхода из аккаунта, чтобы пользователь мог завершить свою сессию и вернуться на страницу входа.

3. **Отправка уведомления на почту об успешной регистрации**
     - Настройте почтовый сервер в настройках Django, добавив необходимые параметры, такие как `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER` и `EMAIL_HOST_PASSWORD`.
     - Создайте функцию для отправки электронных писем, используя метод `send_mail` из `django.core.mail`.
     - Вызовите эту функцию после успешной регистрации пользователя, передав ей адрес электронной почты пользователя и сообщение о успешной регистрации.

# Решение

### Задача 1

Создание пользовательской модели на основе `AbstractUser`:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
```

Этот код создает пользовательскую модель `CustomUser`, которая наследует от `AbstractUser`. Мы добавили дополнительные поля, такие как `location`, `birth_date`, `bio` и `avatar`. Поле `email` используется в качестве уникального идентификатора пользователя.

### Задача 2

Реализация логики регистрации, авторизации и выхода из аккаунта:

```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .utils import send_email   

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            # Отправка email
            email = form.cleaned_data.get('email')
            subject = 'Welcome to our site'
            message = 'Thank you for registering on our site'
            send_email(subject, email, message)

            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Error creating your account')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('/')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Invalid email or password')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('/')
```

Этот код включает три представления: `register`, `login_user` и `logout_user`. Представление `register` обрабатывает регистрацию пользователя, отправляет приветственное письмо и автоматически аутентифицирует пользователя. Представление `login_user` обрабатывает вход пользователя, а `logout_user` - выход.

### Задача 3

Отправка уведомления на почту об успешной регистрации:

```python
# accounts/utils.py
from django.core.mail import send_mail
from django.http import HttpResponse

def send_email(subject, email, message):
    recipient_list = [email]
    from_email = 'hero.beka.kg@gmail.com'

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Письмо отправлено')
    except Exception as e:
        return HttpResponse(str(e))
```

Этот код определяет функцию `send_email`, которая отправляет электронное письмо с заданной темой и сообщением на указанный адрес электронной почты. Функция вызывается после успешной регистрации пользователя в представлении `register`.

```python
# accounts/views.py
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            ...
            email = form.cleaned_data.get('email')
            subject = 'Welcome to our site'
            message = 'Thank you for registering on our site'
            send_email(subject, email, message)
            ....
```

Этот фрагмент кода показывает, как функция `send_email` вызывается в представлении `register` после успешного создания учетной записи пользователя.
