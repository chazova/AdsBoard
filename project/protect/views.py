from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Не забываем импортировать нужные функции и пакеты
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from ads.models import Author


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе premium
@login_required
def upgrade_me(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
       Author.objects.create(author=user)
   return redirect('/')