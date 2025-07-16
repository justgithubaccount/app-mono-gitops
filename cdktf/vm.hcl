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

resource "twc_floating_ip" "intelligent-ganymede-floating-ip" {
	availability_zone = "fra-1"
	ddos_guard = false
}

resource "twc_server" "intelligent-ganymede" {
	name = "Intelligent Ganymede"
	project_id = 1115913
	os_id = 95
	availability_zone = "fra-1"
	is_root_password_required = true
	ssh_keys_ids = [undefined]
	cloud_init = "#cloud-config
hostname: client

package_update: true
package_upgrade: true

packages:
  - docker.io

runcmd:
  - echo "Client node initialized" > /var/log/init.log"
	floating_ip_id = twc_floating_ip.intelligent-ganymede-floating-ip.id

	configuration {
		configurator_id = 79
		disk = 40960
		cpu = 2
		ram = 2048
		gpu = 0
	}

	local_network {
		id = "network-b85636efcaaa436a97d0a13371e28870"
	}
}

resource "twc_server_disk_backup_schedule" "intelligent-ganymede-auto-backup" {
	source_server_id = twc_server.intelligent-ganymede.id
	source_server_disk_id = twc_server.intelligent-ganymede.disks[0].id
	copy_count = 1
	creation_start_at = "2025-07-16T00:00:00.000Z"
	interval = "day"
}
