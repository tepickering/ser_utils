
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdbus import (DbusDeprecatedFlag, DbusInterfaceCommonAsync,
                   DbusNoReplyFlag, DbusPropertyConstFlag,
                   DbusPropertyEmitsChangeFlag,
                   DbusPropertyEmitsInvalidationFlag, DbusPropertyExplicitFlag,
                   DbusUnprivilegedFlag, dbus_method_async,
                   dbus_property_async, dbus_signal_async)


class OrgKdeKstarsEkosCaptureInterface(
    DbusInterfaceCommonAsync,
    interface_name='org.kde.kstars.Ekos.Capture',
):

    @dbus_method_async(
    )
    async def start(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def abort(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def suspend(
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
    async def pause(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def toggle_sequence(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
    )
    async def restart_camera(
        self,
        name: str,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='b',
    )
    async def toggle_video(
        self,
        enabled: bool,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='sb',
        result_signature='b',
    )
    async def load_sequence_queue(
        self,
        file_u_r_l: str,
        ignore_target: bool,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='s',
        result_signature='b',
    )
    async def save_sequence_queue(
        self,
        path: str,
    ) -> bool:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def clear_sequence_queue(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='s',
    )
    async def get_sequence_queue_status(
        self,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='bd',
    )
    async def set_maximum_guiding_deviation(
        self,
        enable: bool,
        value: float,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='bd',
    )
    async def set_in_sequence_focus(
        self,
        enable: bool,
        h_f_r: float,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='i',
    )
    async def get_job_count(
        self,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='i',
    )
    async def get_pending_job_count(
        self,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='s',
    )
    async def get_job_state(
        self,
        id: int,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='s',
    )
    async def get_job_filter_name(
        self,
        id: int,
    ) -> str:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='i',
    )
    async def get_job_image_progress(
        self,
        id: int,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='i',
    )
    async def get_job_image_count(
        self,
        id: int,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='d',
    )
    async def get_job_exposure_progress(
        self,
        id: int,
    ) -> float:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='d',
    )
    async def get_job_exposure_duration(
        self,
        id: int,
    ) -> float:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='i',
        result_signature='i',
    )
    async def get_job_frame_type(
        self,
        id: int,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='d',
    )
    async def get_progress_percentage(
        self,
    ) -> float:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='i',
    )
    async def get_active_job_i_d(
        self,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='i',
    )
    async def get_active_job_remaining_time(
        self,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
        result_signature='i',
    )
    async def get_overall_remaining_time(
        self,
    ) -> int:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def clear_auto_focus_h_f_r(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
    )
    async def ignore_sequence_history(
        self,
    ) -> None:
        raise NotImplementedError

    @dbus_method_async(
        input_signature='si',
    )
    async def set_captured_frames_map(
        self,
        signature: str,
        count: int,
    ) -> None:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def target_name(self) -> str:
        raise NotImplementedError

    @dbus_property_async(
        property_signature='s',
    )
    def observer_name(self) -> str:
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
        property_signature='b',
    )
    def cooler_control(self) -> bool:
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
        signal_signature='s',
    )
    def new_log(self) -> str:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def meridian_flip_started(self) -> None:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='(i)',
    )
    def new_status(self) -> Tuple[int]:
        raise NotImplementedError

    @dbus_signal_async(
        signal_signature='a{sv}',
    )
    def capture_complete(self) -> Dict[str, Tuple[str, Any]]:
        raise NotImplementedError

    @dbus_signal_async(
    )
    def ready(self) -> None:
        raise NotImplementedError

