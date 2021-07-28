from django.shortcuts import render

# Create your views here.
import asyncio
import logging

import sqlalchemy
from quart import (Blueprint, copy_current_websocket_context, flash, redirect,
                   render_template, session, websocket)

from camus import db, message_handler
from .forms import *
from .models import Client, Room
from .util import *

bp = Blueprint('main', __name__)


@bp.route('/about')
async def about():
    return redirect('/#why-camus')


# @bp.route('/', methods=['GET', 'POST'])
def index(request):
    create_room_form = CreateRoomForm()
    if request.method == 'POST':
        create_room_form = CreateRoomForm(request.POST)
        if create_room_form.is_valid():
            a = create_room_form.save()
            a.slug = slugify(str(a.id))
            a.save()
            print(a.id)
            return redirect(f"/room/{a.id}")
    return render(request, 'chat.html', {'create_room_form':create_room_form})


# The `/chat` route is deprecated.
# @bp.route('/chat')
# async def chat_index():
#     return redirect('/', code=307)


# The `/chat/` route is deprecated. Prefer`/room/` instead.
# @bp.route('/chat/<room_id>', methods=['GET', 'POST'])
# @bp.route('/room/<room_id>', methods=['GET', 'POST'])
def room(request,room_id):
    pass
    room = Room.objects.filter(id=room_id)
    room1 = Room.objects.get(id=room_id)
    name = request.POST.get('name')
    # if room.is_full():
    #     return 'Guest limit already reached', 418

    # # No password is required to join the room
    # client = room.authenticate()
    if request.method == 'POST':
        a = Client.objects.create(name=name, room_id=room1)
        request.session['id'] = a.name

        return render(request,
            'chatroom.html')

    # # A password is required to join the room
    # status_code = 200
    form = JoinRoomForm()
    
        # await flash('Invalid password')

    return render(request, 'join-room.html', {'title':'Camus | Join a room','form':form, 'room':room})


# The `/chat/` route is deprecated. Prefer`/room/` instead.
# @bp.websocket('/chat/<room_id>/ws')
# @bp.websocket('/room/<room_id>/ws')
async def room_ws(request,room_id):
    # Verify that the room exists
    Room.objects.filter(id=room_id).first_or_404()

    # Verify the client using a secure cookie
    client = Client.objects.filter(name=request.session['id'])
    client1 = Client.objects.get(name=request.session['id'])

    if client:
        client = Client.objects.get(name=request.session['id'])
        logging.info(f'Accepted websocket connection for client {client1.name}')
        await websocket.accept()
    else:
        return 'Forbidden', 403

    inbox, outbox = message_handler.inbox, message_handler.outbox

    send_task = asyncio.create_task(
        copy_current_websocket_context(ws_send)(outbox[client1.name]),
    )
    receive_task = asyncio.create_task(
        copy_current_websocket_context(ws_receive)(client1.name, inbox),
    )
    try:
        await asyncio.gather(send_task, receive_task)
    finally:
        logging.info(f'Terminating websocket connection for client {client1.name}')
        send_task.cancel()
        receive_task.cancel()


@bp.route('/public')
async def public():
    public_rooms = Room.query.filter_by(is_public=True).all()

    return await render_template(
        'public.html', title='Camus Video Chat | Public Rooms',
        public_rooms=public_rooms)


async def ws_send(queue):
    while True:
        message = await queue.get()
        await websocket.send(message)


async def ws_receive(client_id, queue):
    while True:
        message = await websocket.receive()
        await queue.put((client_id, message))
