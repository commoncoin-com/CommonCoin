# Virtual Cloud Network (VCN)
resource "oci_core_vcn" "commoncoin_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "commoncoin_vcn"
  dns_label      = "ccvcn"
}

# Internet Gateway
resource "oci_core_internet_gateway" "commoncoin_ig" {
  compartment_id = var.compartment_ocid
  display_name   = "commoncoin_ig"
  vcn_id         = oci_core_vcn.commoncoin_vcn.id
}

# Route Table
resource "oci_core_route_table" "commoncoin_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.commoncoin_vcn.id
  display_name   = "commoncoin_rt"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.commoncoin_ig.id
  }
}

# Security List
resource "oci_core_security_list" "commoncoin_sl" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.commoncoin_vcn.id
  display_name   = "commoncoin_security_list"

  # Outbound rules
  egress_security_rules {
    destination      = "0.0.0.0/0"
    protocol         = "all"
    destination_type = "CIDR_BLOCK"
  }

  # Inbound rules
  # SSH
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    tcp_options {
      min = 22
      max = 22
    }
  }

  # P2P Node Port
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    tcp_options {
      min = 33555
      max = 33555
    }
  }

  # RPC Port (Restrict access within VCN by default)
  ingress_security_rules {
    protocol    = "6" # TCP
    source      = "10.0.0.0/16"
    source_type = "CIDR_BLOCK"
    tcp_options {
      min = 33556
      max = 33556
    }
  }
}

# Subnet
resource "oci_core_subnet" "commoncoin_subnet" {
  cidr_block        = "10.0.1.0/24"
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.commoncoin_vcn.id
  route_table_id    = oci_core_route_table.commoncoin_rt.id
  security_list_ids = [oci_core_security_list.commoncoin_sl.id]
  display_name      = "commoncoin_subnet"
  dns_label         = "ccsubnet"
}

# Get Availability Domain
data "oci_identity_availability_domains" "ad" {
  compartment_id = var.compartment_ocid
}

# Query standard Ubuntu 22.04 image matching our shape
data "oci_core_images" "ubuntu" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "22.04"
  shape                    = var.instance_shape
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

# Compute Instance
resource "oci_core_instance" "commoncoin_node" {
  availability_domain = data.oci_identity_availability_domains.ad.availability_domains[0].name
  compartment_id      = var.compartment_ocid
  display_name        = "commoncoin-seed-node"
  shape               = var.instance_shape

  dynamic "shape_config" {
    for_each = var.instance_shape == "VM.Standard.A1.Flex" ? [1] : []
    content {
      ocpus         = var.instance_ocpus
      memory_in_gbs = var.instance_memory_in_gbs
    }
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.commoncoin_subnet.id
    display_name     = "commoncoin_vnic"
    assign_public_ip = true
  }

  source_details {
    source_type             = "image"
    source_id               = data.oci_core_images.ubuntu.images[0].id
    boot_volume_size_in_gbs = var.boot_volume_size_in_gbs
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data           = base64encode(file("${path.module}/cloud-init.yaml"))
  }

  preserve_boot_volume = false
}
