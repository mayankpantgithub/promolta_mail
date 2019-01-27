# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid
# Create your views here.
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from common.responses import Response
from common.errors import BadRequestError
from common.file_helper import save_file
from emailserver.models import EmailThread, EmailElementMapping, EmailElement
from emailuser.models import EmailUser


@api_view(['POST'])
@permission_classes([IsAuthenticated], )
def compose(request):
    request_body = json.loads(request.body)
    text = request_body.get("text")
    user = EmailUser.objects.get(user_ptr=request.user)
    parent_id = request_body.get("parentId") or None
    subject = request_body.get("subject")
    email_thread = EmailThread.objects.create(owner=user, uuid=uuid.uuid4(), subject=subject)
    email_element = EmailElement.objects.create(email_thread=email_thread, text=text, sender=user, uuid=uuid.uuid4())
    data = {
        "emailThread": email_thread.serialized(),
        "emailElement": email_element.serialized()
    }
    return Response(data=data,message="Draft saved")


@api_view(['POST'])
@permission_classes([IsAuthenticated], )
def send(request):
    request_body = json.loads(request.body)
    text = request_body.get("text")
    user = EmailUser.objects.get(user_ptr=request.user)

    email_element_id = request_body.get("emailElementId")
    email_element = EmailElement.objects.get(uuid=email_element_id)
    receiver_list = request_body.get("receiverList")
    if not receiver_list:
        return BadRequestError("Receiver field empty")

    for receiver_uuid in receiver_list:
        receiver = EmailUser.objects.get(uuid=receiver_uuid)
        EmailElementMapping.objects.create(receiver=receiver, email_element=email_element)
    data = {
        "emailElement": email_element.serialized()
    }
    return Response(data=data,message= "Message sent")


@api_view(['POST'])
@permission_classes([IsAuthenticated], )
def delete(request):
    request_body = json.loads(request.body)
    draft_id = request_body.objects.get("draftId")
    element_id = request_body.objects.get("elementId")
    if draft_id:
        email_thread = EmailThread.objects.get(uuid=draft_id)
        user = EmailUser.objects.get(user_ptr=request.user)
        EmailElementMapping.objects.filter(email_thread=email_thread, receiver=user).update(is_deleted=True)
    else:
        EmailElementMapping.objects.filter(uuid=element_id).update(is_deleted=True)

    return Response(data={},message="Deleted Successfully")


@api_view(['GET'])
@permission_classes([IsAuthenticated], )
def unread(request):
    user = EmailUser.objects.get(user_ptr=request.user)

    email_mappings = EmailElementMapping.objects.filter(is_read=False, receiver=user)
    unread_threads = {}
    for email_mapping in email_mappings:
        if unread_threads.has_key(email_mapping.email_element.email_thread.uuid):
            continue
        else:
            unread_threads[
                str(
                    email_mapping.email_element.email_thread.uuid)] = email_mapping.email_element.email_thread.serialized()

    return Response({"data": unread_threads})


@api_view(['POST'])
@permission_classes([IsAuthenticated], )
def read_mail(request):
    user = EmailUser.objects.get(user_ptr=request.user)
    request_body = json.loads(request.body)
    draft_id = request_body.get("draftId")
    email_thread = EmailThread.objects.get(uuid=draft_id)
    email_elements = EmailElement.objects.filter(email_thread=email_thread)
    unread_threads = {}
    for email_element in email_elements:
        email_mappings = EmailElementMapping.objects.filter(is_read=False, email_element=email_element, receiver=user)

        for email_mapping in email_mappings:
            email_mapping.is_read = True
            email_mapping.save()
            if unread_threads.has_key(email_mapping.email_element.email_thread.uuid):
                continue
            else:
                unread_threads[str(
                    email_mapping.email_element.email_thread.uuid)] = email_mapping.email_element.email_thread.serialized()

    return Response({"data": unread_threads})


@api_view(['POST'])
@permission_classes([IsAuthenticated], )
def upload(request):
    request_body = json.loads(request.body)
    element_id = request_body.get("elementId")
    file = request.FILES['myfile']
    email_element = EmailElement.objects.select_for_update(uuid=element_id)
    if not email_element:
        return BadRequestError("Email not found")
    file_url = save_file(file)

    if not email_element.attachments:
        email_element.attachments = []
    email_element.attachments.append(file_url)

    return Response({"url": file_url})

