

from django.views.generic import CreateView, UpdateView


class RootCreateView(CreateView):
    context_object_name = 'profile_obj'


class RootUpdateView(UpdateView):

    create = False

    def get_form_kwargs(self, **kwargs):
        kwargs = super(RootUpdateView, self).get_form_kwargs(**kwargs)
        kwargs['data'] = kwargs.get('data', {}).copy()
        kwargs['user'] = self.request.user
        return kwargs
