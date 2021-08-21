<p align="center">
<img src="./doc/figures/pyri_logo_web.svg" height="200"/>
</p>

## PyRI Open Source Teach Pendant Device Manager

This package is part of the PyRI project. See https://github.com/pyri-project/pyri-core#documentation for documentation. This package is included in the `pyri-robotics-superpack` Conda package.

The `pyri-device-manager` package contains the device manager service which detects and manages devices within the overall system.

## Service

This service is started automatically by `pyri-core`, and does not normally need to be started manually.

Standalone service command line example:

```
pyri-device-manager-service
```

The `pyri-variable-storage` service must be running before use. See https://github.com/pyri-project/pyri-variable-storage

Command line options:

| Option | Type | Required | Description |
| ---    | ---  | ---      | ---         |
| `--variable-storage-url=` | Robot Raconteur URL | No | Robot Raconteur URL of variable storage service |
| `--variable-storage-identifier=` | Identifier | No | Robot Raconteur device identifier in string format for variable storage srevice
| `--device-info-file=` | File | No | Robot Raconteur `DeviceInfo` YAML file. Defaults to contents of `pyri_variable_storage_default_info.yml` |

This service may use any standard `--robotraconteur-*` service node options.

The device manager needs to connect to the variable storage service. This can be done using discovery based on a Robot Raconteur device identifier, or using a specified Robot Raconteur URL. If neither is specified, the device manager will search for the identifier named `pyri_variable_storage` on the local machine.

This service adds the `-variable-storage-url=` and `-variable-storage-identifier=` options to `pyri-core`.

## Acknowledgment

This work was supported in part by Subaward No. ARM-TEC-19-01-F-24 from the Advanced Robotics for Manufacturing ("ARM") Institute under Agreement Number W911NF-17-3-0004 sponsored by the Office of the Secretary of Defense. ARM Project Management was provided by Christopher Adams. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of either ARM or the Office of the Secretary of Defense of the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for Government purposes, notwithstanding any copyright notation herein.

This work was supported in part by the New York State Empire State Development Division of Science, Technology and Innovation (NYSTAR) under contract C160142. 

![](doc/figures/arm_logo.jpg) ![](doc/figures/nys_logo.jpg)

PyRI is developed by Rensselaer Polytechnic Institute, Wason Technology, LLC, and contributors.