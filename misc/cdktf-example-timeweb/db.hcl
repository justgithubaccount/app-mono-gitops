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

resource "twc_vpc" "polite-hoopoe-vpc" {
	name = "Polite Hoopoe VPC"
	subnet_v4 = "192.168.0.0/24"
	location = "ru-3"
}

resource "twc_database_cluster" "polite-hoopoe" {
	name = "Polite Hoopoe"
	type = "postgres17"
	hash_type = "caching_sha2"
	replications = 1
	project_id = 1115913
	preset_id = 1139
	availability_zone = "msk-1"

	network {
		id = twc_vpc.polite-hoopoe-vpc.id
	}
}
