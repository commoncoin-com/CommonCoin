import oci
import sys
import os

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
    
    # Construct OCI config
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
        
    print(f"Connecting to OCI region: {config['region']}...", flush=True)
    try:
        oci.config.validate_config(config)
    except Exception as e:
        print(f"OCI Config validation failed: {e}")
        sys.exit(1)
        
    print(f"Inspecting compartment: {compartment_id}...\n", flush=True)
    
    # 1. Compute Instances
    compute_client = oci.core.ComputeClient(config)
    print("Checking Compute Instances...", flush=True)
    instances = []
    try:
        instances = compute_client.list_instances(compartment_id=compartment_id).data
    except Exception as e:
        print(f"Error checking Compute Instances: {e}")
        
    active_instances = [inst for inst in instances if inst.lifecycle_state not in ("TERMINATED", "TERMINATING")]
    print(f"Found {len(active_instances)} active Compute instances.")
    for inst in active_instances:
        print(f"  - VM: {inst.display_name} (State: {inst.lifecycle_state}, OCID: {inst.id})")
        
    # 2. Block Volumes
    block_client = oci.core.BlockstorageClient(config)
    print("\nChecking Block and Boot Volumes...", flush=True)
    volumes = []
    boot_volumes = []
    try:
        volumes = block_client.list_volumes(compartment_id=compartment_id).data
        boot_volumes = block_client.list_boot_volumes(availability_domain=None, compartment_id=compartment_id).data
    except Exception as e:
        # If availability_domain is required, we get ADs first
        try:
            identity_client = oci.identity.IdentityClient(config)
            ads = identity_client.list_availability_domains(compartment_id=compartment_id).data
            for ad in ads:
                boot_volumes.extend(block_client.list_boot_volumes(availability_domain=ad.name, compartment_id=compartment_id).data)
        except Exception as ex:
            print(f"Error checking Boot Volumes: {ex}")
            
    active_volumes = [vol for vol in volumes if vol.lifecycle_state not in ("TERMINATED", "TERMINATING")]
    active_boot_volumes = [bvol for bvol in boot_volumes if bvol.lifecycle_state not in ("TERMINATED", "TERMINATING")]
    
    print(f"Found {len(active_volumes)} active block volumes.")
    for vol in active_volumes:
        print(f"  - Block Volume: {vol.display_name} (Size: {vol.size_in_gbs} GB, State: {vol.lifecycle_state}, OCID: {vol.id})")
        
    print(f"Found {len(active_boot_volumes)} active boot volumes.")
    for bvol in active_boot_volumes:
        print(f"  - Boot Volume: {bvol.display_name} (Size: {bvol.size_in_gbs} GB, State: {bvol.lifecycle_state}, OCID: {bvol.id})")
        
    # 3. Virtual Cloud Networks (VCNs)
    network_client = oci.core.VirtualNetworkClient(config)
    print("\nChecking Networking Resources...", flush=True)
    vcns = []
    try:
        vcns = network_client.list_vcns(compartment_id=compartment_id).data
    except Exception as e:
        print(f"Error checking VCNs: {e}")
        
    active_vcns = [vcn for vcn in vcns if vcn.lifecycle_state not in ("TERMINATED", "TERMINATING")]
    print(f"Found {len(active_vcns)} active VCNs.")
    for vcn in active_vcns:
        print(f"  - VCN: {vcn.display_name} (CIDR: {vcn.cidr_block}, State: {vcn.lifecycle_state}, OCID: {vcn.id})")
        
        # Subnets in this VCN
        try:
            subnets = network_client.list_subnets(compartment_id=compartment_id, vcn_id=vcn.id).data
            active_subnets = [sub for sub in subnets if sub.lifecycle_state not in ("TERMINATED", "TERMINATING")]
            print(f"    - Subnets ({len(active_subnets)}):")
            for sub in active_subnets:
                print(f"      * Subnet: {sub.display_name} (CIDR: {sub.cidr_block}, OCID: {sub.id})")
        except Exception as e:
            print(f"      * Error listing subnets: {e}")
            
        # Internet Gateways
        try:
            igs = network_client.list_internet_gateways(compartment_id=compartment_id, vcn_id=vcn.id).data
            active_igs = [ig for ig in igs if ig.lifecycle_state not in ("TERMINATED", "TERMINATING")]
            print(f"    - Internet Gateways ({len(active_igs)}):")
            for ig in active_igs:
                print(f"      * Gateway: {ig.display_name} (OCID: {ig.id})")
        except Exception as e:
            print(f"      * Error listing internet gateways: {e}")
            
        # Security Lists
        try:
            sls = network_client.list_security_lists(compartment_id=compartment_id, vcn_id=vcn.id).data
            # Security list state is usually not TERMINATED as it's part of VCN lifecycle
            print(f"    - Security Lists ({len(sls)}):")
            for sl in sls:
                print(f"      * Security List: {sl.display_name} (OCID: {sl.id})")
        except Exception as e:
            print(f"      * Error listing security lists: {e}")

    # 4. Load Balancers
    lb_client = oci.load_balancer.LoadBalancerClient(config)
    print("\nChecking Load Balancers...", flush=True)
    lbs = []
    try:
        lbs = lb_client.list_load_balancers(compartment_id=compartment_id).data
    except Exception as e:
        print(f"Error checking Load Balancers: {e}")
        
    active_lbs = [lb for lb in lbs if lb.lifecycle_state not in ("DELETED", "DELETING")]
    print(f"Found {len(active_lbs)} active Load Balancers.")
    for lb in active_lbs:
        print(f"  - Load Balancer: {lb.display_name} (State: {lb.lifecycle_state}, OCID: {lb.id})")
        
    print("\nOCI Inspection Complete.", flush=True)

if __name__ == "__main__":
    main()
