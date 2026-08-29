# Get your VM's Managed Identity principal ID
VM_SP_ID=$(az vm show -g MonitoringRG -n MonitorEngineVM --query identity.principalId -o tsv)
SUB_ID=$(az account show --query id -o tsv)

# Grant permission to manage VM power states
az role assignment create \
  --assignee $VM_SP_ID \
  --role "Virtual Machine Contributor" \
  --scope /subscriptions/$SUB_ID/resourceGroups/MonitoringRG