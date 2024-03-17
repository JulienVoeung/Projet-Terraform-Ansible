import requests
import time
import os
from vms_manager import VM_Manager

def _list_average(lst): 
    return sum(lst) / len(lst) 

class VM_Listener:
    BASE_DIR:str = os.path.dirname(__file__).removesuffix("src")
    PLAYBOOKS_DIR:str = BASE_DIR + "playbooks/"

    _vm_manager = VM_Manager()
    _last_50_active_conns_nb:list[int] = []
    _nb_back_vms:int = 1
    _load_balancer_ip = ""

    def __init__(self, base_nb_vms:int, load_balancer_ip:str) -> None:
        self._nb_back_vms = base_nb_vms
        self._load_balancer_ip = load_balancer_ip

    def _append_active_connections_info(self):
        time.sleep(1)
        request = requests.get("http://" + self._load_balancer_ip + "/nginx_status")
        try:
            if len(self._last_50_active_conns_nb) > 50:
                self._last_50_active_conns_nb.pop(0)
                self._last_50_active_conns_nb.append(int(str(request.content).split("server")[0]
                    .replace("b'Active connections:", "")
                    .replace("\\n", "")))
            else:
                self._last_50_active_conns_nb.append(int(str(request.content).split("server")[0]
                    .replace("b'Active connections:", "")
                    .replace("\\n", "")))
        except:
            pass

    def listen(self):
        self._append_active_connections_info()
        while len(self._last_50_active_conns_nb) < 10:
            self._append_active_connections_info()

        counter:int = 0
        while True:
            self._append_active_connections_info()
            counter += 1
            if counter == 10:
                counter = 0      
                old_nb_vms = self._nb_back_vms  
                average_active_conns = _list_average(self._last_50_active_conns_nb)

                # Adjust scaling levels here based on average active connections
                if average_active_conns < 20:
                    self._nb_back_vms = 1
                elif average_active_conns < 60:
                    self._nb_back_vms = 2
                else:
                    self._nb_back_vms = 3 
                
                if old_nb_vms != self._nb_back_vms:
                    self._vm_manager.update_vm_count(self._nb_back_vms)
                    os.system("cd " + self.PLAYBOOKS_DIR + " && ansible-playbook update-front-config.yml")
