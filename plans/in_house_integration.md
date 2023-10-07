# Integration with in-house systems

## 📚 | Problem Statement

How can the above integrations with your product's customer catalog be extended to support other systems within your product? For example - the invoice catalog.

## 🚀 | Advantages

- I understand that an invoice catalog refers to a system that manages and organizes invoices.
- Thus, integration of such a system with the customer catalog would mean that the invoice catalog is synced with the customer data.
- This would allow for real-time updates and consistency between the invoice catalog and the customer catalog.
- Extending this approach to other systems within the product would allow for real-time updates and consistency between the customer catalog and other systems within the product.
- This in turn would allow for better customer experience and would also help in reducing the number of errors.
- Customers happy, business happy!

## 🧮 | Aproach

- Let's the imagine the following schemas for the customer catalog and the invoice catalog:

  ```bash
  Customer Catalog
  ----------------
  customer_id (Primary Key)
  name
  email
  phone
  address
  ```

  ```bash
  Invoice Catalog
  ---------------
  invoice_id (Primary Key)
  customer_id (Foreign Key referencing Customer)
  invoice_number
  invoice_date
  due_date
  total_amount
  payment_terms
  ```

- When we create/update/delete a new customer on our product, we also create a new customer on the invoice catalog.
- When we generate an invoice, the system retrieves the customers' information based on the customer_id and this information is populated in the invoice.
- The real-time synchronization between the customer catalog and the invoice catalog maintains accuracy and ensures that the invoice catalog is always up-to-date with the customer data.
- Thus we have a seamless link between the customer catalog and the invoice catalog.
- This approach can be extended to other systems within the product as well.
  <br/>
  <br/>

---
