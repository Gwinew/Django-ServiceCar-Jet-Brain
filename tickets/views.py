from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

name_ticket = {
    'change_oil': 'Change oil',
    'inflate_tires': 'Inflate tires',
    'diagnostic': 'Get diagnostic test'
}

get_ticket = {
    'change_oil': [],
    'inflate_tires': [],
    'diagnostic': []
}
i = 0
info = None
class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

class MenuPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "tickets/menu.html", context={'get_ticket': name_ticket})

class GetTicket(View):
    def calculate(self, link):
        for k, v in get_ticket.items():
            if k == 'change_oil':
                self.get_time_c = len(v) * 2
            if k == 'inflate_tires':
                self.get_time_i = len(v) * 5
            if k == 'diagnostic':
                self.get_time_d = len(v) * 30
        if link == 'change_oil':
            self.get_time = self.get_time_c
        elif link == 'inflate_tires':
            self.get_time = self.get_time_c + self.get_time_i
        elif link == 'diagnostic':
            self.get_time = self.get_time_c + self.get_time_i + self.get_time_d
        return self.get_time

    def get(self, request, link, *args, **kwargs):
        global i
        i += 1
        self.a = self.calculate(link)
        context = {'num': i, 'calc': self.a}
        get_ticket[link].append(i)
        return render(request, "tickets/getticket.html", context)

class NextView(TemplateView):
    template_name = 'tickets/next.html'

    def get_context_data(self, **kwargs):
        context = {}
        global info
        if info == None:
            context['context'] = 'Waiting for the next client'
        else:
            context['context'] = f'Next ticket #{info}'
        return context

class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        for k, v in get_ticket.items():
            if k == 'change_oil':
                self.get_c = len(v)
            if k == 'inflate_tires':
                self.get_i = len(v)
            if k == 'diagnostic':
                self.get_d = len(v)
        context = {"c": self.get_c, "i": self.get_i, "d": self.get_d}
        return render(request, "tickets/processing.html", context)

    def post(self, request, *args, **kwargs):
        global info
        for k, v in get_ticket.items():
            if k == 'change_oil' and len(v) != 0:
                info = get_ticket['change_oil'].pop(0)
                return redirect('/processing')
            elif k == 'inflate_tires' and len(v) != 0:
                info = get_ticket['inflate_tires'].pop(0)
                return redirect('/processing')
            elif k == 'diagnostic' and len(v) != 0:
                info = get_ticket['diagnostic'].pop(0)
                return redirect('/processing')
        info = None
        return redirect('/processing')
