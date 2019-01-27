# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid

from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from emailuser.models import EmailUser
from common.errors import BadRequestError
from common.responses import Response


# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny], )
def create(request):
    request_data = json.loads(request.body)
    email = request_data.get("email")
    first_name = request_data.get("firstName")
    last_name = request_data.get("lastName")
    password = request.data.get("password")

    user = EmailUser.objects.filter(email=email)
    if user:
        return BadRequestError("user already exists")
    else:
        if not password:
            return BadRequestError("Please enter password")
        user = EmailUser.objects.create(email=email, first_name=first_name, last_name=last_name, username=email,
                                        uuid=uuid.uuid4())
        user.set_password(password)
        token = Token.objects.create(user=user)
        data = {
            "token": token.key,
            "uuid": str(user.uuid)
        }

        return Response(data=data)



@api_view(['POST'])
@permission_classes([AllowAny], )
def get_token(request):
    request_data = json.loads(request.body)
    email = request_data.get("email")
    password = request_data.get("password")
    try:
        user = EmailUser.objects.get(email=email)
    except:
        return BadRequestError("user not found")

    if user.check_password(password):
        token = user.get_token()
        data = {
            "token":token
        }
        return Response(data=data)
    else:
        return BadRequestError("Wrong password")
