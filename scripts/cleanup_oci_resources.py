import oci
import sys
import os
import time

TFVARS_PATH = r"E:\commoncoin\infrastructure\terraform.tfvars"

def load_tfvars(path):
    variables = {}
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                variables[k] = v
    return variables

def main():
    print("Loading variables from terraform.tfvars...", flush=True)
    tfvars = load_tfvars(TFVARS_PATH)
    
    config = {
        "user": tfvars.get("user_ocid"),
        "key_file": tfvars.get("private_key_path"),
        "fingerprint": tfvars.get("fingerprint"),
        "tenancy": tfvars.get("tenancy_ocid"),
        "region": tfvars.get("region")
    }
    
    compartment_id = tfvars.get("compartment_ocid")
    if not compartment_id:
        compartment_id = config["tenancy"]
        
    print(f"Initializing clients for region {config['region']}...", flush=True)
    compute_client = oci.core.ComputeClient(config)
    network_client = oci.core.VirtualNetworkClient(config)
    lb_client = oci.load_balancer.LoadBalancerClient(config)
    
    # 1. Terminate compute instances
    print("Listing Compute Instances to terminate...", flush=True)
    try:
        instances = compute_client.list_instances(compartment_id=compartment_id).data
    except Exception as e:
        print(f"Error listing instances: {e}")
        instances = []
        
    active_instances = [inst for inst in instances if inst.lifecycle_state not in ("TERMINATED", "TERMINATING")]
    if not active_instances:
        print("No active Compute instances found.")
    else:
        print(f"Found {len(active_instances)} active Compute instances. Terminating them...")
        for inst in active_instances:
            print(f"Terminating instance: {inst.display_name} ({inst.id})...")
            try:
                compute_client.terminate_instance(instance_id=inst.id)
            except Exception as e:
                print(f"Error terminating instance {inst.display_name}: {e}")
                
        # Wait for instances to terminate
        print("Waiting for instances to terminate...", flush=True)
        while True:
            try:
                instances = compute_client.list_instances(compartment_id=compartment_id).data
            except Exception:
                break
            active_instances = [inst for inst in instances if inst.lifecycle_state not in ("TERMINATED", "TERMINATING")]
            if not active_instances:
                print("All Compute instances terminated.")
                break
            print(f"Still waiting for {len(active_instances)} instances to terminate...")
            time.sleep(10)
            
    # 2. Terminate Networking (VCNs, subnets, gateways)
    print("\nListing VCNs to terminate...", flush=True)
    try:
        vcns = network_client.list_vcns(compartment_id=compartment_id).data
    except Exception as e:
        print(f"Error listing VCNs: {e}")
        vcns = []
        
    active_vcns = [vcn for vcn in vcns if vcn.lifecycle_state not in ("TERMINATED", "TERMINATING")]
    if not active_vcns:
        print("No active VCNs found.")
    else:
        for vcn in active_vcns:
            print(f"Cleaning VCN: {vcn.display_name} ({vcn.id})...")
            
            # Subnets
            try:
                subnets = network_client.list_subnets(compartment_id=compartment_id, vcn_id=vcn.id).data
                active_subnets = [sub for sub in subnets if sub.lifecycle_state not in ("TERMINATED", "TERMINATING")]
                for sub in active_subnets:
                    print(f"  Deleting Subnet: {sub.display_name} ({sub.id})...")
                    try:
                        network_client.delete_subnet(subnet_id=sub.id)
                    except Exception as e:
                        print(f"    Error deleting subnet: {e}")
            except Exception as e:
                print(f"  Error checking subnets: {e}")
                
            # Wait for subnets to delete
            print("  Waiting for subnets to delete...", flush=True)
            time.sleep(5)
            
            # Internet Gateways
            try:
                igs = network_client.list_internet_gateways(compartment_id=compartment_id, vcn_id=vcn.id).data
                active_igs = [ig for ig in igs if ig.lifecycle_state not in ("TERMINATED", "TERMINATING")]
                for ig in active_igs:
                    print(f"  Deleting Internet Gateway: {ig.display_name} ({ig.id})...")
                    try:
                        network_client.delete_internet_gateway(ig_id=ig.id)
                    except Exception as e:
                        print(f"    Error deleting gateway: {e}")
            except Exception as e:
                print(f"  Error checking gateways: {e}")
                
            # Delete VCN
            print(f"  Deleting VCN: {vcn.display_name}...")
            try:
                network_client.delete_vcn(vcn_id=vcn.id)
                print(f"  VCN {vcn.display_name} deleted successfully.")
            except Exception as e:
                print(f"    Error deleting VCN: {e}")
                
    print("\nOCI Cleanup Process Complete.", flush=True)

if __name__ == "__main__":
    main()
