# Zenskar Assignment

## 📚 | Problem Statement

- This project focuses on implementing a bidirectional sync between the customer data on my product and that on a Stripe account. This system allows for real-time updates and consistency between my product and Stripe.
- The integration involves two main components: **outward sync** and **inward sync**.
- **Outward Sync** - The process of syncing data from this system to Stripe.
- **Inward Sync** - The process of syncing data from Stripe to this system.

## 🧮 | Plans

- [Salesforce Integration](./plans/salesforce_integration.md)
- [In-house Integration](./plans/in_house_integration.md)

## 🚧 | Deployment

There are many components to this system. Namely, a Postgres Database hosted on EC2, a Stripe account, a FastAPI app, Docker desktop, ngrok for exposing local server, and setting up the .env file.

### 1. Postgres Database

- We will be using Postgres as our database.
- Create an EC2 instance on AWS and setup Postgres on it.
- This is a great medium article to use as [reference](https://medium.com/@akhilsharma_10270/the-right-way-to-install-postgresql-on-aws-ec2-ubuntu-22-04-c77e72bfb8ef) for setting up Postgres on EC2.

### 2. Stripe Account

- Create a Stripe (test) account and get the API keys.
- Now create a webhook endpoint on Stripe and point it to some random URL. We will change this URL later.
- Add the following events to the webhook:

```bash
- customer.created
- customer.updated
- customer.deleted
```

### 3. FastAPI App

- We will be using FastAPI to create the web-server.
- Clone the repository and navigate to the root directory.
- Create a .env file and fill it with the following details:

```bash
  - STRIPE_SECRET_KEY
  - PSQL_USER
  - PSQL_PASSWORD
  - PSQL_HOST
  - PSQL_PORT
  - PSQL_DB
  - HOST_IP
```

- For HOST_IP, type the following command in your terminal:

```bash
- Windows: ipconfig
- Linux: ifconfig
```

- Get the ipv4 address and paste it in the .env file for HOST_IP.

### 4. Docker Desktop

- We need docker to run the app and its dependencies, in a containerized environment.
- Ensure you have docker desktop installed on your system.
- Edit KAFKA_ADVERTISED_LISTENERS key with your HOST_IP.
- Run the following command to build and run the docker images:

```bash
docker compose up --build
```

- The app should be running on port 8000, and the rest of the dependencies on their respective ports.
- In addition to that, run the following command in the root directory to start the consumer:

```bash
python run_consumer.py
```

### 5. Ngrok Setup

- We need ngrok to expose our FastAPI app to the internet.
- Create an account on ngrok and download the ngrok client.
- Use the auth-token command Ngrok provides to authenticate your account.
- Run the downloaded ngrok executable file to start the ngrok client.
- Run the following command to expose the local server:

```bash
ngrok.exe http <HOST_IP>:8000

[example]
ngrok.exe http 192.168.1.2:8000
```

- Now copy the forwarding URL and change the webhook endpoint on Stripe to this URL.

## 🚀 | API Endpoints

- _**GET**_ /users - Get all users
- _**GET**_ /users/{id} - Get user by id
- _**POST**_ /users - Create a new user
- _**PUT**_ /users/{id} - Update user by id
- _**DELETE**_ /users/{id} - Delete user by id
- **POST** /users/sync - Stripe webhook endpoint

  <br/>

## 👨‍💻 | Author

**Kaustav Mukhopadhyay**

- Linkedin: [@kaustavmukhopadhyay](https://www.linkedin.com/in/kaustavmukhopadhyay/)
- Github: [@muKaustav](https://github.com/muKaustav)

<br/>

## 📝 | License

Copyright © 2023 [Kaustav Mukhopadhyay](https://github.com/muKaustav).<br />
This project is [MIT](./LICENSE) licensed.
<br/>
<br/>

---
