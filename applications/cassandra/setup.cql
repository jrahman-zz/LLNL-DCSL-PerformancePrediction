create keyspace usertable with placment_strategy = 'SimplyStrategy' and strategy_options = {replication_factor:1};
use usertable;
create column family data
