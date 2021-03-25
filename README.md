# PyRI Open Source Teach Pendant Device Manager

The device manager detects and manages devices within the overall system.

## Setup

The `pyri-device-manager` package should be installed into a virtual environment using the command:

```
python3 -m pip install -e .
```

See https://github.com/pyri-project/pyri-core for more information on setting up the virtual environment.

# Startup

The `pyri-variable-storage` service must be running before use. See https://github.com/pyri-project/pyri-variable-storage

To start the service, run:

```
pyri-device-manager-service --device-info-file=config/pyri_device_manager_default_info.yml --variable-storage-url=rr+tcp://localhost:59901?service=variable_storage --robotraconteur-tcp-ipv4-discovery=true
```