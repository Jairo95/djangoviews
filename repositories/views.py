from django.shortcuts import render
from django.views.generic import (
    View,
    TemplateView,
    RedirectView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


from .models import Locker, Folder, Document
from .forms import LockerForm, FolderForm, DocumentForm


def lockers(request):
    qs = Locker.objects.all().order_by('-id')
    context = {}
    context['lockers'] = qs
    return render(request=request, template_name='repositories/lockers/lockers.html', context=context)


class FoldersView(View):

    def get(self, request, locker_pk):
        qs = Folder.objects.filter(locker__pk=locker_pk).order_by('-id')
        context = {}
        context['folders'] = qs
        context['kwargs'] = {
            'locker_pk': locker_pk
        }
        return render(request=request, template_name='repositories/folders/folders.html', context=context)


class LockerCreateView(CreateView):
    model = Locker
    form_class = LockerForm
    template_name = 'repositories/lockers/locker_form.html'

    def get_success_url(self):
        return reverse('repositories:locker_edit', kwargs={
            'pk': self.object.pk
        })


class LockerUpdateView(UpdateView):
    model = Locker
    form_class = LockerForm
    template_name = 'repositories/lockers/locker_form.html'

    def get_success_url(self):
        return reverse('repositories:locker_edit', kwargs={
            'pk': self.object.pk
        })


class LockerDeleteView(DeleteView):
    model = Locker
    template_name = 'repositories/lockers/locker_form.html'


class FolderView(FormView):
    form_class = FolderForm
    template_name = 'repositories/folders/folder_form.html'
    
    def get_object(self):
        folder = None
        if 'pk' in self.kwargs:
            folder = Folder.objects.filter(pk=self.kwargs.get('pk')).first()
        return folder

    def get_initial(self):
        initial = super().get_initial()
        initial['locker'] = Locker.objects.filter(pk=self.kwargs.get('locker_pk')).first()
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        folder = self.get_object()

        if folder is not None:
            return form_class(instance=folder, **self.get_form_kwargs())
        else:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        folder = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse(
            'repositories:folders', kwargs={
                'locker_pk': self.kwargs.get('locker_pk')
            }
        )


class FolderDeleteView(View):
    
    def get(self, request, locker_pk, pk):
        Folder.objects.filter(pk=pk).delete()

        return HttpResponseRedirect(
            reverse(
                'repositories:folders',
                kwargs={'locker_pk': locker_pk}
                )
            )


class DocumentsView(ListView):
    model = Document
    context_object_name = 'documents'
    template_name = 'repositories/documents/documents.html'

    def get_queryset(self):
        qs = Document.objects.filter(folder__pk=self.kwargs.get('folder_pk')).order_by('-id')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kwargs'] = self.kwargs
        return context


class DocumentView(TemplateView):
    template_name = 'repositories/documents/document_form.html'

    def get_object(self):
        document = Document.objects.filter(pk=self.kwargs.get('pk')).first() if 'pk' in self.kwargs else None
        return document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        initial = {}
        initial['folder'] = Folder.objects.filter(pk=self.kwargs.get('folder_pk')).first()

        document = self.get_object()
        context['form'] = DocumentForm(instance=document, initial=initial)
        context['kwargs'] = self.kwargs
        return context

    def post(self, request, locker_pk, folder_pk, *args, **kwargs):
        document = self.get_object()
        form = DocumentForm(data=request.POST, instance=document)
        document = form.save()

        return HttpResponseRedirect(
            reverse('repositories:documents', kwargs={
                'locker_pk': locker_pk,
                'folder_pk': folder_pk
            }))


class HomeView(RedirectView):
    url = reverse_lazy('repositories:lockers')


class DocumenteDeleteView(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):

        Document.objects.filter(pk=self.kwargs.get('pk')).delete()
        return reverse(
            'repositories:documents', kwargs={
                'locker_pk': self.kwargs.get('locker_pk'),
                'folder_pk': self.kwargs.get('folder_pk'),
            }
        )


class LockerDetailView(DetailView):
    model = Locker
    template_name = 'repositories/lockers/locker_form.html'




