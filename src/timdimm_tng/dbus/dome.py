
from __future__ import annotations

from typing import Tuple

from sdbus import (
    DbusInterfaceCommon,
    dbus_method,
    dbus_property
)


class Dome(
    DbusInterfaceCommon,
    interface_name='org.kde.kstars.INDI.Dome',
):
    def __init__(self, *args, **kwargs):
        super(Dome, self).__init__(
            service_name="org.kde.kstars",
            object_path="/KStars/INDI/Dome",
            *args,
            **kwargs
        )

    @dbus_method(
        method_name='connect'
    )
    def connect(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method(
        method_name='disconnect'
    )
    def disconnect(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='isParked'
    )
    def is_parked(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='park'
    )
    def park(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='unpark'
    )
    def unpark(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='abort'
    )
    def abort(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='moveCW'
    )
    def move_c_w(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='moveCCW'
    )
    def move_c_c_w(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        input_signature='b',
        result_signature='b',
        method_name='controlShutter'
    )
    def control_shutter(
        self,
        open: bool,
    ) -> bool:
        raise NotImplementedError

    @dbus_method(
        result_signature='b',
        method_name='hasShutter'
    )
    def has_shutter(
        self,
    ) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='s',
        property_name='name'
    )
    def name(self) -> str:
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='connected'
    )
    def connected(self) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='canPark'
    )
    def can_park(self) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='canAbsMove'
    )
    def can_abs_move(self) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='canRelMove'
    )
    def can_rel_move(self) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='canAbort'
    )
    def can_abort(self) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='d',
        property_name='position'
    )
    def position(self) -> float:
        raise NotImplementedError

    @dbus_property(
        property_signature='b',
        property_name='isMoving'
    )
    def is_moving(self) -> bool:
        raise NotImplementedError

    @dbus_property(
        property_signature='i',
        property_name='status'
    )
    def status(self) -> int:
        raise NotImplementedError

    @dbus_property(
        property_signature='i',
        property_name='shutterStatus'
    )
    def shutter_status(self) -> int:
        raise NotImplementedError

    @dbus_property(
        property_signature='i',
        property_name='parkStatus'
    )
    def park_status(self) -> int:
        raise NotImplementedError
