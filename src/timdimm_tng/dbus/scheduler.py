
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusDeprecatedFlag, DbusInterfaceCommonAsync,
                   DbusNoReplyFlag, DbusPropertyConstFlag,
                   DbusPropertyEmitsChangeFlag,
                   DbusPropertyEmitsInvalidationFlag, DbusPropertyExplicitFlag,
                   DbusUnprivilegedFlag, dbus_method_async,
                   dbus_property_async, dbus_signal_async)


class OrgKdeKstarsEkosSchedulerInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.kstars.Ekos.Scheduler',
):

    @dbus_method_async(
    )
    async def start(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def stop(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def remove_all_jobs(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
        result_signature='b',
    )
    async def load_scheduler(
        self,
        file_u_r_l: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
    )
    async def set_sequence(
        self,
        sequence_file_u_r_l: str,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def reset_all_jobs(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def profile(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='as',
    )
    def log_text(self) -> List[str]:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='i',
    )
    def status(self) -> int:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='(i)',
    )
    def new_status(self) -> Tuple[int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def new_log(self) -> str:
        raise NotImplementedError

