from typing import List, Any, Dict
import RobotRaconteur as RR
from RobotRaconteurCompanion.Util import DateTimeUtil as rr_datetime_util
from RobotRaconteurCompanion.Util import IdentifierUtil as rr_ident_util
import threading

def _get_all_candidate_urls(service_info, node):
    # TODO: Check that url nodeid and nodename match service_info

    try:
        node_info = node.GetDetectedNodeCacheInfo(service_info.NodeID)
    except:
        return service_info.ConnectionURL

    ret = []
    for u in node_info.ConnectionURL:
        u = u.replace("&service=RobotRaconteurServiceIndex","")
        u = u.replace("service=RobotRaconteurServiceIndex&","")
        ret.append(f"{u}&service={service_info.Name}")
    
    return ret
    

def _service_info_to_pyri_device_info(service_info, pyri_device_info_type, ident_util : rr_ident_util.IdentifierUtil, node):

    # TODO: strict type checking of incoming data
    ret = pyri_device_info_type()
    ret.node = ident_util.CreateIdentifier(service_info.NodeName,str(service_info.NodeID))
    ret.service_name = service_info.Name
    ret.urls = _get_all_candidate_urls(service_info,node) # service_info.ConnectionURL
    ret.root_object_type = service_info.RootObjectType
    if service_info.RootObjectImplements is not None:
        ret.root_object_implements = list(service_info.RootObjectImplements)
    if service_info.Attributes is not None:
        a = service_info.Attributes
        if "device" in a:
            ret.device = ident_util.StringToIdentifier(a["device"].data)
        if "parent_device" in a:
            ret.parent_device = ident_util.StringToIdentifier(a["parent_device"].data)
        if "manufacturer" in a:
            try:
                ret.manufacturer = ident_util.StringToIdentifier(a["manufacturer"].data)
            except:
                pass
        if "model" in a:
            try:
                ret.model = ident_util.StringToIdentifier(a["model"].data)
            except:
                pass
        if "serial_number" in a:
            ret.serial_number = a["serial_number"].data
        if "user_description" in a:
            ret.user_description = a["user_description"].data

    return ret



class DeviceManager(object):
    def __init__(self, variable_storage_url, device_info = None, node : RR.RobotRaconteurNode = None):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node
        self.device_info = device_info
        self._pyri_device_info_type = self._node.GetStructureType('tech.pyri.device_manager.PyriDeviceInfo')
        self._device_not_found = self._node.GetExceptionType('tech.pyri.device_manager.DeviceNotFound')
        
        self._datetime_util = rr_datetime_util.DateTimeUtil(self._node)
        self._ident_util = rr_ident_util.IdentifierUtil(self._node)

        filter_ = RR.ServiceSubscriptionFilter()
        filter_.TransportSchemes=["rr+tcp"]
        self._discovery = self._node.SubscribeServiceInfo2('com.robotraconteur.device.Device',filter_)

        self._discovery.ServiceDetected += self._service_detected
        self._discovery.ServiceLost += self._service_lost
        
        self.device_added = RR.EventHook()
        self.device_removed = RR.EventHook()
        self.device_updated = RR.EventHook()
        self.device_detected = RR.EventHook()
        self.device_lost = RR.EventHook()

        self._variable_storage = self._node.SubscribeService(variable_storage_url)
        
    def _service_detected(self, sub,sub_id,service_info2):
        dev_info = _service_info_to_pyri_device_info(service_info2,self._pyri_device_info_type, self._ident_util, self._node)
        if dev_info.device is not None:
            self.device_detected.fire(dev_info.device)

    def _service_lost(self, sub,sub_id,service_info2):
        dev_info = _service_info_to_pyri_device_info(service_info2,self._pyri_device_info_type, self._ident_util, self._node)
        if dev_info.device is not None:
            self.device_lost.fire(dev_info.device)

    def getf_detected_devices(self):
        with self._lock:
            ret_local = []
            ret_other = []
            devices = self._discovery.GetDetectedServiceInfo2()

            local_prefix = ["rr+local", "rr+hardware", "rr+intra"]
            
            for d in devices.values():
                d2 = _service_info_to_pyri_device_info(d,self._pyri_device_info_type, self._ident_util,self._node)
                # Check if device is local by checking if any url has rr+local, rr+hardware, or rr+intra prefix.
                if any(any(u.startswith(p) for p in local_prefix) for u in d2.urls):
                    ret_local.append(d2)
                else:
                    ret_other.append(d2)

            return ret_local + ret_other

    def getf_active_devices(self):
        with self._lock:
            var_storage = self._variable_storage.GetDefaultClient()
            device_var_names = var_storage.filter_variables("device_manager",".*",["active_device"])
            active_devs_vars = []
            #TODO: Type check returned values from variable storage
            for v_name in device_var_names:
                active_devs_vars.append(var_storage.getf_variable_value("device_manager",v_name).data)

            return active_devs_vars

    def getf_detected_device_info(self, device_ident):
        
        devices = self.getf_detected_devices()

        #TODO: More efficient search for device
        for d in devices:
            if self._ident_util.IsIdentifierAny(d.device):
                continue
            if self._ident_util.IsIdentifierMatch(device_ident,d.device):
                return d
        raise self._device_not_found(f"Device {self._ident_util.IdentifierToString(device_ident)} not found")

    def getf_device_info(self, local_device_name):
        with self._lock:             
            var_storage = self._variable_storage.GetDefaultClient()
            device_info = var_storage.getf_variable_value("device_manager",local_device_name).data
            return device_info

    def _add_device_variable(self, device_ident, local_device_name, associated_devices, replace):
        var_storage = self._variable_storage.GetDefaultClient()
        var_consts = self._node.GetConstants('tech.pyri.variable_storage', var_storage)
        variable_persistence = var_consts["VariablePersistence"]
        variable_protection_level = var_consts["VariableProtectionLevel"]
        device_info = self.getf_detected_device_info(device_ident)
        device_info.local_device_name = local_device_name
        device_info.associated_devices = associated_devices or []
        var_storage.add_variable2("device_manager",local_device_name,"tech.pyri.device_manager.PyriDeviceInfo", \
            RR.VarValue(device_info,"tech.pyri.device_manager.PyriDeviceInfo"), ["active_device"], {}, variable_persistence["const"], None, variable_protection_level["read_write"], \
                [], "", replace)

    def add_device(self, device_ident, local_device_name, associated_devices):
        #TODO: check device name format
        #TODO: check if device already added?
        with self._lock:
            self._add_device_variable(device_ident, local_device_name, associated_devices, False)
            self._node.PostToThreadPool(lambda: self.device_added.fire(device_ident, local_device_name))
                        
    def replace_device(self, device_ident, local_device_name, associated_devices):
        with self._lock:
            device_info = self.getf_detected_device_info(device_ident)
            device_info.local_device_name = local_device_name
            device_info.associated_devices = associated_devices or []
            var_storage = self._variable_storage.GetDefaultClient()
            var_storage.setf_variable_value(device_ident, local_device_name, device_info)
            self._node.PostToThreadPool(lambda: self.device_updated.fire(device_ident, local_device_name))

    def remove_device(self, local_device_name):
        with self._lock:
            var_storage = self._variable_storage.GetDefaultClient()
            var_storage.delete_variable("device_manager",local_device_name)
            self._node.PostToThreadPool(lambda: self.device_removed.fire(local_device_name))

    def close(self):
        with self._lock:
            self._discovery.Close()