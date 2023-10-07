# Salesforce Integration

## 📚 | Problem Statement

- Create a plan for adding a second integration with Salesforce's customer catalog to your product's customer catalog.

## 🧮 | Plans

### 1. Defining the Integration

- We decide on the design and architecture of the integration.
- The design refers to the data flow between the two systems. Thus, we need to define the schemas such that minimal changes are required to the existing system.
- We create a new package for the Salesforce integration, such that it is independent of the Stripe integration.

### 2. Creating the Integration

- We install the necessary libraries to interact with Salesforce. One such library is the simple-salesforce library, it gives us APIs to access salesforce data.
- We obtain the Salesforce credentials and add them to the .env file.
- We define how customer data from our product will be mapped to the Salesforce customer data.
- We create new APIs to handle the Salesforce integration.
- Using these APIs, we implement the outward sync and inward sync, similar to the Stripe integration.

### 3. Extending the Kafka Consumer

- We extend the Kafka consumer to handle the Salesforce integration.
- We create a new topic for Salesforce events and add it to the consumer.
- We add salesforce_util.py and the corresponding logic for implementing the outward sync and inward sync.
- Robust error handling is implemented to ensure that the system is fault-tolerant.
- Exhaustive logging and monitoring is implemented to ensure that the system is observable, and events can be differentiated.
- The queue should now support both Stripe and Salesforce events.

### 4. Testing the Integration

- We test the integration by:

  - creating a new customer on our product and checking if the customer is created on Salesforce.
  - creating a new customer on Salesforce and checking if the customer is created on our product.
  - updating a customer on our product and checking if the customer is updated on Salesforce.
  - updating a customer on Salesforce and checking if the customer is updated on our product.
  - deleting a customer on our product and checking if the customer is deleted on Salesforce.
  - deleting a customer on Salesforce and checking if the customer is deleted on our product.

- We also test if this integration works in tandem with the Stripe integration.

### 5. Additional Steps

- We add proper documentation for the integration.
- We plan the deployment/scaling of the entire system
  <br/>
  <br/>

---
