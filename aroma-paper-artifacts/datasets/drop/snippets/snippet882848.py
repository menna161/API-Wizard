from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import explode, concat_ws, udf, concat, col, lit, when
import config
import cassandra
from datetime import datetime
from dateutil.relativedelta import relativedelta


def main():
    '\n\tMain function\n\n\tMain function that joins the bitcoin and dark web data\n\n\t'
    appName = 'DarkCoinJoin'
    master = config.spark['MASTERIP']
    spark = SparkSession.builder.appName(appName).config('spark.cassandra.connection.host', config.cassandra['HOSTS']).config('spark.cassandra.connection.port', config.cassandra['PORT']).config('spark.cassandra.output.consistency.level', 'ONE').config('spark.kryoserializer.buffer.max', '2047m').config('spark.driver.port', config.cassandra['DRIVERPORT']).config('spark.network.timeout', '10000000').master(master).getOrCreate()
    sqlContext = SQLContext(spark)
    df_bitcoin = spark.read.format('org.apache.spark.sql.cassandra').options(table=config.cassandra['BITCOIN'], keyspace=config.cassandra['KEYSPACE']).load()
    df_bitcoin.registerTempTable('bitcoin')
    df_marketplace = spark.read.format('org.apache.spark.sql.cassandra').options(table=config.cassandra['MARKETPLACE'], keyspace=config.cassandra['KEYSPACE']).load()
    df_marketplace.registerTempTable('marketplace')
    substring = udf((lambda x: x[0:510]), StringType())
    substring2 = udf((lambda x: x[0:99]), StringType())
    df_marketplace = df_marketplace.withColumn('description', substring('description')).withColumn('ship_to', substring2('ship_to')).withColumn('ship_from', substring2('ship_from')).withColumn('category', substring2('category')).withColumn('image_url', substring('image_url')).withColumn('product_name', substring('product_name'))
    date_incr = udf((lambda date, num_days: (date + relativedelta(days=num_days))), TimestampType())
    result = df_bitcoin.join(df_marketplace, (((df_bitcoin.recv_amount == df_marketplace.price) & (df_bitcoin.time > df_marketplace.ad_date)) & (df_bitcoin.time < date_incr(df_marketplace.ad_date, lit(10)))), 'inner').drop(df_bitcoin.recv_amount)
    write_postgres(result)
