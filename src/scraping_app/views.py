from gc import get_objects

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import FindForm, VForm
from .models import Vacancy


def home_view(request):
    # print(request.GET)
    form = FindForm()
    return render(request, 'scraping_app/home.html', {'form': form})


def list_view(request):
    # print(request.GET)
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = []
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
        qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
        paginator = Paginator(qs, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping_app/list.html', context)

def v_detail(request, pk=None):
    #object_ = Vacancy.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraping_app/detail.html', {'object': object_})

class VDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping_app/detail.html'
    #context_object_name = 'object'

class VList(ListView):
    model = Vacancy
    template_name = 'scraping_app/list.html'
    form = FindForm()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
        return qs

class VCreate(CreateView):
    model = Vacancy
    form_class = VForm
    template_name = 'scraping_app/create.html'

    def get_success_url(self):
        return reverse_lazy('home')

class VUpdate(UpdateView):
    model = Vacancy
    form_class = VForm
    template_name = 'scraping_app/create.html'

    def get_success_url(self):
        return reverse_lazy('home')

class VDelete(DeleteView):
    model = Vacancy
    #template_name = 'scraping_app/delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, "Запись успешно удалена!")
        return self.post(request, *args, **kwargs)