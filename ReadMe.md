# Problem Statement: Real-Time Order Processing System with Kafka

## Background
In traditional e-commerce or retail systems, order processing often follows a synchronous, monolithic approach, leading to bottlenecks, lack of scalability, and potential system failures. When an order is placed, multiple dependent services—such as inventory management and payment processing—need to interact. If any of these services fail, it can cause delays, inconsistencies, or even data loss.

## Problem Statement
We aim to build a **real-time, event-driven order processing system** using **Apache Kafka** as the event broker. The system will consist of three key microservices:

1. **Order Service** – Handles order creation and updates order status.
2. **Payment Service** – Processes payments and updates order status accordingly.
3. **Inventory Service** – Manages stock levels and updates inventory after successful payments.

### Scenario
- A user places an order for an item that has 10 units available in inventory.
- The **Order Service** creates an order with a `PENDING` state and publishes an event to Kafka.
- The **Payment Service** listens to the order event, processes the payment, and updates the order state to `PAID` or `FAILED`.
- If the payment is successful (`PAID` state):
  - The **Inventory Service** listens to the payment event and deducts the ordered quantity from the inventory.
  - The order status is updated to `COMPLETED`.
- If the payment fails (`FAILED` state):
  - The order remains in `FAILED` state, and no inventory is deducted.
  
### Challenges Addressed
- **Decoupling Services:** By using Kafka, we eliminate direct dependencies between services, allowing better scalability and fault tolerance.
- **Eventual Consistency:** Ensures inventory updates happen only after successful payments.
- **Fault Tolerance:** Implementing a Dead Letter Queue (DLQ) for failed payment events.
- **Scalability:** Each service can scale independently based on demand.

## Technologies Used
- **Backend:** Python FastAPI (for microservices)
- **Message Broker:** Apache Kafka
- **Database:** PostgreSQL 
- **Deployment:** Docker

## Expected Outcome
This project will demonstrate how event-driven architectures can improve system resilience and scalability while ensuring consistency across services. It will also serve as a portfolio-worthy project to showcase expertise in **Kafka, microservices, and event-driven design**.

