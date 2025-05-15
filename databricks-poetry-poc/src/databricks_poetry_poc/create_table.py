import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, DateType

def read_json_mapping(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def map_spark_type(data_type):
    """Map JSON type to Spark data type"""
    mapping = {
        "INT": IntegerType(),
        "STRING": StringType(),
        "FLOAT": FloatType(),
        "DATE": DateType()
    }
    return mapping.get(data_type.upper(), StringType())  # default to STRING

def create_table_from_mapping(mapping):
    spark = SparkSession.builder \
        .appName("DatabricksPoetryPoC") \
        .config("spark.sql.catalogImplementation", "in-memory") \
        .getOrCreate()

    table_name = mapping["tableName"]
    columns = mapping["columns"]

    # Create schema from mapping
    schema = StructType([
        StructField(col["name"], map_spark_type(col["type"]), True)
        for col in columns
    ])

    # Create empty DataFrame
    df = spark.createDataFrame([], schema)

    # Save as table
    df.write.saveAsTable(table_name)

    print(f"✅ Table `{table_name}` created successfully (in memory)!")


if __name__ == "__main__":
    mapping = read_json_mapping("mappings/table_mapping.json")
    create_table_from_mapping(mapping)