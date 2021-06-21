# EatBefore

EatBefore a Enterprise Solution for done by team G10T2.

EatBefore is a web-based application which aims to provide a platform to encourage users to provide reviews on eateries, allowing them to earn some monetary incentives in return through Google Adsense ad revenue based on the amount of views they gain.

## Requirements

- Python 2.0+ or Python 3.0+
- Docker
- Ensure the following port numbers are not occupied (5001, 5002, 5003, 5004, 5005, 5006, 5101, 5102, 5201, 5202, 5203)

### Database Setup
Database selection option
1. Google Cloud SQL
Host: 34.87.173.70
User: is213
Password: totaly2021

2. Local Database

For simulation purpose, a local database can be used

Create Database user:
Username:is213
No Password
Ensure CRUD Privileges are granted

Run the following SQL Files in order before running the application 
1. user.sql
2. review.sql
3. comment.sql
4. transaction.sql
5. log.sql
6. error.sql

In docker-compose.yml, in each Microservice, comment the first line of dbURL and uncomment the second line to enable connection to Local Database connection instead of CloudSQL 

### AWS S3
1. In upload.py [line 38], fill in the aws_access_key_id and aws_secret_access_key created from your personal AWS.
2. In AWS S3, create a bucket named "esd-image". Within that bucket, create a folder named "r/".
3. Under "esd-image" bucket, create a bucket policy and input the following code:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::esd-image/*"
        }
    ]
}


### Payments API

1. PayPal Sandbox Developer Account 
https://www.paypal.com/signin?returnUri=https%3A%2F%2Fdeveloper.paypal.com%2Fdeveloper%2Faccounts%2Fcreate
2. Go to PayPal Sandbox Default Application
3. Under SandBox APP Settings, ensure Payouts checkbox is enabled
4. Get Client ID and Secret Key from PayPal SandBox Default Application
5. Place both Client ID and Secret Key in payment.py by replacing the place holder [Client_ID] and [Client_Secret]


### Bad Words API
1. Sign up with PromptAPI
https://promptapi.com/#signup-form
2. Go to your PromptAPI profile page and copy your API key
3. In review.js [line 17] and makereview.js [line 113], change the API key to your own.


### Notification
1. In notification.py [line 17], add in your email in a string data type (eg. "esd@gmail.com").
2. In notification.py [line 18], add in your password in a string data type (eg. "password").


## Usage
1. Open up command prompt
2. Go to file path /esdg10t2
3. type "docker-compose build" to build solution and install required packages
4. type "docker-compose up -d" to start and run containers 
 
