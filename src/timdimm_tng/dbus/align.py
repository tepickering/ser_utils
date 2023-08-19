
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusDeprecatedFlag, DbusInterfaceCommonAsync,
                   DbusNoReplyFlag, DbusPropertyConstFlag,
                   DbusPropertyEmitsChangeFlag,
                   DbusPropertyEmitsInvalidationFlag, DbusPropertyExplicitFlag,
                   DbusUnprivilegedFlag, dbus_method_async,
                   dbus_property_async, dbus_signal_async)


class OrgKdeKstarsEkosAlignInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.kstars.Ekos.Align',
):

    @dbus_method_async(
    )
    async def abort(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='b',
    )
    async def capture_and_solve(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
        result_signature='b',
    )
    async def load_and_slew(
        self,
        file_u_r_l: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='u',
    )
    async def set_solver_mode(
        self,
        mode: int,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
    )
    async def set_solver_action(
        self,
        mode: int,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='ad',
    )
    async def camera_info(
        self,
    ) -> List[float]:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='ad',
    )
    async def get_solution_result(
        self,
    ) -> List[float]:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='ad',
    )
    async def telescope_info(
        self,
    ) -> List[float]:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='i',
    )
    async def get_load_and_slew_status(
        self,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
    )
    async def set_binning_index(
        self,
        binning_index: int,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='dd',
    )
    async def set_target_coords(
        self,
        ra: float,
        de: float,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='ad',
    )
    async def get_target_coords(
        self,
    ) -> List[float]:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='d',
    )
    async def set_target_position_angle(
        self,
        value: float,
    ) -> None:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def optical_train(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def camera(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def filter_wheel(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def filter(self) -> str:
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

    @dbus_property_async(
        property_signature='ad',
    )
    def fov(self) -> List[float]:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def solver_arguments(self) -> str:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='(i)',
    )
    def new_status(self) -> Tuple[int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='a{sv}',
    )
    def new_solution(self) -> Dict[str, Tuple[str, Any]]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='s',
    )
    def new_log(self) -> str:
        raise NotImplementedError

