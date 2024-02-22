from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.decorators.vary import vary_on_headers
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.cache import cache_page
from django.contrib.auth import login
from django.contrib import messages
from .forms import FormRegistration  # Поменяйте это на путь к вашей форме регистрации
from .models import AdvUser  # Поменяйте это на путь к вашей модели пользователя
from django.shortcuts import render, redirect

from .models import br, AdvUser, Comment, RecordLike,ExtraInformation, ImagesAdmin #модели под  записи, регистрацию, комментарии, оценивание 
from django.db.models import Sum 
from .forms import formI, FormRegistration, CommentForm, ExtraInformationForm, SerarchRecordForm, ImagesAdminForm #формы для регистрации и создания записей


# осуществляет поиск записей по 'title'
#обработка основной страница с записями
#@login_required(redirect_field_name='I33I/login/')

@vary_on_headers('Cookie') 
def ber(request):
    items = br.objects.order_by('-published')
    paginator = Paginator(items, 19)
    count_dict = {}
    form = SerarchRecordForm(request.POST)
    admin_image = ImagesAdmin.objects.all()
    
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    for item in page:
        count = Comment.objects.filter(post=item).count()
        count_dict[item.id] = count
        author_info = ExtraInformation.objects.get(author=item.author)
        item.author_info = author_info  # Добавляем информацию о пользователе к записи
    
    if request.method == 'POST':    
        if form.is_valid(): 
            value = form.cleaned_data['value']  
            items = br.objects.filter(title__icontains=value)
            context = {'items': page.object_list, 'page': page, 'count_dict': count_dict, 'form': form, 'admin_image':admin_image}
            return render(request, 'samplesearch.html', context)
        
    context = {'items': page.object_list, 'page': page, 'count_dict': count_dict, 'form': form, 'admin_image':admin_image}
    return render(request, 'sample.html', context)


#определение админом изображения поумолчанию 
def DefaultImage(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            form = ImagesAdminForm(request.POST, request.FILES,)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = ImagesAdminForm() #вывод пустой формы для заполнения
            return render(request, 'admin_image.html', {'form': form})
    

#вывод конкретной записи
def specific_entry(request, post_id):  
    post = br.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).select_related('user').prefetch_related(
        Prefetch('user__extrainformation_set', queryset=ExtraInformation.objects.only('image', 'age', 'gender'))
    )
    admin_image = ImagesAdmin.objects.all()
    acc = ExtraInformation.objects.get(author=post.author)
    #вывод общего рейтинга записи на основе разности like и dislike
    rating = RecordLike.objects.filter(post=post).aggregate(Sum('like'))['like__sum'] or 0
    return render(request, 'specific_entry.html', {'post': post, 'comments': 
                                                   comments,'rating': rating, 'admin_image': admin_image, 'acc':acc})

    

#обработка страницы со сведениями о проекте

def i33iX(request):
    return render(request, 'proj.html')


#обработка страницы создания записи(с учётом аунтификации пользователя) 
@login_required(redirect_field_name='I33I/login/')
def Create_view(request):    
    if request.method == 'POST':
        form = formI(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/') #перенаправления на основную страницу после создания записи
        
    else:
        form = formI #вывод пустой формы для заполнения
    return render(request, 'create_view.html', {'form': form})


def registreted(request):
    form = FormRegistration()
    if request.method == 'POST':
        formR = FormRegistration(request.POST)
        if formR.is_valid():
            username = formR.cleaned_data['username']
            email = formR.cleaned_data['email']
            password1 = formR.cleaned_data['password1']
            password2 = formR.cleaned_data['password2']
            
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('/I33I/sing_in')
            
            if AdvUser.objects.filter(username=username).exists():
                messages.error(request, 'A user with this name already exists.')
                return redirect('/I33I/sing_in')
            
            try:
                user = AdvUser.objects.create_user(username=username, email=email, password=password1)
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('/')
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
                return redirect('/I33I/sing_in')
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
            return redirect('/I33I/sing_in')
    return render(request, 'registration/sing_in.html', {'form': form})


#вывод данных пользователя
@login_required(redirect_field_name='I33I/login/')
def account(request,):
    user = request.user.id
    reg = AdvUser.objects.all()
    admin_image = ImagesAdmin.objects.all()
    try: #если данные есть, то они выводятся   
        acc = ExtraInformation.objects.filter(author=user)
    except ExtraInformation.DoesNotExist:
        acc = None

    return render(request, 'account.html', {'reg': reg, 'acc': acc,'admin_image':admin_image})


#представление выхода из аккаунта, с использованием примесей 
class brLogOut(LoginRequiredMixin, LogoutView):
    template_name = 'registration/log_out.html'
    next_page = '/'


# система комментирования записей
@login_required(redirect_field_name='I33I/login/') 
def CreateComment(request, post_id):  
    post = br.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('specific_entry', post_id=post_id)
        else:
            print(form.errors)
    else:
        form = CommentForm()
        return render(request, 'com_create.html', {'form': form})
    return redirect('specific_entry', post_id=post.id)
    

#реализация общей системы оценивания записей (like)
@login_required(redirect_field_name='I33I/login/')
def CreateLike(request, post_id):
    post = br.objects.get(id=post_id)
    user = request.user
    #если запись уже существует удаляем, не существует - добавляем(like)
    likes, created = RecordLike.objects.get_or_create(user=user, post=post)
    
    if not created:
        likes.delete()
    else:
        likes.like += 1
        likes.save()
    return redirect('specific_entry', post_id=post.id)


#реализация общей системы оценивания записей (dislike)
@login_required(redirect_field_name='I33I/login/')
def CreateDislike(request, post_id):
    post = br.objects.get(id=post_id)
    user = request.user
    #если запись уже существует удаляем, не существует - добавляем(dislike)
    likes, created = RecordLike.objects.get_or_create(user=user, post=post)
    
    if not created:
        likes.delete()
    else:
        likes.like -= 1
        likes.save()
    return redirect('specific_entry', post_id=post.id)


#дополнение дополнительных сведений о пользователе 
@login_required(redirect_field_name='I33I/login/')
def CreateExtraInformation(request):
    user_id = request.user.id if request.user.is_authenticated else None
    existing_info = ExtraInformation.objects.filter(author=user_id).first()
    
    if request.method == 'POST':
        form = ExtraInformationForm(request.POST, request.FILES, instance=existing_info)
        if form.is_valid():
            if existing_info and existing_info.image:
                old_image_path = existing_info.image.path
                default_storage.delete(old_image_path)
            
            extra_info = form.save(commit=False)
            extra_info.author = request.user
            extra_info.save()

            return redirect('account')
    else:
        initial_data = {}
        if existing_info:
            initial_data = {
                'e_inf': existing_info.e_inf,
                'age': existing_info.age,
                'gender': existing_info.gender,
            }
        form = ExtraInformationForm(initial=initial_data)  # Используйте initial_data для начальных значений полей формы

    return render(request, 'extrainformation.html', {'form': form})
    
#контроллер-функция дл вывода записей созданных пользователем
@login_required(redirect_field_name='I33I/login/') 
def MyNotes(request):
    user = request.user.id
    item = br.objects.filter(author=user)
    return render(request, 'MyNotes.html', {'item':item})

#класс осуществляющий удаление записей 
class BrDeleteRecord(DeleteView):
    template_name = 'br_confirm_delete.html'
    model = br
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    def get_success_url(self):  
        new_url = reverse_lazy('MyNotes')
        return new_url


#смена пароля пользователя
class PasswordChangeView(PasswordChangeView):
    template_name = 'PasswordChange/password_change.html'

    def get_success_url(self) -> str:
        context = reverse_lazy('PasswordChangeDoneView')
        return context


#уведомление о смене пароля пользователем 
class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'PasswordChange/PasswordChangeDoneView.html'


#реализует сброс пароля пользователя 
class PasswordReset(PasswordResetConfirmView):
    template_name = 'PasswordReset/new_password.html'
    post_reset_login = False
    def get_success_url(self):
        context = reverse_lazy('login')
        return context
    def form_valid(self, form):
        # Валидный пароль, сохраняем его
        form.save()
        return super().form_valid(form) 


#контроллер-класс, инициирующий отправку письмо с инструкцией сброса пароля
class PasswordResetRecord(PasswordResetView):
    #путь к шаблону с формой для ввода адреса в виде строки 
    template_name = 'PasswordReset/email_for_reset.html'
    #путь к шаблону темыэлетронного письма 
    subject_template_name = 'PasswordReset/password_reset_subject.txt'
    #путь к шаблону тела электронного письма
    email_template_name = 'PasswordReset/password_reset_email.html'
    def get_success_url(self) -> str:
        context = reverse_lazy('account')
        return context
    

#контроллер-класс реализующий вход пользователя в систему 
class MyLoginView(LoginView):
    def get_success_url(self):
        context = reverse_lazy('account')
        return context 


#осуществляет выборку записей по названию 'Search'
def SearchForRecords(request):
    items = br.objects.order_by('-published')
    count_dict = {}  # создано для хранения количества комментариев под каждой записью 
    form = SerarchRecordForm(request.POST)
    admin_image = ImagesAdmin.objects.all()

    if request.method == 'POST':    
        form = SerarchRecordForm(request.POST)  # Перемещаем создание формы сюда
        if form.is_valid(): 
            value = form.cleaned_data['value']  
            items = br.objects.filter(title__icontains=value)
            for item in items:
                count = Comment.objects.filter(post=item).count()
                count_dict[item.id] = count
                author_info = ExtraInformation.objects.get(author=item.author)
                item.author_info = author_info  # Добавляем информацию о пользователе к записи

    paginator = Paginator(items, 33)  # Переносим создание Paginator сюда
    
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    
    context = {'items': items, 'page': page, 'count_dict': count_dict,  'form': form, 'admin_image':admin_image}
    return render(request, 'samplesearch.html', context)


#вывод данных пользователя для всех желающих
def UserInformations(request, user_id):
    admin_image = ImagesAdmin.objects.all()
    acc = ExtraInformation.objects.filter(author=user_id)
    post = br.objects.filter(author=user_id)
    return render(request, 'user_informations.html', {'admin_image': admin_image, 'acc':acc, 'post':post})