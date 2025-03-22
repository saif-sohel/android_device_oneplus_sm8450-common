#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# Copyright (C) 2016 The CyanogenMod Project
# Copyright (C) 2017-2020 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oneplus/sm8450-common',
]

blob_fixups: blob_fixups_user_type = {
    'odm/etc/camera/CameraHWConfiguration.config': blob_fixup()
        .regex_replace('(SystemCamera = )1;', '\\10;')
        .regex_replace('(SystemCamera = )0;$', '\\11;'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libinput_shim.so')
        .replace_needed('android.hidl.base@1.0.so', 'libhidlbase.so'),
    'vendor/etc/seccomp_policy/wfdhdcphalservice.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
    'vendor/etc/media_*/video_system_specs.json': blob_fixup()
        .regex_replace('(max_retry_alloc_output_timeout": )1000', '\\10'),
    'vendor/etc/msm_irqbalance.conf': blob_fixup()
        .regex_replace('IGNORED_IRQ=27,23,38$', 'IGNORED_IRQ=27,23,38,115,332'),
    'vendor/lib64/sensors.ssc.so': blob_fixup()
        .replace_hex_string('qti.sensor.wise_light', 'android.sensor.light\x00')
        .sigscan('F1 E9 D3 84 52 49 3F A0 72', 'F1 A9 00 80 52 09 00 A0 72'),
    'vendor/bin/hw/android.hardware.security.keymint-service-qti': blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'odm/etc/init/vendor.oplus.hardware.biometrics.fingerprint@2.1-service.rc': blob_fixup()
        .regex_replace('chown system system /sys/kernel/oplus_display/hbm', 
                      'chmod 0000 /sys/kernel/oplus_display/hbm'),
    'odm/lib64/libEIS.so': blob_fixup()
        .replace_needed('libui.so', 'libui-oos.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libgui_shim.so')
        .replace_needed('android.hidl.base@1.0.so', 'libhidlbase.so'),
}

module = ExtractUtilsModule(
    'sm8450-common',
    'oneplus',
    blob_fixups=blob_fixups,
    check_elf=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()