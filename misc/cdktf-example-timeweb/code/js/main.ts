import { Construct } from 'constructs';
import { App, TerraformStack } from 'cdktf';
import { TimewebCloudProvider, S3Bucket } from './.gen/providers/timeweb-cloud';

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new TimewebCloudProvider(this, 'twc', {
      token: process.env.TIMEWEB_CLOUD_TOKEN!, // Лучше использовать env-переменную
    });

    new S3Bucket(this, 'bucket', {
      name: '664369f6-cc55-442e-b758-341949a5c073',
      presetId: 389,
      type: 'private',
      projectId: 1115913,
    });
  }
}

const app = new App();
new MyStack(app, 'twc-cdk');
app.synth();
