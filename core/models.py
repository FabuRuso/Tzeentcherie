from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    forename = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100)
    password_hs = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    pass

class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)

    god_perm = models.BooleanField(default=False)

    edit_roles_perm = models.BooleanField(default=False)

    post_owned_perm = models.BooleanField(default=True)
    put_owned_perm = models.BooleanField(default=True)
    delete_owned_perm = models.BooleanField(default=True)

    put_not_owned_perm = models.BooleanField(default=False)
    delete_not_owned_perm = models.BooleanField(default=False)

    put_users_perm = models.BooleanField(default=False)
    deactivate_users_perm = models.BooleanField(default=False)  # <== 'soft' deactivation,  saving in db
    delete_users_perm = models.BooleanField(default=False)      # <==  full  deletion,      removing from db

    pass

class RoleAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role', unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='assignments_set')
    pass

class Tzeentcherie(models.Model):
    title = models.CharField(max_length=511, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_set')
    created_at = models.DateTimeField(auto_now_add=True)

    pass