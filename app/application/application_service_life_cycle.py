from typing import Optional

from injector import singleton, inject

from application import UnitOfWork


@singleton
class ApplicationServiceLifeCycle:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    def begin(self, is_listening: bool = True) -> None:
        if is_listening:
            self.listen()
        self.__unit_of_work.start()

    def fail(self, exception: Optional[Exception] = None) -> None:
        self.__unit_of_work.rollback()
        if exception is not None:
            raise exception

    def success(self) -> None:
        self.__unit_of_work.commit()

    def listen(self) -> None:
        pass