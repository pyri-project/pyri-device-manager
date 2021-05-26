from pyri.plugins.service_node_launch import ServiceNodeLaunch, PyriServiceNodeLaunchFactory

def _dev_manager_add_args(arg_parser):
    arg_parser.add_argument('--variable-storage-url', type=str, default=None,required=False,help="Robot Raconteur URL for variable storage service")
    arg_parser.add_argument('--variable-storage-identifier', type=str, default=None,required=False,help="Robot Raconteur identifier for variable storage service")
     
def _dev_manager_prepare_args(arg_results):
    args = []
    if arg_results.variable_storage_url is not None:
        args.append(f"--variable-storage-url={arg_results.variable_storage_url}")
    if arg_results.variable_storage_identifier is not None:
        args.append(f"--variable-storage-identifier={arg_results.variable_storage_identifier}")
    return args


launches = [
    ServiceNodeLaunch("device_manager", "pyri.device_manager", "pyri.device_manager", _dev_manager_add_args,_dev_manager_prepare_args,["variable_storage"])
]

class DeviceManagerLaunchFactory(PyriServiceNodeLaunchFactory):
    def get_plugin_name(self):
        return "pyri.device_manager"

    def get_service_node_launch_names(self):
        return ["device_manager"]

    def get_service_node_launches(self):
        return launches

def get_service_node_launch_factory():
    return DeviceManagerLaunchFactory()

        
