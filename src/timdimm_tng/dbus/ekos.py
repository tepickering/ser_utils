
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusDeprecatedFlag, DbusInterfaceCommonAsync,
                   DbusNoReplyFlag, DbusPropertyConstFlag,
                   DbusPropertyEmitsChangeFlag,
                   DbusPropertyEmitsInvalidationFlag, DbusPropertyExplicitFlag,
                   DbusUnprivilegedFlag, dbus_method_async,
                   dbus_property_async, dbus_signal_async)


class OrgKdeKstarsEkosInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.kstars.Ekos',
):

    @dbus_method_async(
    )
    async def connect_devices(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def disconnect_devices(
        self,
    ) -> None:
        raise NotImplementedError

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
        result_signature='as',
    )
    async def get_profiles(
        self,
    ) -> List[str]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
        result_signature='b',
    )
    async def set_profile(
        self,
        profile_name: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='b',
    )
    async def set_ekos_live_connected(
        self,
        enabled: bool,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='bb',
    )
    async def set_ekos_live_config(
        self,
        remember_credentials: bool,
        auto_connect: bool,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='ss',
    )
    async def set_ekos_live_user(
        self,
        username: str,
        password: str,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sb',
    )
    async def set_ekos_logging_enabled(
        self,
        name: str,
        enabled: bool,
    ) -> None:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='i',
    )
    def indi_status(self) -> int:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='i',
    )
    def ekos_status(self) -> int:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='u',
    )
    def settle_status(self) -> int:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='b',
    )
    def ekos_live_status(self) -> bool:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='as',
    )
    def log_text(self) -> List[str]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='(i)',
    )
    def indi_status_changed(self) -> Tuple[int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='(i)',
    )
    def ekos_status_changed(self) -> Tuple[int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='(i)',
    )
    def settle_status_changed(self) -> Tuple[int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='b',
    )
    def ekos_live_status_changed(self) -> bool:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def new_log(self) -> str:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def new_module(self) -> str:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='si',
    )
    def new_device(self) -> Tuple[str, int]:
        raise NotImplementedError

