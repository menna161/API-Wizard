import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pytz import FixedOffset, timezone, utc
from random import randint
from enum import Enum
from sqlalchemy import create_engine, DateTime
from datetime import datetime

if (__name__ == '__main__'):
    start_date = datetime.now().replace(microsecond=0, second=0, minute=0)
    (customer_entities, driver_entities, end_date, orders_df, start_date) = generate_entities(start_date, 1000, 1000, 20000)
    customer_df = create_customer_daily_profile_df(customer_entities, start_date, end_date)
    print(customer_df.head())
    drivers_df = create_driver_hourly_stats_df(driver_entities, start_date, end_date)
    print(drivers_df.head())
    orders_table = 'orders'
    driver_hourly_table = 'driver_hourly'
    customer_profile_table = 'customer_profile'
    print('uploading orders')
    save_df_to_csv(orders_df, orders_table, dtype={'event_timestamp': DateTime()})
    print('uploading drivers')
    save_df_to_csv(drivers_df, driver_hourly_table, dtype={'datetime': DateTime()})
    print('uploading customers')
    save_df_to_csv(customer_df, customer_profile_table, dtype={'datetime': DateTime()})
