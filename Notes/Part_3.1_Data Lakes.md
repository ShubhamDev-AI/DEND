# Data Lakes

There are many other big data tools and systems, each with its own use case. 

## Review of the hardware behind big data 

Big Data is referred to all the process that work with huge amounts of data. Generally, we start to talk about Big Data when instead of working in a single machine, we need to work with a distributed system of a cluster of computers. 

To understand when we deal with Big Data tools, we need to know the modern hardware capabilities in terms of CPU, RAM Memory, SSD and Network. 

- **CPU (Central Processing Unit)**: The CPU is the "brain" of the computer. Every process on your computer is eventually handled by your CPU. This includes calculations and also instructions for the other components of the compute. It is 200x faster than memory.

- **Memory (RAM)** When your program runs, data gets temporarily stored in memory before getting sent to the CPU. Memory is ephemeral storage - when your computer shuts down, the data in the memory is lost. It is 15x faster than SSD. However, is expensive.

- **Storage (SSD or Magnetic Disk)** Storage is used for keeping data over long periods of time. When a program runs, the CPU will direct the memory to temporarily load data from long-term storage. It is 20x faster thn network.

- **Network (LAN or the Internet)**: Network is the gateway for anything that you need that isn't stored on your computer. The network could connect to other computers in the same room (a Local Area Network) or to a computer on the other side of the world, connected over the internet. Transferring data across a networdk is the biggest bottleneck when working with big data (one of the avantages of Spark is that it only shuffles data between computers when it absolutely hast to).

You may have noticed a few other numbers involving the L1 and L2 Cache, mutex locking, and branch mispredicts. 

Here the numbers:
- [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832)
- [Timeline Evolution of Latency Numbers Every Programmer Should Know](http://people.eecs.berkeley.edu/~rcs/research/interactive_latency.html)


## Introduction to distributed systems  

### Parallel vs Distributed

In general, parallel computing implies multiple CPUs that share the same memory. With distributed computing, each CPU has its own memory. In distributed computing, ech computer/machine is connected to the other machines across network.

### Hadoop Ecosystem

- HDFS: Hadoop Data Storage. Big dat storage system that splits data into chunks and stores the chunks across a cluster of computers.
- MapReduce: Hadoop Data Processing
- YARN: Hadoop Resource Manager
- Hadoop Common: Utilities

Complementary tools for data analysis:
- Apache Pig: SQL-like language that runs on top of Hadoop MapReduce
- Apache Hive: another SQL-like interfice that runs on top of Hadoop MapReduce.

Complementary tools for streaming applications:
- Apache Storm: streaming library. Million tuples processed per second per node. 
- Apache Flink: streaming library 

#### MapReduce

MapReduce is a programming technique for manipulate large data sets. Hadoop MapReduce is a specific implementation of this programming technique.

The Technique works by diving up a large dataset into many chunks and distributing the data across a cluster. In map step, each data is analyzed and converted into a key-value pair. Then these key-value pair are shuffled across the cluster so that all keys are on the same machine. In the reduce sep, the values with the same keys are combined together.

While Spark doesn't implement MapReduce, you can write Spark programs that bhave in a similar way to the map-reduce paradigm. 

### Spark Ecosystem

Spark contains libraries for data analysis, machine learning, graph analysis and streaming live data.

Spark is generally faster than Hadoop. The major difference between Spark and Hadoop is how they use memory. Hadoop writes intermediate results to disk whereas Spark tries to keep data in memory whenever possible. This makes Spark faster for many use cases. 

Spark does not include a file storage system like Hadoop ecosystem does with HDFS. You can use Spark on top of HDFS but you do not have to. Saprl can read in data from other sources as well such as Amazon S3.

#### Spark Modes

- Local Mode: when you are working with Spark installed on your laptop. Using this mode we won't take any advantage of Spark, but it could be useful to explore data and write code.
- Standalone
- YARN
- Mesos

#### Common Spark use cases  

- Data analysis
- Machine Learning
- Streaming
- Graph Analysis

#### Spark's Limitations

Spark Streaming's latency is at least 500ms since it operates on microbathes of records intead of processing one record at a time. Native streaming tools such as Storm, Apex or Flink can push down this latency value and might be more suitable for low latency applications.  

#### Spark Advantages

Spark is faster than Hadoop, since Hadoop is a bit older. However, while Spark is great for interactive algorithms, there is not much of a performance boost over Haddop MapReduce when doing a simple counting. Migrating legacy code to Spark, especially on hundreds of nodes that are already in production, might not be worth the cost for the small performance boost.

