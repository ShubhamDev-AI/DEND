
# Hands on AWS

## Amazon Redshift 

![Redshift_Cluster](img/AWS_Building_Redshift_Cluster.PNG)

![IAM SG](img/AWS_IAM_Security_Group.JPG)  
  
  
### Create an IAM role
 
An AWS IAM (Identity and Access Management) is a framework for business processes that facilitates the management of electronic or digital identities. 

IAM roles are a secure way to grant permissions to trusted entities. 

Examples of entities include the following:

- IAM user in another account
- The application code that runs on an EC2 instance and that needs to perform actions on AWS resources. For example, an ETL that access S3 to get data to load into a Redshift.
- AWS service that must act on the account's resources to provide its features
- Users of a corporate directory that use the federated identity with SAML
- IAM roles emit valid keys for short periods, which makes them a more secure form of access.
 
For any operation that accesses data on another AWS resource, your cluster needs permission to access the resource and the data on the resource on your behalf. You provide those permissions by using AWS Identity and Access Management (IAM).
 
To create an IAM Role follow the [steps in AWS tutorial](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-create-an-iam-role.html).

1. Sign in to the AWS Management Console and open the IAM console at https://console.aws.amazon.com/iam/
2. In the left navigation pane, choose Roles.
3. Choose Create role.
4. In the AWS Service group, choose Redshift.
5. Under Select your use case, choose Redshift - Customizable, and then Next: Permissions.
6. On the Attach permissions policies page, choose AmazonS3ReadOnlyAccess, and then choose Next: Tags.
7. Skip this page and choose Next: Review.
8. For Role name, enter myRedshiftRole, and then choose Create Role.

More information about IAM roles in [AWS FAQS](https://aws.amazon.com/iam/faqs/)

### Create a Security Group

A security group acts as a virtual firewall that **controls the traffic** for one or more instances. When you launch an instance, you can specify one or more security groups; otherwise, we use the default security group. You can add rules to each security group that allow traffic to or from its associated instances. You can modify the rules for a security group at any time; the new rules are automatically applied to all instances that are associated with the security group. When we decide whether to allow traffic to reach an instance, we evaluate all the rules from all the security groups that are associated with the instance.

For example, imagine we want to connect a Jupyter notebook to an Amazon Redshift. We want to access from "outside" and so we need to open a TCP port of Redshift to do others able to connect with the database. A Security Group 

In order to create a Security Group:

1. Go to your Amazon EC2 console and under Network and Security in the left navigation pane, select Security Groups.
2. Choose the Create Security Group button.
3. Enter redshift_security_group for Security group name.
4. Enter "authorize redshift cluster access" for Description.
5. Select the Inbound tab under Security group rules.
6. Click on Add Rule and enter the following values:
- Type: Custom TCP Rule.
- Protocol: TCP.
- Port Range: 5439. The default port for Amazon Redshift is 5439, but your port might be different. See note on determining your firewall rules on the first page.
- Source: select Custom IP, then type 0.0.0.0/0.
**Important**: Using 0.0.0.0/0 is not recommended for anything other than demonstration purposes because it allows access from any computer on the internet. In a real environment, you would create inbound rules based on your own network settings.
7. Choose Create.

### Launch a Redshift Cluster

Before launch an AWS Redshift Cluster 

 The cluster that you are about to launch will be live, and you will be charged the standard Amazon Redshift usage fees for the cluster until you delete it. **Make sure to delete your cluster each time you're finished working to avoid large, unexpected costs**. Instructions on deleting your cluster are included on the last page. You can always launch a new cluster, so don't leave your Redshift cluster running overnight or throughout the week if you don't need to.  
 
 1. Sign in to the AWS Management Console and open the Amazon Redshift console at https://console.aws.amazon.com/redshift/
 2. On the Amazon Redshift Dashboard, choose Launch cluster.
 3. On the Cluster details page, enter the following values and then choose Continue:
    - Cluster identifier: Enter redshift-cluster.
    - Database name: Enter dev.
    - Database port: Enter 5439.
    - Master user name: Enter awsuser.
    - Master user password and Confirm password: Enter a password for the master user account.
 4. On the Node Configuration page, accept the default values and choose Continue.
 5. On the Additional Configuration page, enter the following values:
- VPC security groups: redshift_security_group
- Available IAM roles: myRedshiftRole  
    Choose Continue.  
 6. Review your Cluster configuration and choose Launch cluster.  

In order to **delete your cluster**:

1. On the Clusters page of your Amazon Redshift console, click on the box next to your cluster to select it, and then click on **Cluster > Delete cluster.**
2. You can choose **No for Create snapshot**, check the box that you acknowledge this, and then choose Delete.
3. Your cluster will change it's status to deleting, and then disappear from your Cluster list once it's finished deleting. You'll no longer be charged for this cluster.

### Create an IAM user

Here, you'll create an IAM user that you will use to access your Redshift cluster from Airflow.

1. Sign in to the AWS Management Console and open the IAM console at https://console.aws.amazon.com/iam/.
2. In the left navigation pane, choose Users.
3. Choose Add User.
4. Enter a name for your user (e.g. airflow_redshift_user)
5. Choose Programmatic access, then choose Next: Permissions.
6. Choose Attach existing policies directly.
7. Search for redshift and select AmazonRedshiftFullAccess. Then, search for S3 and select AmazonS3ReadOnlyAccess. After selecting both policies, choose Next: Tags.
8. Skip this page and choose Next: Review.
9. Review your choices and choose Create user.
10. Save your credentials! This is the only time you can view or download these credentials on AWS. Choose Download .csv to download these credentials and then save this file to a safe location. You'll need to copy and paste this Access key ID and Secret access key in the next step.

### Create and delete an S3 Bucket

**Create an S3 Bucket**

1. Go to the Amazon S3 Console and select Create bucket.
2. Enter a name for your bucket and select the region you'd like to create it in.
3. You won't be able to use the same name entered in the screenshot below - the names of all existing buckets on Amazon S3 are unique. You won't be able to change this name later, so choose one that makes sense for the content you'll have in it. This bucket name will be included in any URLs pointing to objects you add in your bucket.
4. Keep the default settings and select Next.
5. Specify public access settings for this bucket. For example, unchecking all of these boxes would allow anyone to be able to access this bucket. Be careful with this - you may end up having to pay lots of fees in data transfers from your bucket if you share this link and many people access large amounts of data with it. For this demo, we will leave all of these boxes checked.
6. Review your settings and select Create bucket.
7. You should now see your bucket in your list. Any buckets you've made public will be labeled so here.

**Delete S3 Bucket**

To delete the bucket, select the bucket and click Delete. Then, enter the name of the bucket and select Confirm.


### Upload to S3 Bucket  

1. Click on the bucket you just created and select Upload on the top left.
2. Select Add files and choose a file you want to store.
3. Leave the default settings and select Next.
4. Choose the Standard storage class and select Next.
5. Review your settings and select Upload.
6. You should be able to see details on the file you just uploaded by selecting it in your bucket.

### Create a PostgreSQL DB Instance using RDS

1. Go to the Amazon RDS console and click on Databases on the left navigation pane. Choose what region you'd like to create this database in on the right of the top menu bar.
2. Click on the Create Database button.
3. Select PostgreSQL on the Select Engine page.
4. Since this is for demonstration purposes, select Dev/Test under Use case.
5. Next, is a long Specify DB details page. You can leave the default values (shown below) for most of these settings. Just make the following choices:
- For DB instance class, select db.t2.small
- For DB instance identifier, enter postgreSQL-test or another name of your choice
- Enter a master username and password
- Leave the default values for the next few sections.
- In the Backup section and select 1 day since this is for demonstration purposes.
- Leave the default values for the rest and click on - Create database on the bottom right.
- You should land on a confirmation page.
6. Click Databases on the left navigation pane to return to your list of databases. You should see your newly created database with the status Creating.
7. Wait a few minutes for this to change to the status Available.

## IaC: Infrastructure as a Code

Infrastucture as a Code (IaC) is the ability to create infrastructure, i.e. machines, users, roles, folders and processes using code.

It is an important technique in modern data engineers, being border-line dataEng/devOps.

IaC has several advantages, which mainly are the following:

- **Sharing**: One can share all the steps with others easily
- **Reproducibility**: One can be sure that no steps are forgotten
- **Multiple deployments**: One can create a test environment identical to the production environment
- **Maintainability**: If a change is needed, one can keep track of the changes by comparing the code

We have a number of option to achieve IaC on AWS:
- **aws-cli scripts**: similar to bash scripts, simple & convenient
- **AWS sdk**: available in lots programming languags (python, java, ruby, c++, node.js, and more)
- Amazon Cloud Formation

