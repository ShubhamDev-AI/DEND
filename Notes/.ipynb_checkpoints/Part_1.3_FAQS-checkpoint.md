
# 3. FAQS

**Why can't everything be stored in a giant Excel spreadsheet?**

-	Limitations on amount of data.
-	Data Integrity (Duplication of data).
-	Disability of crossing tables (joins)
-	Scalability. Also reading and writing operations on a large scale (often crashes when doing computing expensive operations and you lose everything).
-	Permissions (everyone can modify or write over a spreadsheet)
-	Multiple User Access (one person can be connected at the same time)

**How is data modeling different from machine learning modeling?**

There are two different meanings for data modelling:
-	Data Engineering meaning: Data modelling in terms of architecture, i.e., how to structure data to be used by different people within an organization. It is the process of designing data and making it available to end-users (machine learning engineers, data scientists, business analytics)
-	Data Scientist meaning: Data modelling means how to build a function that could represent the behavior of real data, often used to predict future behaviors, reproduce patterns or understand correlations of data. It is typically known as statistical modelling or machine learning modelling.


**What type of companies use Apache Cassandra?**

All kinds of companies. For example, Uber uses Apache Cassandra for their entire backend. Netflix uses Apache Cassandra to serve all their videos to customers. NoSQL (and more specifically Apache Cassandra) are good use cases for:
-	Transaction logging (retail, health care)
-	IOT
-	Time series data
-	Any workload that is heavy on writes to the database (since Apache Cassandra is optimized for writes).
Would Apache Cassandra be a hindrance for my analytics work? If yes, why?
Yes, if you are trying to do analysis, such as GROUP BY statements, then yes. Since Apache Cassandra requires data modeling based on the query you want, you can't do ad-hoc queries. However you can add clustering columns into your data model and create new tables.


**Is Eventual Consistency the opposite of what is promised by SQL database per ACID principle?**
Much has been written about how Consistency is interpreted in the ACID principle and the CAP theorem. Consistency in the ACID principle refers to the requirement that only transactions that abide by constraints and database rules are written into the database, otherwise the database keeps previous state. In other words, the data should be correct across all rows and tables. However, consistency in the CAP theorem refers to every read from the database getting the latest piece of data or an error. 
To learn more, here are some links you may find useful:


**Which of this combination is desirable Consistency and Availability, Consistency and Partition, or Availability and Partition for a production system?**
There is no such thing as Consistency and Partition, you can only have Consistency and Availability or Availability and Partition. Remember, relational and non-relational databases do different things, and that's why most companies have both types of database systems.

**Does Cassandra meet just Availability and Partition in the CAP theorem?**
According to CAP theorem, a database can actually only guarantee two out of the three in CAP. So supporting Availability and Partition makes sense, since Availability and Partition are the biggest requirements.

**If Apache Cassandra is not built for consistency, won't the analytics pipeline break?**
If I am trying to do analysis, such as getting a trend overtime, e.g., how many friends does John have on Twitter, and if you have one less person counted because of "eventual consistency" (the data may not be up-to-date in all locations), that's OK. In theory, that can be an issue but only if you are not constantly updating. If the pipeline pulls data from one node and it has not been updated, then you won't get it. Remember, it is about Apache Cassandra about Eventual Consistency.

**What does the network look like? Can you share any examples?**
In Apache Cassandra every node is connected to every node -- it's peer to peer database architecture.

**Is data deployment strategy an important element of data modeling in Apache Cassandra?**
Deployment strategies are a great topic, but have very little to do with data modeling. Developing deployment strategies focuses on determining how many clusters to create or determining how many nodes are needed. These are topics generally covered under database architecture, database deployment and operations, which we will not cover in this lesson. Here is a useful link to learn more about it for Apache Cassandra.

In general, the size of your data and your data model can affect your deployment strategies. You need to think about how to create a cluster, how many nodes should be in that cluster, how to do the actual installation. More information about deployment strategies can be found on this DataStax documentation page.
