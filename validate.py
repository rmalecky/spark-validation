import boto3
import json
import jsonschema
import sys

from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions


args = getResolvedOptions(sys.argv,
                          ['s3bucket',
                           'datafile',
                           'numpartitions'])

S3BUCKET = args["s3bucket"]
datafile = "s3://" + S3BUCKET + "/" + args["datafile"]
numParts = int(args["numpartitions"])



# create the spark context

sc = SparkContext.getOrCreate()


# Read in the schema from S3

s3 = boto3.resource('s3')
schema = json.loads(s3.Bucket(S3BUCKET).Object('schema.json').get()['Body'].read())

# Create the validation function

def validate(row, schema):
    datum = json.loads(row)
    validator = jsonschema.Draft4Validator(schema)
    errors = [e.message for e in validator.iter_errors(datum)]
    if not errors:
        return None
    return json.dumps({"data": datum, "errors": errors})



# Read the data in from S3 and repartition it.
# Each partition is operated on in parallel.

data = sc.textFile(datafile).repartition(numParts)

numRows = data.count()

# Count the distinct rows in the data set.
numDistRows = data.distinct().count()

# Apply the validate function to each row
errors = data.map(lambda x: validate(x, schema))

# remove rows without errors
numErrors = errors.filter(lambda x: x is not None).count()

print "number of rows: {0}".format(numRows)
print "number of duplicate rows: {0}".format(numRows - numDistRows)
print "number of invalid rows: {0}".format(numErrors)




