
import os

### Set Environment bucket location for RW acess 
ENV_BUCKET="s3a://demo-aws-2/datalake/"

try : 
  DL_s3bucket=os.environ["STORAGE"]+"/datalake/"
except KeyError: 
  DL_s3bucket=ENV_BUCKET


#### HDFS Paths for Files #####
flights_path='airlines/flights/' 
airport_path='airlines/airports/' 
carrier_path='airlines/carriers/'
file_prefix='file:////home/cdsw/'

#### Start Spark Session ####

print("Start Spark session :")
from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession\
  .builder\
  .appName('wine-quality-analysis')\
  .config("spark.executor.memory","2g")\
  .config("spark.executor.cores","1")\
  .config("spark.executor.instances","3")\
  .config("spark.yarn.access.hadoopFileSystems",DL_s3bucket )\
  .getOrCreate()

        
# ### Create flights database
database = 'flights'

print("Create airlines Database")

try: 
  spark.sql('''create database if not exists flights''')
except:
  database = 'default'


# ### save Flights table 
# read table
print("save flights data")

flights_df = spark.read.csv(
    path=file_prefix+flights_path,
    header=True,
    sep=',',
    inferSchema=True,
    nullValue='NA'
).cache()
flights_df.printSchema()

# save in Hive
flights_df.orderBy(['Month','DayofMonth']).coalesce(4)\
    .write.format('parquet').mode("overwrite")\
    .saveAsTable(database+'.flights_raw')

print("Flights table saved")  
    
# ### save airports table 
# read table
print("save airport data")

airports_df = spark.read.csv(
    path=file_prefix+airport_path,
    header=True,
    sep=',',
    inferSchema=True,
    nullValue=None
).cache()
airports_df.printSchema()

# save in Hive
airports_df.orderBy(['state','airport']).coalesce(2)\
    .write.format('parquet').mode("overwrite")\
    .saveAsTable(database+'.airports')
    
print("airports table saved")  
   

# ### save carriers table 
# read table
print("save carriers data")

carriers_df = spark.read.csv(
    path=file_prefix+carrier_path,
    header=True,
    sep=',',
    inferSchema=True,
    nullValue=None
).cache()
carriers_df.printSchema()

# save in Hive
carriers_df.orderBy(['Code']).coalesce(2)\
    .write.format('parquet').mode("overwrite")\
    .saveAsTable(database+'.carriers')
    
print("carriers table saved")  

# ### Show databases
spark.sql("show tables in " + database).show()


spark.stop()