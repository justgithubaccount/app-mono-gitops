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

resource "twc_s3_bucket" "664369f6-cc55-442e-b758-341949a5c073-bucket" {
	name = "664369f6-cc55-442e-b758-341949a5c073"
	preset_id = 389
	type = "private"
	project_id = 1115913
}
