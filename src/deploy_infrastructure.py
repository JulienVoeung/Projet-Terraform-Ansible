import subprocess
import ipaddress
import sys
import os
import time
from vms_listener import VM_Listener

if __name__ == '__main__':
  MIN_REQUIRED_PYTHON_VERSION_MAJOR:int = 3
  MIN_REQUIRED_PYTHON_VERSION_MINOR:int = 9

  if (sys.version_info.major < MIN_REQUIRED_PYTHON_VERSION_MAJOR or
        sys.version_info.minor < MIN_REQUIRED_PYTHON_VERSION_MINOR):
    print("Python " + str(MIN_REQUIRED_PYTHON_VERSION_MAJOR) + "." + str(MIN_REQUIRED_PYTHON_VERSION_MINOR) +
          " or higher is required to run this script.")
    exit(1)

  BASE_DIR:str = os.path.dirname(__file__).removesuffix("src")
  SRC_DIR:str = BASE_DIR + "src/"
  TEMPLATES_DIR:str = BASE_DIR + "templates/"
  PLAYBOOKS_DIR:str = BASE_DIR + "playbooks/"
  OUTPUT_DIR:str = BASE_DIR + "output/"

  if len(sys.argv) < 2:
    print("You need to specify how many VMs you need (min 1, max 3).")
    print("Usage: python deploy-infrastructure.py <nb_of_vms_needed>")
    exit(1)

  try:
    nb_vms:int = int(sys.argv[1])
    if nb_vms < 1 or nb_vms > 3:
      raise
  except:
    print("Enter a valid number (min 1, max 3) !")
    raise

  if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

  proc = subprocess.Popen([sys.executable, SRC_DIR + 'vms_manager.py', str(nb_vms)], stdout=subprocess.PIPE)
  output_lines:list[str] = []
  output_detected = False

  while True:
    line = proc.stdout.readline().decode("utf-8")
    if "Outputs:" in line:
      output_detected = True
    if output_detected:
      output_lines.append(line.strip().replace(',', '').replace('"', ''))
    if line != "":
      print (line.rstrip())
    else:
      break

  internal_ips:list[str] = []
  public_ip = output_lines[-2].split('=')[1].strip().replace('"', '')

  for line in output_lines:
    try:
      ipaddress.ip_address(line)
      internal_ips.append(line)
    except:
      pass

  with open(TEMPLATES_DIR + 'loadbalancer.conf.template', 'r') as file:
    lb_template_lines = file.readlines()

  for ip in internal_ips:
    lb_template_lines.insert(1, "\tserver " + str(ip) + ";\n")

  with open(OUTPUT_DIR + 'loadbalancer.conf', 'w') as file:
    file.writelines( lb_template_lines )

  with open(OUTPUT_DIR + 'hosts', 'w') as file:
    file.write("[serveursweb]\n")
    for ip in internal_ips:
      file.write(str(ip) + "\n")

  with open('/etc/ansible/hosts', 'w') as file:
    file.write("[serveursweb]\n")
    file.write(str(public_ip) + "\n")

  # Wait 10 seconds to give enough time to VM to finish boot up
  print("Waiting 10 seconds for VM(s) to be ready ...")
  time.sleep(10)

  os.system("cd " + PLAYBOOKS_DIR + " && ansible-playbook front-config.yml")

  print("Now listening to server activity to update VMs count when needed ...")
  VM_Listener(nb_vms, public_ip).listen()