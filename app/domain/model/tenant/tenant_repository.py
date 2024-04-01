import abc

from domain.model.tenant import TenantId, Tenant


class TenantRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> TenantId:
        pass

    @abc.abstractmethod
    def add(self, tenant: Tenant) -> None:
        pass
