output "node_public_ip" {
  value       = oci_core_instance.commoncoin_node.public_ip
  description = "Public IP address of the CommonCoin node"
}

output "node_state" {
  value       = oci_core_instance.commoncoin_node.state
  description = "Current state of the CommonCoin compute instance"
}
