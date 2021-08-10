import sys
import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
from .device_manager import DeviceManager
import argparse
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from pyri.plugins import robdef as robdef_plugins
from pyri.util.service_setup import PyriServiceNodeSetup

def main():
    parser = argparse.ArgumentParser(description="PyRI Variable Storage Service Node")
    parser.add_argument('--variable-storage-url', type=str, default=None,required=False,help="Robot Raconteur URL for variable storage service")
    parser.add_argument('--variable-storage-identifier', type=str, default=None,required=False,help="Robot Raconteur identifier for variable storage service")
        
    with PyriServiceNodeSetup("tech.pyri.device_manager",59902,register_plugin_robdef=True,\
        default_info = (__package__,"pyri_device_manager_default_info.yml"), \
        arg_parser = parser, no_device_manager=True,
        distribution_name="pyri-device-manager") as service_node_setup:
        
        RRN.ThreadPoolCount = 100

        dev_manager = DeviceManager(service_node_setup.argparse_results.variable_storage_url, \
            service_node_setup.argparse_results.variable_storage_identifier, \
            device_info=service_node_setup.device_info_struct, node = RRN) 

        service_node_setup.register_service("device_manager","tech.pyri.device_manager.DeviceManager",dev_manager)
        
        service_node_setup.wait_exit()

        dev_manager.close()

if __name__ == "__main__":
    sys.exit(main() or 0)
