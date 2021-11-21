from rest_framework import permissions
from api_yamdb.settings import PROJECT_SETTINGS


class AdminPermissions(permissions.BasePermission):
    """
    Права на создание, удаление и изменение пользователей.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_superuser
                    or request.user.role == PROJECT_SETTINGS['role']['admin'][0])
        return False


class AdminOrReadOnly(permissions.BasePermission):
    """
    Права для админов на создание произведений, категорий и жанров.
    Права для всех на чтение.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(
                request.user.is_superuser
                or request.user.role == PROJECT_SETTINGS['role']['admin'][0]
            )


class AdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    """
    Права на чтение есть у всех.
    Права на запись есть только у:
        1) авторов ревью и комментов;
        2) модераторов;
        3) админов.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return bool(
                obj.author == request.user
                or request.user.role == PROJECT_SETTINGS['role']['moderator'][0]
                or request.user.role == PROJECT_SETTINGS['role']['admin'][0]
                or request.user.is_superuser
            )
        elif request.method in permissions.SAFE_METHODS:
            return True
        return False
