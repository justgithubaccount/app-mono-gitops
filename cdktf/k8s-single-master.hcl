terraform {
    required_providers {
        twc = {
            source = "tf.timeweb.cloud/timeweb-cloud/timeweb-cloud"
        }
    }
    required_version = ">= 0.13"
}

provider "twc" {
    token = "TIMEWEB_CLOUD_TOKEN"
}

resource "twc_k8s_cluster" "charming-lacerta-cluster" {
	name = "Charming Lacerta"
	project_id = 1115913
	network_id = "network-b85636efcaaa436a97d0a13371e28870"
	network_driver = "calico"
	ingress = false
	preset_id = 1955
	version = "v1.33.2+k0s.0"
	description = ""
}

resource "twc_k8s_node_group" "brainy-halimede-node-group" {
	cluster_id = twc_k8s_cluster.charming-lacerta-cluster.id
	name = "Brainy Halimede"
	preset_id = 1969
	node_count = 2
	is_autoscaling = false
}
