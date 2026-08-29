import os
import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "<YOUR_SUBSCRIPTION_ID>")
RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP", "MonitoringRG")

def shutdown_idle_vms():
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

    # List all VMs in the target resource group
    vms = compute_client.virtual_machines.list(RESOURCE_GROUP)

    for vm in vms:
        # Check instance view for power state
        instance_view = compute_client.virtual_machines.instance_view(RESOURCE_GROUP, vm.name)
        statuses = [s.display_status for s in instance_view.statuses]

        if "VM running" in statuses:
            logging.info(f"Target VM '{vm.name}' is currently running. Initiating deallocation...")
            
            # Stop and deallocate the VM to save compute costs
            async_deallocate = compute_client.virtual_machines.begin_deallocate(RESOURCE_GROUP, vm.name)
            async_deallocate.wait()
            
            logging.info(f"Successfully stopped and deallocated VM: {vm.name}")
        else:
            logging.info(f"VM '{vm.name}' is already stopped.")

if __name__ == "__main__":
    shutdown_idle_vms()