from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from base.forms import RoomForm
from base.models import Room
from base.models import Message


def hello(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Hello {s}")


# def rooms(request):
#     rooms = Room.objects.all()
#     context = {'rooms': rooms}
#     return render(request, template_name='base/rooms.html', context=context)

class RoomsView(ListView):
    template_name = 'base/rooms.html'
    model = Room


def room(request, pk):
    room = Room.objects.get(id=pk)

    #POST
    if request.method == "POST":
        Message.objects.create(
            body=request.POST.get('body'),
            room=room,
            user=request.user
        )
        room.participants.add(request.user)
        room.save()
        return redirect('room', pk=pk)

    #GET
    messages = room.message_set.all()
    context = {'messages': messages, 'room': room}
    return render(request, template_name='base/room.html', context=context)


class RoomCreateView(CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    extra_context = {'title': 'CREATE ROOM'}

    # def form_valid(self, form):
    #     cleaned_data = form.cleaned_data
    #     Room.objects.create(
    #         name=cleaned_data['name'],
    #         description=cleaned_data['description']
    #     )
    #     return super().form_valid(form)


class RoomUpdateView(UpdateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    extra_context = {'title': 'UPDATE ROOM'}
    model = Room


class RoomDeleteView(DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    success_url = reverse_lazy('rooms')