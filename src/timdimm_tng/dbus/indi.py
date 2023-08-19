
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusDeprecatedFlag, DbusInterfaceCommonAsync,
                   DbusNoReplyFlag, DbusPropertyConstFlag,
                   DbusPropertyEmitsChangeFlag,
                   DbusPropertyEmitsInvalidationFlag, DbusPropertyExplicitFlag,
                   DbusUnprivilegedFlag, dbus_method_async,
                   dbus_property_async, dbus_signal_async)


class OrgKdeKstarsINDIInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.kstars.INDI',
):

    @dbus_method_async(
        input_signature='ias',
        result_signature='b',
    )
    async def start(
        self,
        port: int,
        drivers: List[str],
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
        result_signature='b',
    )
    async def stop(
        self,
        port: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='si',
        result_signature='b',
    )
    async def connect(
        self,
        host: str,
        port: int,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='si',
        result_signature='b',
    )
    async def disconnect(
        self,
        host: str,
        port: int,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='as',
    )
    async def get_devices(
        self,
    ) -> List[str]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
        result_signature='as',
    )
    async def get_properties(
        self,
        device: str,
    ) -> List[str]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='ss',
        result_signature='s',
    )
    async def get_property_state(
        self,
        device: str,
        property: str,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='as',
    )
    async def get_devices_paths(
        self,
        interface: int,
    ) -> List[str]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='ss',
        result_signature='b',
    )
    async def send_property(
        self,
        device: str,
        property: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sss',
        result_signature='s',
    )
    async def get_light(
        self,
        device: str,
        property: str,
        light_name: str,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='ssss',
        result_signature='b',
    )
    async def set_switch(
        self,
        device: str,
        property: str,
        switch_name: str,
        status: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sss',
        result_signature='s',
    )
    async def get_switch(
        self,
        device: str,
        property: str,
        switch_name: str,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='ssss',
        result_signature='b',
    )
    async def set_text(
        self,
        device: str,
        property: str,
        text_name: str,
        text: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sss',
        result_signature='s',
    )
    async def get_text(
        self,
        device: str,
        property: str,
        text_name: str,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sssd',
        result_signature='b',
    )
    async def set_number(
        self,
        device: str,
        property: str,
        number_name: str,
        value: float,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sss',
        result_signature='d',
    )
    async def get_number(
        self,
        device: str,
        property: str,
        number_name: str,
    ) -> float:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sss',
        result_signature='aysi',
    )
    async def get_b_l_o_b_data(
        self,
        device: str,
        property: str,
        blob_name: str,
    ) -> Tuple[bytes, str, int]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sss',
        result_signature='ssi',
    )
    async def get_b_l_o_b_file(
        self,
        device: str,
        property: str,
        blob_name: str,
    ) -> Tuple[str, str, int]:
        raise NotImplementedError

