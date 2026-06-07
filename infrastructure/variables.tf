variable "tenancy_ocid" {
  type        = string
  description = "OCI Tenancy OCID"
}

variable "user_ocid" {
  type        = string
  description = "OCI User OCID"
}

variable "fingerprint" {
  type        = string
  description = "API Key fingerprint"
}

variable "private_key_path" {
  type        = string
  description = "Path to local private API Key"
}

variable "compartment_ocid" {
  type        = string
  description = "OCI Compartment OCID where resources will be provisioned"
}

variable "region" {
  type        = string
  default     = "us-ashburn-1"
  description = "OCI Region"
}

variable "ssh_public_key" {
  type        = string
  description = "Public SSH key for node login"
}

variable "instance_shape" {
  type        = string
  default     = "VM.Standard.A1.Flex" # Always Free Ampere ARM
  description = "The shape of the compute instance"
}

variable "instance_ocpus" {
  type        = number
  default     = 2
  description = "Number of OCPUs for VM.Standard.A1.Flex"
}

variable "instance_memory_in_gbs" {
  type        = number
  default     = 12
  description = "Memory in GB for VM.Standard.A1.Flex"
}

variable "boot_volume_size_in_gbs" {
  type        = number
  default     = 50
  description = "Size of boot volume in GB (Always Free allows up to 200GB total)"
}
