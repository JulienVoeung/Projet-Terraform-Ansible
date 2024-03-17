import sys
import os

class VM_Manager:
    BASE_DIR:str = os.path.dirname(__file__).removesuffix("src")
    TERRAFORM_SCRIPTS_DIR:str = BASE_DIR + "terraform/"

    TERRAFORM_INIT:str = "terraform -chdir=" + TERRAFORM_SCRIPTS_DIR + " init"

    back_vms_count:int = 0

    def terraform_init(self):
        os.system(self.TERRAFORM_INIT)

    def update_vm_count(self, nb_vm: int):
        os.system("terraform -chdir=" + self.TERRAFORM_SCRIPTS_DIR + " apply -auto-approve -var='nb_back_vms=" + str(nb_vm) + "'" )
        self.back_vms_count = nb_vm
        

if __name__ == '__main__':
    MIN_REQUIRED_PYTHON_VERSION_MAJOR:int = 3
    MIN_REQUIRED_PYTHON_VERSION_MINOR:int = 9

    if (sys.version_info.major < MIN_REQUIRED_PYTHON_VERSION_MAJOR or
            sys.version_info.minor < MIN_REQUIRED_PYTHON_VERSION_MINOR):
        print("Python " + str(MIN_REQUIRED_PYTHON_VERSION_MAJOR) + "." + str(MIN_REQUIRED_PYTHON_VERSION_MINOR) +
                " or higher is required to run this script.")
        exit(1)

    if len(sys.argv) < 2:
        print("You must specify how many vms you want need.")
        exit(1)

    try:
        nb_vms_wanted:int = int(sys.argv[1])

        manager = VM_Manager()
        manager.terraform_init()        
        manager.update_vm_count(nb_vms_wanted)
    except:
        print("An error has occured: ", sys.exc_info()[0])
        raise