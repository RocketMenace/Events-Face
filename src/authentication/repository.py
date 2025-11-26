from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

from .dto import UserCredentialsDTO, UserDTO
from .exceptions import UserAlreadyExists
from .models import CustomUser


class UserRepository:
    model = CustomUser

    def create(self, dto: UserDTO) -> UserDTO:
        try:
            obj = self.model.objects.create_user(
                username=dto.username,
                password=dto.password,
            )
            obj.full_clean()
            obj.save()
            return UserDTO(id=obj.id, username=obj.username)

        except IntegrityError as e:
            if "username" in str(e) or "users_username_key" in str(e):
                raise UserAlreadyExists
            raise
        except ValidationError:
            raise

    def get_user_by_username(self, credentials: UserCredentialsDTO) -> CustomUser:
        try:
            obj = self.model.objects.filter(
                is_active=True,
                username=credentials.username,
            ).first()
            return obj
        except ObjectDoesNotExist:
            raise
