from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Lead, Agent, Category
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm
from agents.mixins import OrganisorAndLoginRequiredMixin


class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        """Начальный набор запросов состоит из потенциальных клиентов для всей организации"""
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            """Фильтруем потенциальных клиентов для агента вошедшего в систему"""
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({'unassigned_leads': queryset})
        return context


class LeadDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        """Начальный набор запросов состоит из потенциальных клиентов для всей организации"""
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            """Фильтруем потенциальных клиентов для агента вошедшего в систему"""
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        """Начальный набор запросов состоит из потенциальных клиентов для всей организации"""
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            """Фильтруем потенциальных клиентов для агента вошедшего в систему"""
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        # send email
        send_mail(
            subject='Новый клиент был создан',
            message= 'Переходи на сайт',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    #queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        """Начальный набор запросов состоит из потенциальных клиентов для всей организации"""
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            """Фильтруем потенциальных клиентов для агента вошедшего в систему"""
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')

    def get_queryset(self):
        user = self.request.user
        """исходный набор лидов для всей организации"""
        return Lead.objects.filter(organisation=user.userprofile)


class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    #def get_form_kwargs(self, **kwargs):
    #    kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
    #    kwargs.update({
    #        'request': self.request
    #    })
    #    return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)

        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        """Начальный набор запросов состоит из потенциальных клиентов для всей организации"""
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

#def lead_detail(request, pk):
#    lead = Lead.objects.get(id=pk)
#    context = {
#        'lead': lead
#    }
#    return render(request, 'leads/lead_detail.html', context)


#def lead_create(request):
#    form = LeadModelForm()
#    if request.method == 'POST':
#        form = LeadModelForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('/leads')
#    context = {
#        'form': form
#    }
#    return render(request, 'leads/lead_create.html', context)


#def lead_update(request, pk):
#    lead = Lead.objects.get(id=pk)
#    form = LeadModelForm(instance=lead)
#    if request.method == 'POST':
#        form = LeadModelForm(request.POST, instance=lead)
#        if form.is_valid():
#            form.save()
#            return redirect('/leads')
#    context = {
#            'form': form,
#            'lead': lead
#        }
#    return render(request, 'leads/lead_update.html', context)


#def lead_delete(request, pk):
#    lead = Lead.objects.get(id=pk)
#    lead.delete()
#    return redirect('/leads')


#def lead_update(request, pk):
#    lead = Lead.objects.get(id=pk)
#    form = LeadForm()
#    if request.method == 'POST':
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            agent = form.cleaned_data['agent']
#            lead.first_name = first_name
#            lead.age = age
#            lead.agent = agent
#            lead.save()
#            return redirect('/leads')
#    context = {
#        'form': form,
#        'lead': lead
#    }
#    return render(request, 'leads/lead_update.html', context)

#def lead_c(request):
#    form = LeadForm()
#    if request.method == 'POST':
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            agent = Agent.objects.first()
#            Lead.objects.create(
#                first_name=first_name,
#                last_name=last_name,
#                age=age,
#                agent=agent
#           )
#           return redirect('/leads')

#    context = {
#        'form': LeadForm
#    }
#    return render(request, 'leads/lead_create.html', context)
