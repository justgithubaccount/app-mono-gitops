package main

import (
	"os"

	"cdk.tf/go/stack/generated/timewebcloud/provider"
	"cdk.tf/go/stack/generated/timewebcloud/s3bucket"

	"github.com/hashicorp/terraform-cdk-go/cdktf"
	"github.com/aws/constructs-go/constructs/v10"
)

type MyStackConfig struct {
	cdktf.TerraformStack
}

func NewMyStack(scope constructs.Construct, id string) cdktf.TerraformStack {
	stack := cdktf.NewTerraformStack(scope, &id)

	// Провайдер
	provider.NewTimewebCloudProvider(stack, jsiiString("twc"), &provider.TimewebCloudProviderConfig{
		Token: jsiiString(os.Getenv("TIMEWEB_CLOUD_TOKEN")),
	})

	// Ресурс S3 Bucket
	s3bucket.NewS3Bucket(stack, jsiiString("my_bucket"), &s3bucket.S3BucketConfig{
		Name:      jsiiString("664369f6-cc55-442e-b758-341949a5c073"),
		PresetId:  jsiiNumber(389),
		Type:      jsiiString("private"),
		ProjectId: jsiiNumber(1115913),
	})

	return stack
}

func main() {
	app := cdktf.NewApp(nil)
	NewMyStack(app, "twc-cdk-go")
	app.Synth()
}

// Вспомогательные функции для указателей
func jsiiString(value string) *string {
	return &value
}

func jsiiNumber(value float64) *float64 {
	return &value
}
