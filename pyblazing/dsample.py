import time
import pprint
from blazingsql import BlazingContext
from dask.distributed import Client
client = Client('127.0.0.1:8786')
client.restart()
bc = BlazingContext(dask_client=client, network_interface="lo")

# bc = BlazingContext()

dir_data_fs = '/home/aocsa/tpch/100MB2Part/tpch'
nfiles = 4

# bc.create_table('customer', [dir_data_fs + '/customer_0_0.parquet', dir_data_fs + '/customer_1_0.parquet', dir_data_fs + '/customer_2_0.parquet'])

bc.create_table('part', dir_data_fs + '/part_*.parquet')

# "BindableTableScan(table=[[main, customer]], 
# filters=[[OR(AND(<($0, 15000), =($1, 5)), =($0, *($1, $1)), >=($1, 10), <=($2, 500))]], 
# projects=[[0, 3, 5]], aliases=[[c_custkey, c_nationkey, c_acctbal]])"
# query = """select c_custkey, c_nationkey, c_acctbal
#             from 
#               customer
#             where 
#               c_custkey > 2990 and c_custkey < 3010 
#             """

query = "select count(p_partkey), sum(p_partkey), max(p_partkey), min(p_partkey) from part where p_partkey < 100"

# [b'c_custkey', b'c_name', b'c_address', b'c_nationkey', b'c_phone', b'c_acctbal', b'c_mktsegment', b'c_comment']
lp = bc.explain(query)
print(lp)
ddf = bc.sql(query)
print(query)
# print(ddf)
print(ddf.compute())