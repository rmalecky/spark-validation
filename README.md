# Validating data with AWS Glue
This repo shows how to validate json data using AWS Glue and jsonschema.

## Prerequisites
- AWS Account with Admin Access
- Pre-create the AWSGlueServiceRole (https://docs.aws.amazon.com/glue/latest/dg/create-an-iam-role.html)
- Local Dev Environment
  - Python 2.7
  - AWS Credentials

## Sample data
Generate Sample data by running the following script locally.  Python 2.7 needs to be installed.

https://faker.readthedocs.io/en/latest/index.html

``` bash
# install the faker package
pip install faker

# create sample files
python data.py 1000 > small.jsonl
python data.py 1000000 > million.jsonl
```

## Create jsonschema deployment package
Run the following commands to create a zipped copy of the jsonschema package.  Use Python 2.7



```bash

mkdir jsonschema
pip install -t ./jsonschema jsonschema
cd jsonschema/
zip -r ../jsonschema.zip *
cd ..
rm -rf jsonschema
```

## Upload Files to S3
replace `<ENTER_S3BUCKET>` with the S3 Bucket for this demo.

```bash
aws s3 mb s3://<ENTER_S3BUCKET>
aws s3 cp small.jsonl s3://<ENTER_S3BUCKET>/
aws s3 cp million.jsonl s3://<ENTER_S3BUCKET>/
aws s3 cp schema.json s3://<ENTER_S3BUCKET>/
aws s3 cp jsonschema.zip s3://<ENTER_S3BUCKET>/
aws s3 cp validate.py s3://<ENTER_S3BUCKET>/
```

## Create and run the validation job
Output and job status can be monitored via the Glue console.
```bash
aws glue create-job --name validation \
  --role AWSGlueServiceRole \
  --command Name=glueetl,ScriptLocation=s3://<ENTER_S3BUCKET>/validate.py \
  --allocated-capacity 2 \
  --default-arguments '{
    "--s3bucket": "<ENTER_S3BUCKET>",
    "--datafile": "million.jsonl",
    "--numpartitions": "8", "--extra-py-files":
    "s3://<ENTER_S3BUCKET>/jsonschema.zip",
    "--job-language": "python",
    "--job-bookmark-option": "job-bookmark-disable"
  }'


aws glue start-job-run --job-name validation
```



## References
- https://github.com/aws-samples/aws-glue-samples/tree/master/examples
- https://faker.readthedocs.io/en/latest/index.html
- https://python-jsonschema.readthedocs.io/en/latest/
- https://docs.aws.amazon.com/cli/latest/reference/glue/index.html#cli-aws-glue
- http://spark.apache.org/docs/2.2.1/api/python/pyspark.html
- https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming.html


