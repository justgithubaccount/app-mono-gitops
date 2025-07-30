from constructs import Construct
from cdktf import App, TerraformStack, TerraformVariable
from imports.timeweb_cloud import TimewebCloudProvider, S3Bucket

import os

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Провайдер Timeweb Cloud
        TimewebCloudProvider(self, "twc", token=os.getenv("TIMEWEB_CLOUD_TOKEN"))

        # Создание S3-бакета
        S3Bucket(self, "my_bucket",
            name="664369f6-cc55-442e-b758-341949a5c073",
            preset_id=389,
            type="private",
            project_id=1115913
        )

app = App()
MyStack(app, "twc-cdk-python")
app.synth()
