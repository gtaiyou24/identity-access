from __future__ import annotations

import datetime
import uuid

from injector import singleton, inject

from application import ApplicationServiceLifeCycle
from application.identity.command import ProvisionTenantCommand, RegisterUserCommand, AuthenticateUserCommand
from application.identity.dpo import UserDpo
from domain.model.mail import MailDeliveryService
from domain.model.tenant import Tenant
from domain.model.user import UserRepository, User, EmailAddress
from exception import SystemException, ErrorCode


@singleton
class IdentityApplicationService:
    @inject
    def __init__(self,
                 application_service_life_cycle: ApplicationServiceLifeCycle,
                 user_repository: UserRepository,
                 mail_delivery_service: MailDeliveryService):
        self.__application_service_life_cycle = application_service_life_cycle
        self.__user_repository = user_repository
        self.__mail_delivery_service = mail_delivery_service

    def provision_tenant(self, command: ProvisionTenantCommand):
        """テナントを作成する"""
        try:
            self.__application_service_life_cycle.begin()

            # テナントを作成する
            tenant = Tenant.provisioned(
                self.__tenant_repository.next_identity(),
                command.tenant_name,
                command.tenant_description
            )

            # テナントを登録する
            self.__tenant_repository.add(tenant)

            # 管理者を追加する
            invitation = tenant.offer_registration_invitation("init").open_end()

            self.__application_service_life_cycle.success()
        except Exception as e:
            self.__application_service_life_cycle.fail(e)

    def register_user(self, command: RegisterUserCommand) -> UserDpo:
        """ユーザー登録"""
        user = User.new(
            EmailAddress(command.email_address),
            command.plain_password,
        )
        if self.__user_repository.user_with_email_address(user.email_address):
            raise SystemException(ErrorCode.REGISTER_USER_ALREADY_EXISTS, 'ユーザー登録に失敗しました。')

        self.__user_repository.add(user)

        verification_token = uuid.uuid4()
        expires = datetime.datetime.now() + datetime.timedelta(minutes=10)
        self.__mail_delivery_service.send(user.email_address, '【Epic Bot】メールアドレスの検証', """Hi there""")

        return UserDpo(user)

    def authenticate_user(self, command: AuthenticateUserCommand) -> UserDpo | None:
        """ユーザー認証"""
        email_address = EmailAddress(command.email_address)
        user = self.__user_repository.user_with_email_address(email_address)

        # 該当ユーザーが存在するか、パスワードは一致しているか
        if user is None or not user.verify_password(command.password):
            raise SystemException(ErrorCode.LOGIN_BAD_CREDENTIALS, 'ユーザーが見つかりませんでした。')

        return UserDpo(user)

    def user(self, email_address: str) -> UserDpo | None:
        user = self.__user_repository.user_with_email_address(EmailAddress(email_address))
        if user is None:
            return None
        return UserDpo(user)
