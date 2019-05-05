# Data Warehouses

The following is a summary of the Chapter 2 Introduction to Data Warehouses of Udacity's Data Engineering Nanodegree. You'll go into Data Warehouses understading **the need of a Data Warehouse** from a Business and Technical Perspective as well as which are **the most common Data Warehouse Architectures**.

## What Is A Data Warehouse from Business Perspective?

Imagine you are in charge of a retailer’s data infrastructure. Let’s look at some business activities.

- Customers should be able to find goods & make orders
- Inventory Staff should be able to stock, retrieve, and re-order goods
- Delivery Staff should be able to pick up & deliver goods
- HR should be able to assess the performance of sales staff
- Marketing should be able to see the effect of different sales channels
- Management should be able to monitor sales growth

Ask yourself: **Can I build a database to support these activities? Are all of the above questions of the same nature?** 

Let's take a closer look at details that may affect your data infrastructure. 

- Retailer has a nation-wide presence → Are you going to do one database for all of them or are you going to do a database for each store or headquarter? → You need scalability
- Acquired smaller retailers, brick & mortar shops, online store → You have complexity 
- Has support call center & social media accounts → You need Tabular data and availability to aggregate data
- Customers, Inventory Staff and Delivery staff expect the system to be fast & stable → You need Performance
- HR, Marketing & Sales Reports want a lot information but have not decided yet on everything they need → Do you have clear requirements? Your data needs could change over time

### Operational and Analytics Data Source

From a business perspective, a business is a set of business processes. We can divide these processes between operational processes and analytics processes. 
- Operational processes: are all those which try to make it work. 
- Analytics processes: are all those which try to understand what is happening.
And together both care about how to improve business.

![Operational vs Analytical](img/operations_vs_analytics.PNG)

What if we use the same data source for both purposes? We built data sources to warehouse all operational information and then we use these source to analyse the data.

We'll probably get a source which is excellent for operations, with integrity and no redundancy, but with slow performance and hard to understand and analyse.

![Operational vs Analytical](img/operations_and_analytics_source.PNG)

The general solution is the data warehouse, transforming operational data sources to other sources optimized for our purposes. The data warehouse is the system (processes, technologies and data representations) that enables to support analytical processes. 

![Operational vs Analytical](img/Data_Warehouse_Solution.PNG)


## What is a Data Warehouse from a Technical Perspective?

See different definitions:

*"A data warehouse is a copy of transaction data specifically structured for query and analysis" - Kinball*

Focus on **copy** (we are not going on the same data) and we are going to desing a structure in a way to be **optimal for analysis**.

*"A data warehouse is a subject-oriented, integrated, nonvolatile and time-variant collection of data in support of management's decisions." - Inmon*

- Motivated by taking management decisions and insights, 
- **Subject-oriented** means the there is no one-size-fits-all or it is going to support different subject areas.
- **Integrated** because the data come from many sources.
- **Nonvolatile** in the sense that it's not transient and has to be persistent.
- **Time-variant** means I will ask same question today and tomorrow and is going to change because data is going to be inserted or updated.

*"A data warehouse is a system that **retrieves and consolidates data periodically** from the source systems into a dimensional or normalized data store. It usually keeps years of history and is querie for business intelligence or other analytical activities. It is **typically updated in batches**, not every time a transaction happens in the source system."*

### Data Warehouse Goals

- Simple to understand
- Performand
- Quality Assured
- Handles new questions well
- Secure

## Data Warehouse Arquitectures

Over the recent years, Data Engineers has designed different architectures for Data Warehousing. The following are the most famous ones:

- Kimball's **Bus Arquitecture**
- Independent **Data Marts**
- Inmon's **Corporate Information Factory (CIF)**
- **Hybrid** Bus & CIF


### Bus Architecture

According to Kimball's Bus Architecture, data is kept in a **common dimension data model**, organized by business process and shared across different departments. It does not allow for individual department specific data modeling requirements. 

![Kimball](img/kimball.PNG)

In the Kimball architecture, the sales analytics and the delivery analytics will both use the same data dimension.

## Independent Data Marts

The idea of independent data marts is that each department have their own separate and smaller dimensional models, having different fact tables for the same events (no conformed dimensions). Thus, independent Data Marts have ETL processes that are designed by specific business departments to meet their analytical needs.

![Data Marts](img/data_marts.PNG)

However, the main problem is that can lead to unconsistent views, and despite awareness of the emergence of this architecture from departamental auonomy, it is generally discouraged.

## Corporate Information Factory (CIF)

![CIF](img/cif.PNG)

Corporate Information Factory (CIF) is build on a 3NF normalized database and then allow for documented data denormalization for Data Marts.  The aim is to provide the flexibility of data marts, make the original and normalized data also available as well as preventing from the unconsistencies. 

From Data adquisition, a cleaned and normalized Enterprise Data Warehouse is built. The Enterprise Data Warehouse provides a normalized data (3NF) architecture before individual departments build on it. The Data Marts use 3NF model and add denormalization based on department needs. 

Then, BI or analytical application can access not only data marts, but also enterprise data warehouse, being both departamental and original data available to analytic modules.

### Hybrid Bus & CIF

Combining CIF's Enterprise Data Warehouse with Bus Arquitecture (instead of Data Marts) we get an hybrid architecture, having a normalized DWH as well as conformed dimensions.

![hybrid_bus_cif](img/hybrid_bus_cif.PNG)
