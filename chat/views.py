from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import ChatRoom, Message
from .forms import MessageForm

# Create your views here.

def room(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            chat_room.messages.add(message)
            return redirect('room', room_name=room_name)
    else:
        form = MessageForm()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'form': form,
        'messages': chat_room.messages.all()
    })
def index(request):
    room_names = ['room1', 'room2']  # Example room names
    return render(request, 'chat/index.html', {'room_names': room_names})