from typing import List
from RobotRaconteurCompanion.Util import RobDef as robdef_util
from pyri.plugins.robdef import PyriRobDefPluginFactory

class DeviceManagerRobDefPluginFactory(PyriRobDefPluginFactory):
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return "pyri-variable-storage"

    def get_robdef_names(self) -> List[str]:
        return ["tech.pyri.device_manager"]

    def  get_robdefs(self) -> List[str]:
        return get_device_manager_robdef()

def get_robdef_factory():
    return DeviceManagerRobDefPluginFactory()

def get_device_manager_robdef():
    return robdef_util.get_service_types_from_resources(__package__,["tech.pyri.device_manager"])