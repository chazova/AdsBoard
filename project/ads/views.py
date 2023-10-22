from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import render, reverse, redirect
from .models import *
from .filters import AdsFilter, RepliesFilter
from .forms import AdsForm, ReplyForm, ImageForm, VideoForm
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


class AdList(FilterView):
    model = Ad
    template_name = 'ads/ads.html'
    context_object_name = 'ads'
    ordering = ['-create_time']  # сортировка по времени в порядке убывания
    paginate_by = 30  # поставим постраничный вывод в один элемент
    filterset_class = AdsFilter

    def get_queryset(self):
        queryset = AdsFilter(self.request.GET, super().get_queryset()).qs
        return queryset
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdsFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = AdsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


# дженерик для получения деталей о товаре
class AdDetailView(DetailView):
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'
    queryset = Ad.objects.all()

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_ad = context['object']
        context['videos'] = Video.objects.filter(ad=current_ad)
        print(context)
        return context




# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class AdCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'ads/ad_create.html'
    form_class = AdsForm
    permission_required = ('ads.add_ad',)

    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.author = Author.objects.get(author=self.request.user)
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)


# дженерик для редактирования объекта
class AdUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'ads/ad_create.html'
    form_class = AdsForm
    permission_required = ('ads.change_ad',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)


# дженерик для удаления товара
class AdDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'ads/ad_delete.html'
    context_object_name = 'ad'
    queryset = Ad.objects.all()
    success_url = reverse_lazy('ads:ads')  # не забываем импортировать функцию reverse_lazy из пакета django.urls
    permission_required = ('ads.delete_ad',)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ads/reply_create.html'
    form_class = ReplyForm

    def form_valid(self, form, **kwargs):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна

        fields.ad = Ad.objects.get(pk=self.kwargs.get("ad_id"))
        fields.user = User.objects.get(username=self.request.user.username)
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)

    success_url = reverse_lazy('ads:ads')


class UserAdsList(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/user_ads.html'
    context_object_name = 'ads'
    ordering = ['-create_time']

    def get_queryset(self):
        queryset = Ad.objects.filter(author__author=self.request.user)
        return queryset

class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'ads/replies.html'
    context_object_name = 'replies'
    ordering = ['-create_time']

    def get_queryset(self):
        queryset = Reply.objects.filter(ad__author__author=self.request.user)
        queryset = RepliesFilter(self.request.GET, queryset).qs
        return queryset

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = RepliesFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


@login_required
def confirm_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    reply.is_confirm = 'true'
    reply.save()
    return redirect('/ads/replies/')

@login_required
def delete_reply(request, reply_id):
    reply = Reply.objects.get(pk=reply_id)
    reply.delete()
    return redirect('/ads/replies/')


# class ImageAddView(LoginRequiredMixin, CreateView):
#     template_name = 'ads/image_add.html'
#     form_class = ImageForm
#
#     def form_valid(self, form, **kwargs):
#         fields = form.save(commit=False)
#         fields.ad = Ad.objects.get(pk=self.kwargs.get("ad_id"))
#         fields.save()
#         return super().form_valid(form)
#
#     success_url = reverse_lazy('/')

def upload_image(request, ad_id):
    current_ad = Ad.objects.get(pk=ad_id)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Image(ad=current_ad, image=request.FILES["image"])
            instance.save()
            return redirect("/")
    else:
        form = ImageForm
    return render(request, "ads/image_add.html", {"form": form})

def upload_video(request, ad_id):
    current_ad = Ad.objects.get(pk=ad_id)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            instance = Video(ad=current_ad, embed_video=request.POST["embed_video"])
            instance.save()
            return redirect("/")
    else:
        form = VideoForm
    return render(request, "ads/video_add.html", {"form": form})

