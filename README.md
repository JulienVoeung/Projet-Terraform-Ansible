1. You must install ansible(package-manager), <a href="https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli" target="_blank">terraform</a>, <a href="https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt" target="_blank">azure-cli</a> and python3.9 (python3.9 or above via package-manager)
2. Install python requirements
- `pip install -r ./src/requirements.txt`
3. Run `az login` to log in to your azure account
4. Edit /etc/ansible/ansible.cfg and uncomment the line => host_key_checking = False
5. Add new group and change permission of /etc/ansible folder and files: (needed because the python script needs to edit /etc/ansible/hosts)
- `sudo addgroup ansible-adm`
- `sudo adduser $USER ansible-adm`
- `sudo chown -R :ansible-adm /etc/ansible`
- `sudo chmod 775 /etc/ansible`
- `sudo chmod 664 /etc/ansible/*`
6. Restart your terminal to apply your new user group
7. Run (with pyhton 3.9 or above) the script
- `python3.9 ./src/deploy-infrastructure.py <nb_of_vms_you_need>`