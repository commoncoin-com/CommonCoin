# Deploying CommonCoin (COM) to Oracle Cloud (OCI)

This guide documents the automated provisioning and deployment of a public CommonCoin node on Oracle Cloud Always Free compute VMs using Terraform and cloud-init.

---

## 1. OCI API Key & Account Setup

To deploy resources with Terraform, you must generate an API key and obtain the necessary OCIDs from the OCI Console.

1. **Generate API Signing Key**:
   In your terminal, run:
   ```bash
   mkdir -p ~/.oci
   openssl genrsa -out ~/.oci/oci_api_key.pem 2048
   chmod 600 ~/.oci/oci_api_key.pem
   openssl rsa -pubout -in ~/.oci/oci_api_key.pem -out ~/.oci/oci_api_key_public.pem
   ```

2. **Add Public Key to OCI Console**:
   * Navigate to **User Settings** -> **API Keys** -> **Add API Key**.
   * Upload `~/.oci/oci_api_key_public.pem`.
   * Copy the configuration values (user OCID, tenancy OCID, fingerprint, region).

3. **SSH Login Key**:
   Ensure you have a public SSH key at `~/.ssh/id_rsa.pub` to configure compute login.

---

## 2. Configure Terraform Variables

Navigate to the `infrastructure/` directory:

```bash
cd infrastructure/
```

Create a file named `terraform.tfvars` and populate it with your OCI account details:

```hcl
tenancy_ocid     = "ocid1.tenancy.oc1..xxxxxx"
user_ocid        = "ocid1.user.oc1..xxxxxx"
fingerprint      = "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx"
private_key_path = "~/.oci/oci_api_key.pem"
compartment_ocid = "ocid1.compartment.oc1..xxxxxx"
region           = "us-ashburn-1"
ssh_public_key   = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQD..."
```

---

## 3. Deploy the Node

1. **Initialize Terraform**:
   Downloads the required OCI providers.
   ```bash
   terraform init
   ```

2. **Generate Execution Plan**:
   Review what resources will be created.
   ```bash
   terraform plan
   ```

3. **Apply Plan**:
   Provision the virtual cloud network and compute instance.
   ```bash
   terraform apply
   ```
   *Type `yes` when prompted.*

Once completed, Terraform will display the public IP address of the newly spawned node:
```bash
node_public_ip = "129.146.x.x"
```

---

## 4. Track Build Progress on the VM

Log in to the VM using SSH:

```bash
ssh ubuntu@<node_public_ip>
```

The `cloud-init` script is running in the background to install dependencies and build CommonCoin. You can track the progress in real-time by inspecting the log:

```bash
tail -f /var/log/cloud-init-output.log
```

Once the build is complete, check that the daemon is active and running under systemd:

```bash
systemctl status commoncoind
```

Run RPC queries to verify details:

```bash
commoncoin-cli getnetworkinfo
commoncoin-cli getblockchaininfo
```

---

## 5. Security & Firewall Rules

The security list configured in `main.tf` automatically opens:
* **Port 22/TCP**: SSH Administration.
* **Port 33555/TCP**: P2P Peer Sync (must be open publicly for node communication).
* **Port 33556/TCP**: JSON-RPC Interface (restricted to localhost and internal VCN IP subnet `10.0.0.0/16` for security).
