from django.contrib.auth.models import User
from django.db import models


class EmailUser(User):
    uuid = models.UUIDField()

    def full_name(self):
        return self.first_name+" "+self.last_name
