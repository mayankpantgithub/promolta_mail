# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
import django


# Create your models here.


class EmailThread(models.Model):
    uuid = models.UUIDField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    subject = models.TextField()
    owner = models.ForeignKey('emailuser.EmailUser')
    sent_at = models.DateTimeField(null=True)

    def serialized(self):
        return {
            "draftId": str(self.uuid),
            "subject": self.subject
        }


class EmailElement(models.Model):
    uuid = models.UUIDField()
    text = models.TextField()
    attachments = models.TextField()  # list of attachment urls
    email_thread = models.ForeignKey('emailserver.EmailThread', null=True)
    sender = models.ForeignKey('emailuser.EmailUser')

    def serialized(self):
        return {
            "elementId":str(self.uuid),
            "text": self.text,
            "subject": self.email_thread.subject,
            "attachments": self.attachments,
            "senderName": self.sender.full_name()
        }


class EmailElementMapping(models.Model):
    receiver = models.ForeignKey('emailuser.EmailUser')
    email_element = models.ForeignKey('emailserver.EmailElement')
    is_cc = models.BooleanField(default=False)
    is_bcc = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def serialized(self):
        return {
            "text": self.email_element.text,
            "subject": self.email_thread.subject,
            "receiver": self.receiver.full_name,
            "isCC": self.is_cc,
            "isBCC": self.is_bcc
        }
