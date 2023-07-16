from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,
        )
        send_mail(
            subject='Вас приглашают стать агентом',
            message='Вы были добавлены в систему XCRM, войдите в систему чтобы начать работать',
            from_email='admin@mail.com',
            recipient_list=[user.email],
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)

    def get_success_url(self):
        return reverse('agents:agent-list')


class AgentDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)

    def get_success_url(self):
        return reverse('agents:agent-list')
