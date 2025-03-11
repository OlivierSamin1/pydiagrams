#!/usr/bin/env python3
"""
Script to generate example files for all diagram types in PyDiagrams
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
current_dir = Path(__file__).resolve().parent
project_root = current_dir
sys.path.insert(0, str(project_root))

# Ensure examples and output directories exist
examples_dir = project_root / "examples"
output_dir = project_root / "output"
examples_dir.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True)

# Dictionary of examples by category
examples = {
    "architectural": {
        "context_diagram": """
        "container_diagram": """
graph TD
    subgraph "Internet Banking System"
    WebApp[Web Application] --> API[API Application]
    MobileApp[Mobile App] --> API
    API --> Database[(Database)]
    end
    
    User[Banking Customer] --> WebApp
    User --> MobileApp
    API --> Email[Email System]
    API --> Mainframe[Mainframe Banking System]
""",
        "component_diagram": """
graph TD
    subgraph "API Application"
    SignIn[Sign In Controller] --> Security[Security Component]
    Accounts[Accounts Controller] --> Accounts_Service[Accounts Service]
    Accounts_Service --> Database[(Database)]
    Transactions[Transactions Controller] --> Transactions_Service[Transactions Service]
    Transactions_Service --> Mainframe[Mainframe Banking System]
    end
    
    MobileApp[Mobile App] --> SignIn
    MobileApp --> Accounts
    MobileApp --> Transactions
""",
        "network_diagram": """
graph TB
    subgraph "London Office"
    L_Router[Router] --- L_Firewall[Firewall]
    L_Firewall --- L_Switch[Switch]
    L_Switch --- L_Server1[Web Server]
    L_Switch --- L_Server2[Database Server]
    end
    
    subgraph "New York Office"
    NY_Router[Router] --- NY_Firewall[Firewall]
    NY_Firewall --- NY_Switch[Switch]
    NY_Switch --- NY_Server1[Application Server]
    NY_Switch --- NY_Server2[File Server]
    end
    
    Internet((Internet)) --- L_Router
    Internet --- NY_Router
    
    L_Router --- VPN{VPN Tunnel} --- NY_Router
""",
        "deployment_diagram": """
@startuml
!include <aws/common>
!include <aws/Compute/all>
!include <aws/Database/all>
!include <aws/Storage/all>

title AWS Deployment Diagram

cloud "AWS Cloud" {
    EC2WebServer(web, "Web Server", "t3.medium")
    EC2WebServer(app, "App Server", "t3.large")
    RDSInstance(db, "Database", "db.r5.large")
    S3(s3, "Static Assets", "Standard")
    
    ElasticLoadBalancing(lb, "Load Balancer")
    
    lb -> web
    web -> app
    app -> db
    web -> s3
}

actor "User" as user
user -> lb

@enduml
"""
    },
    "entity": {
        "erd": """
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string name
        string email
        string address
    }
    ORDER ||--|{ LINE_ITEM : contains
    ORDER {
        int orderNumber
        date orderDate
        string status
    }
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
    LINE_ITEM {
        int quantity
        float price
    }
    PRODUCT {
        string name
        string description
        float price
    }
""",
        "dfd": """
graph LR
    User((User)) --> |1. Input Data| Process1[Process Data]
    Process1 --> |2. Store Data| DB[(Database)]
    Process1 --> |3. Request Validation| Process2[Validate Data]
    Process2 --> |4. Request External Info| External[External System]
    External --> |5. Provide Info| Process2
    Process2 --> |6. Return Validation Result| Process1
    Process1 --> |7. Return Result| User
"""
    },
    "code": {
        "code_diagram": """
graph TD
    subgraph "Application Structure"
    App[App.js] --> Router[Router.js]
    Router --> Home[Home.js]
    Router --> Products[Products.js]
    Router --> Cart[Cart.js]
    Products --> ProductDetail[ProductDetail.js]
    Cart --> Checkout[Checkout.js]
    end
    
    subgraph "State Management"
    Store[Store.js] --> ProductsReducer[productsReducer.js]
    Store --> CartReducer[cartReducer.js]
    Store --> UserReducer[userReducer.js]
    end
    
    App --> Store
    Products --> ProductsReducer
    Cart --> CartReducer
    Home --> UserReducer
"""
    },
    "uml": {
        "class_diagram": """
classDiagram
    class Customer {
        -String name
        -String email
        -String address
        +register()
        +login()
        +updateProfile()
    }
    
    class Order {
        -int orderNumber
        -Date orderDate
        -String status
        +placeOrder()
        +cancelOrder()
        +ship()
    }
    
    class Product {
        -String name
        -String description
        -float price
        +addToCart()
        +removeFromCart()
    }
    
    class Payment {
        -float amount
        -Date paymentDate
        -String method
        +processPayment()
        +refund()
    }
    
    Customer "1" -- "0..*" Order : places
    Order "1" -- "1..*" Product : contains
    Order "1" -- "1" Payment : paid by
""",
        "sequence_diagram": """
@startuml
actor User
participant "Web UI" as UI
participant "API Server" as API
participant "Database" as DB
participant "Email Service" as Email

User -> UI: Register
UI -> API: POST /register
API -> DB: Insert User
DB --> API: User Created
API -> Email: Send Welcome Email
Email --> API: Email Sent
API --> UI: Registration Success
UI --> User: Show Success Message

User -> UI: Login
UI -> API: POST /login
API -> DB: Check Credentials
DB --> API: Valid Credentials
API --> UI: Return Auth Token
UI --> User: Show Dashboard
@enduml
""",
        "activity_diagram": """
graph TD
    Start((Start)) --> Login[Login]
    Login --> ValidCred{Valid Credentials?}
    ValidCred -->|No| ShowError[Show Error]
    ShowError --> Login
    ValidCred -->|Yes| Dashboard[Show Dashboard]
    Dashboard --> Action{Select Action}
    Action -->|View Profile| Profile[View Profile]
    Action -->|Place Order| Order[Place Order]
    Action -->|View History| History[View History]
    Profile --> Dashboard
    Order --> Cart[Add to Cart]
    Cart --> Checkout{Checkout?}
    Checkout -->|No| Dashboard
    Checkout -->|Yes| Payment[Process Payment]
    Payment --> Success{Success?}
    Success -->|No| ShowPayError[Show Payment Error]
    ShowPayError --> Payment
    Success -->|Yes| Confirmation[Show Confirmation]
    Confirmation --> Dashboard
    History --> Dashboard
    Dashboard --> Logout[Logout]
    Logout --> End((End))
""",
        "usecase_diagram": """
@startuml
left to right direction
actor Customer
actor Admin
actor System

rectangle "E-commerce System" {
  usecase "Browse Products" as UC1
  usecase "Add to Cart" as UC2
  usecase "Checkout" as UC3
  usecase "Process Payment" as UC4
  usecase "Ship Order" as UC5
  usecase "Manage Products" as UC6
  usecase "Manage Orders" as UC7
  usecase "Generate Reports" as UC8
  usecase "Send Notifications" as UC9
  
  Customer -- UC1
  Customer -- UC2
  Customer -- UC3
  
  Admin -- UC6
  Admin -- UC7
  Admin -- UC8
  
  UC3 .> UC4 : includes
  UC4 .> UC5 : triggers
  UC5 .> UC9 : includes
  
  System -- UC9
}
@enduml
""",
        "state_diagram": """
stateDiagram-v2
    [*] --> Idle
    
    Idle --> Processing: Order Received
    Processing --> Fulfilling: Order Processed
    Processing --> Cancelled: Cancel Request
    
    Fulfilling --> Shipped: Items Shipped
    Shipped --> Delivered: Items Delivered
    
    Delivered --> [*]
    Cancelled --> [*]
    
    state Processing {
        [*] --> ValidatingPayment
        ValidatingPayment --> PreparingItems: Payment Valid
        ValidatingPayment --> Failed: Payment Invalid
        PreparingItems --> [*]: Items Ready
        Failed --> [*]
    }
""",
        "component_diagram": """
@startuml
package "Frontend" {
  [User Interface] as UI
  [Router]
  [State Management] as State
}

package "Backend" {
  [API Gateway] as API
  [Authentication Service] as Auth
  [User Service] as User
  [Product Service] as Product
  [Order Service] as Order
  [Payment Service] as Payment
}

database "Databases" {
  [User DB] as UserDB
  [Product DB] as ProductDB
  [Order DB] as OrderDB
}

UI --> Router
Router --> State
Router --> API

API --> Auth
API --> User
API --> Product
API --> Order
API --> Payment

User --> UserDB
Product --> ProductDB
Order --> OrderDB
Payment --> OrderDB

@enduml
"""
    }
}

# Save all examples to files
for category, diagrams in examples.items():
    print(f"Generating examples for {category} diagrams...")
    for diagram_type, content in diagrams.items():
        file_extension = ".mmd"
        file_path = examples_dir / f"{category}_{diagram_type}{file_extension}"
        
        with open(file_path, "w") as f:
            f.write(content.strip())
        
        print(f"  Created {file_path}")

print("\nAll example files have been generated in the 'examples' directory.") 