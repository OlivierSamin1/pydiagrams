#!/usr/bin/env python3
"""
Script to generate Mermaid examples for all diagram types in pydiagrams/diagrams
and create corresponding HTML outputs.
"""
import os
import sys
import webbrowser
import importlib
import inspect
from pathlib import Path

# Example Mermaid diagrams for different categories
DIAGRAMS = {
    "architectural": {
        "context_diagram": """
graph TD
    User((User)) --> System[Digital Banking System]
    System --> DB[(Database)]
    System --> PaymentGateway[Payment Gateway]
    System --> EmailService[Email Service]
    System --> Mobile[Mobile App]
    System --> Web[Web Portal]
""",
        "container_diagram": """
graph TD
    subgraph "Digital Banking System"
    WebApp[Web Application] --> API[API Gateway]
    MobileApp[Mobile App] --> API
    API --> AuthService[Authentication Service]
    API --> AccountService[Account Service]
    API --> TransactionService[Transaction Service]
    API --> NotificationService[Notification Service]
    AccountService --> DB[(Account Database)]
    TransactionService --> TransactionDB[(Transaction Database)]
    NotificationService --> Queue[Message Queue]
    Queue --> EmailWorker[Email Worker]
    Queue --> SMSWorker[SMS Worker]
    end
""",
        "component_diagram": """
graph TD
    subgraph "Transaction Service"
    TransController[Transaction Controller] --> TransValidator[Transaction Validator]
    TransController --> TransProcessor[Transaction Processor]
    TransProcessor --> FeeCalculator[Fee Calculator]
    TransProcessor --> TransactionStore[Transaction Store]
    TransProcessor --> NotificationClient[Notification Client]
    TransactionStore --> Database[(Database)]
    end
    
    API[API Gateway] --> TransController
    NotificationClient --> NotificationService[Notification Service]
""",
        "network_diagram": """
graph TB
    subgraph "Cloud Environment"
    LB[Load Balancer] --> AppServer1[App Server 1]
    LB --> AppServer2[App Server 2]
    AppServer1 --> Cache[Redis Cache]
    AppServer2 --> Cache
    AppServer1 --> DB[(Database Cluster)]
    AppServer2 --> DB
    end
    
    subgraph "Corporate Network"
    Firewall --> AdminPortal[Admin Portal]
    AdminPortal --> VPN[VPN Connection]
    end
    
    Internet((Internet)) --> Firewall
    Internet --> LB
    VPN --> LB
""",
        "deployment_diagram": """
graph TB
    subgraph "Production Environment"
    subgraph "Region A"
    LBA[Load Balancer A] --> AppA1[App Server A1]
    LBA --> AppA2[App Server A2]
    AppA1 --> CacheA[Cache A]
    AppA2 --> CacheA
    AppA1 --> DBA[Primary DB]
    AppA2 --> DBA
    end
    
    subgraph "Region B"
    LBB[Load Balancer B] --> AppB1[App Server B1]
    LBB --> AppB2[App Server B2]
    AppB1 --> CacheB[Cache B]
    AppB2 --> CacheB
    AppB1 --> DBB[Replica DB]
    AppB2 --> DBB
    end
    
    DBA <--> DBB
    
    CDN[Content Delivery Network] --> LBA
    CDN --> LBB
    end
    
    Users((Users)) --> CDN
"""
    },
    "entity": {
        "erd": """
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string id PK
        string name
        string email
        string address
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        string id PK
        date created_at
        string status
        decimal total_amount
        string customer_id FK
    }
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    PRODUCT {
        string id PK
        string name
        string description
        decimal price
        int stock_quantity
    }
    ORDER_ITEM {
        string order_id PK, FK
        string product_id PK, FK
        int quantity
        decimal unit_price
    }
""",
        "dfd": """
graph LR
    User((User)) --> |1. Submit Order| OrderProcess[Order Process]
    OrderProcess --> |2. Validate Order| Validation[Validation Process]
    Validation --> |3. Check Inventory| InventoryDB[(Inventory DB)]
    InventoryDB --> |4. Inventory Status| Validation
    Validation --> |5. Validation Result| OrderProcess
    
    OrderProcess --> |6. Create Order| OrderDB[(Order DB)]
    OrderProcess --> |7. Request Payment| PaymentProcess[Payment Process]
    PaymentProcess --> |8. Process Payment| PaymentGateway[Payment Gateway]
    PaymentGateway --> |9. Payment Result| PaymentProcess
    PaymentProcess --> |10. Payment Status| OrderProcess
    
    OrderProcess --> |11. Order Confirmation| User
    OrderProcess --> |12. Trigger Fulfillment| FulfillmentProcess[Fulfillment Process]
    FulfillmentProcess --> |13. Update Inventory| InventoryDB
    FulfillmentProcess --> |14. Schedule Delivery| DeliveryProcess[Delivery Process]
"""
    },
    "code": {
        "code_diagram": """
graph TD
    subgraph "Application Structure"
    App[App.js] --> Router[Router.js]
    Router --> HomePage[HomePage.js]
    Router --> ProductPage[ProductPage.js]
    Router --> CartPage[CartPage.js]
    Router --> CheckoutPage[CheckoutPage.js]
    
    HomePage --> FeaturedProducts[FeaturedProducts.js]
    HomePage --> CategoryList[CategoryList.js]
    
    ProductPage --> ProductDetails[ProductDetails.js]
    ProductPage --> RelatedProducts[RelatedProducts.js]
    ProductDetails --> ProductGallery[ProductGallery.js]
    ProductDetails --> ProductOptions[ProductOptions.js]
    ProductDetails --> AddToCartButton[AddToCartButton.js]
    
    CartPage --> CartItems[CartItems.js]
    CartPage --> CartSummary[CartSummary.js]
    
    CheckoutPage --> ShippingForm[ShippingForm.js]
    CheckoutPage --> PaymentForm[PaymentForm.js]
    CheckoutPage --> OrderSummary[OrderSummary.js]
    end
    
    subgraph "State Management"
    Store[Store.js] --> UserReducer[UserReducer.js]
    Store --> ProductReducer[ProductReducer.js]
    Store --> CartReducer[CartReducer.js]
    Store --> OrderReducer[OrderReducer.js]
    end
    
    subgraph "API Services"
    ApiClient[ApiClient.js] --> UserService[UserService.js]
    ApiClient --> ProductService[ProductService.js]
    ApiClient --> CartService[CartService.js]
    ApiClient --> OrderService[OrderService.js]
    end
    
    App --> Store
    ProductPage --> ProductService
    CartPage --> CartService
    CheckoutPage --> OrderService
    HomePage --> ProductService
"""
    },
    "uml": {
        "class_diagram": """
classDiagram
    class User {
        -String id
        -String name
        -String email
        -String password
        +register()
        +login()
        +updateProfile()
    }
    
    class Customer {
        -String address
        -String paymentMethod
        +placeOrder()
        +viewOrderHistory()
        +addToCart()
    }
    
    class Admin {
        -String role
        +manageProducts()
        +viewReports()
        +manageUsers()
    }
    
    class Order {
        -String id
        -Date orderDate
        -String status
        -float total
        +calculateTotal()
        +updateStatus()
        +cancel()
    }
    
    class Product {
        -String id
        -String name
        -String description
        -float price
        -int stockQuantity
        +updateStock()
        +updatePrice()
    }
    
    class OrderItem {
        -int quantity
        -float unitPrice
        +calculateSubtotal()
    }
    
    class Cart {
        -String id
        +addItem()
        +removeItem()
        +updateQuantity()
        +clear()
    }
    
    class CartItem {
        -int quantity
        +updateQuantity()
    }
    
    User <|-- Customer
    User <|-- Admin
    Customer "1" -- "0..*" Order : places
    Order "1" *-- "1..*" OrderItem : contains
    OrderItem "1" -- "1" Product : references
    Customer "1" -- "0..1" Cart : has
    Cart "1" *-- "0..*" CartItem : contains
    CartItem "1" -- "1" Product : references
""",
        "activity_diagram": """
graph TD
    Start((Start)) --> Login{User Logged In?}
    Login -->|No| ShowLoginForm[Show Login Form]
    ShowLoginForm --> SubmitLoginForm[Submit Credentials]
    SubmitLoginForm --> ValidCredentials{Valid Credentials?}
    ValidCredentials -->|No| ShowError[Show Error Message]
    ShowError --> ShowLoginForm
    ValidCredentials -->|Yes| Login
    
    Login -->|Yes| ShowProductCatalog[Show Product Catalog]
    ShowProductCatalog --> SearchFilter[Search/Filter Products]
    SearchFilter --> SelectProduct[Select Product]
    SelectProduct --> ShowProductDetails[Show Product Details]
    ShowProductDetails --> AddToCart{Add to Cart?}
    
    AddToCart -->|No| ShowProductCatalog
    AddToCart -->|Yes| UpdateCart[Update Shopping Cart]
    UpdateCart --> Checkout{Proceed to Checkout?}
    
    Checkout -->|No| ShowProductCatalog
    Checkout -->|Yes| ShowCartSummary[Show Cart Summary]
    ShowCartSummary --> EnterShippingInfo[Enter Shipping Information]
    EnterShippingInfo --> EnterPaymentInfo[Enter Payment Information]
    EnterPaymentInfo --> ConfirmOrder[Confirm Order]
    ConfirmOrder --> ProcessPayment[Process Payment]
    ProcessPayment --> PaymentSuccessful{Payment Successful?}
    
    PaymentSuccessful -->|No| ShowPaymentError[Show Payment Error]
    ShowPaymentError --> EnterPaymentInfo
    
    PaymentSuccessful -->|Yes| CreateOrder[Create Order]
    CreateOrder --> SendConfirmation[Send Order Confirmation]
    SendConfirmation --> End((End))
""",
        "sequence_diagram": """
sequenceDiagram
    actor User
    participant Frontend
    participant API
    participant Auth
    participant DB
    participant Email
    
    User->>Frontend: Access Application
    Frontend->>API: Request Initial Data
    API->>DB: Query Data
    DB-->>API: Return Data
    API-->>Frontend: Send Initial Data
    Frontend-->>User: Display UI
    
    User->>Frontend: Submit Login
    Frontend->>API: Login Request
    API->>Auth: Validate Credentials
    Auth->>DB: Query User
    DB-->>Auth: Return User Data
    Auth-->>API: Authentication Result
    API-->>Frontend: Login Response + Token
    Frontend-->>User: Display Dashboard
    
    User->>Frontend: Place Order
    Frontend->>API: Create Order Request
    API->>DB: Save Order
    DB-->>API: Order Created
    API->>Email: Send Order Confirmation
    Email-->>User: Order Confirmation Email
    API-->>Frontend: Order Creation Response
    Frontend-->>User: Order Confirmation Page
""",
        "usecase_diagram": """
graph TD
    subgraph "E-commerce System"
    
    subgraph "Customer Use Cases"
    UC1[Browse Products]
    UC2[Search Products]
    UC3[View Product Details]
    UC4[Add to Cart]
    UC5[Checkout]
    UC6[Track Order]
    UC7[Manage Account]
    UC8[Write Review]
    end
    
    subgraph "Admin Use Cases"
    UC9[Manage Products]
    UC10[Manage Orders]
    UC11[Generate Reports]
    UC12[Manage Users]
    end
    
    subgraph "System Use Cases"
    UC13[Process Payment]
    UC14[Send Notifications]
    UC15[Update Inventory]
    UC16[Log Activities]
    end
    
    end
    
    Customer((Customer)) --- UC1
    Customer --- UC2
    Customer --- UC3
    Customer --- UC4
    Customer --- UC5
    Customer --- UC6
    Customer --- UC7
    Customer --- UC8
    
    Admin((Admin)) --- UC9
    Admin --- UC10
    Admin --- UC11
    Admin --- UC12
    
    System((System)) --- UC13
    System --- UC14
    System --- UC15
    System --- UC16
    
    UC5 -.- UC13
    UC5 -.- UC14
    UC5 -.- UC15
""",
        "state_diagram": """
stateDiagram-v2
    [*] --> BrowsingProducts: User Visits Site
    
    BrowsingProducts --> ViewingProduct: Select Product
    ViewingProduct --> BrowsingProducts: Continue Shopping
    ViewingProduct --> CartFilling: Add to Cart
    
    CartFilling --> CartFilling: Add More Items
    CartFilling --> CartFilling: Update Quantity
    CartFilling --> CartFilling: Remove Item
    CartFilling --> BrowsingProducts: Continue Shopping
    CartFilling --> Checkout: Proceed to Checkout
    
    Checkout --> AddressFilling: Enter Shipping Info
    AddressFilling --> PaymentInfo: Enter Payment
    PaymentInfo --> OrderReview: Review Order
    OrderReview --> ProcessingPayment: Confirm Order
    
    ProcessingPayment --> OrderPlaced: Payment Successful
    ProcessingPayment --> PaymentFailed: Payment Failed
    PaymentFailed --> PaymentInfo: Try Again
    
    OrderPlaced --> OrderProcessing: Begin Fulfillment
    OrderProcessing --> OrderShipped: Ship Order
    OrderShipped --> OrderDelivered: Deliver Order
    OrderDelivered --> [*]
    
    state OrderProcessing {
        [*] --> Verification
        Verification --> Packing
        Packing --> ReadyForShipment
        ReadyForShipment --> [*]
    }
""",
        "component_diagram": """
graph TD
    subgraph "Frontend Layer"
    WebUI[Web UI]
    MobileApp[Mobile App]
    end
    
    subgraph "API Gateway Layer"
    APIGateway[API Gateway]
    end
    
    subgraph "Service Layer"
    AuthService[Authentication Service]
    UserService[User Service]
    ProductService[Product Service]
    CartService[Cart Service]
    OrderService[Order Service]
    PaymentService[Payment Service]
    NotificationService[Notification Service]
    end
    
    subgraph "Data Layer"
    UserDB[(User Database)]
    ProductDB[(Product Database)]
    OrderDB[(Order Database)]
    CartDB[(Cart Database)]
    end
    
    WebUI --> APIGateway
    MobileApp --> APIGateway
    
    APIGateway --> AuthService
    APIGateway --> UserService
    APIGateway --> ProductService
    APIGateway --> CartService
    APIGateway --> OrderService
    
    AuthService --> UserDB
    UserService --> UserDB
    ProductService --> ProductDB
    CartService --> CartDB
    OrderService --> OrderDB
    OrderService --> ProductService
    OrderService --> PaymentService
    OrderService --> NotificationService
"""
    }
}

def get_module_classes(module_path):
    """Get all classes from a module"""
    try:
        # Convert path to module name
        module_path = str(module_path).replace('/', '.').replace('\\', '.')
        if module_path.endswith('.py'):
            module_path = module_path[:-3]
        
        # Remove any leading dots
        module_path = module_path.lstrip('.')
        
        # Import the module
        module = importlib.import_module(module_path)
        
        # Get all classes defined in the module
        classes = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                classes.append(obj)
        
        return classes
    
    except (ImportError, AttributeError) as e:
        print(f"Error importing module {module_path}: {e}")
        return []

def discover_diagram_classes():
    """Discover all diagram classes in the pydiagrams/diagrams directory"""
    current_dir = Path.cwd()
    diagrams_dir = current_dir / "pydiagrams" / "diagrams"
    
    if not diagrams_dir.exists():
        print(f"Error: Diagrams directory not found at {diagrams_dir}")
        return {}
    
    # Add pydiagrams to Python path if needed
    sys.path.insert(0, str(current_dir))
    
    # Find all diagram files
    diagram_classes = {}
    
    for category in ["architectural", "entity", "code", "uml"]:
        category_dir = diagrams_dir / category
        if not category_dir.exists():
            print(f"Warning: Category directory not found: {category_dir}")
            continue
        
        category_classes = {}
        
        # Get all Python files in the category directory
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            # Try to import the module and get classes
            module_path = f"pydiagrams.diagrams.{category}.{py_file.stem}"
            classes = get_module_classes(module_path)
            
            if classes:
                diagram_type = py_file.stem.replace('_diagram', '')
                category_classes[diagram_type] = classes
        
        if category_classes:
            diagram_classes[category] = category_classes
    
    return diagram_classes

def generate_examples():
    """Generate example Mermaid files for all diagram types"""
    current_dir = Path.cwd()
    examples_dir = current_dir / "examples"
    
    if not examples_dir.exists():
        examples_dir.mkdir()
    
    # Create examples for each diagram type
    for category, diagram_types in DIAGRAMS.items():
        category_dir = examples_dir / category
        if not category_dir.exists():
            category_dir.mkdir(exist_ok=True)
        
        for diagram_type, content in diagram_types.items():
            file_path = category_dir / f"{diagram_type}.mmd"
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            
            print(f"Created example file: {file_path}")
    
    return examples_dir

def generate_html_outputs(examples_dir):
    """Generate HTML outputs for all example files"""
    current_dir = Path.cwd()
    outputs_dir = current_dir / "outputs"
    
    if not outputs_dir.exists():
        outputs_dir.mkdir()
    
    # Collect all generated HTML files
    generated_files = []
    
    # Process example files for each category
    for category in ["architectural", "entity", "code", "uml"]:
        category_examples_dir = examples_dir / category
        category_outputs_dir = outputs_dir / category
        
        if not category_examples_dir.exists():
            print(f"Warning: Category examples directory not found: {category_examples_dir}")
            continue
            
        if not category_outputs_dir.exists():
            category_outputs_dir.mkdir(exist_ok=True)
        
        # Process all Mermaid files in the category
        for mmd_file in category_examples_dir.glob("*.mmd"):
            output_file = category_outputs_dir / f"{mmd_file.stem}.html"
            
            # Generate HTML output
            generated_file = create_mermaid_html(mmd_file, output_file)
            if generated_file:
                generated_files.append(generated_file)
    
    return generated_files

def create_mermaid_html(input_file, output_file):
    """Create HTML file with Mermaid diagram"""
    try:
        # Read input file content
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Create HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{input_file.stem}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #333333;
        }}
        
        .mermaid {{
            max-width: 100%;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .buttons {{
            margin-top: 20px;
            text-align: center;
        }}
        
        button {{
            padding: 8px 16px;
            background-color: #4a86e8;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 0 5px;
        }}
        
        button:hover {{
            background-color: #3a76d8;
        }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
                fontFamily: '"Courier New", Courier, monospace'
            }});
            
            // Toggle dark mode
            const darkModeButton = document.getElementById('dark-mode');
            darkModeButton.addEventListener('click', function() {{
                document.body.classList.toggle('dark-mode');
                
                if (document.body.classList.contains('dark-mode')) {{
                    document.body.style.backgroundColor = '#1e1e1e';
                    document.body.style.color = '#e0e0e0';
                    mermaid.initialize({{
                        theme: 'dark'
                    }});
                }} else {{
                    document.body.style.backgroundColor = '#ffffff';
                    document.body.style.color = '#333333';
                    mermaid.initialize({{
                        theme: 'default'
                    }});
                }}
                
                // Re-render the diagram
                const container = document.querySelector(".mermaid");
                const source = container.textContent.trim();
                container.innerHTML = source;
                mermaid.init(undefined, '.mermaid');
            }});
        }});
    </script>
</head>
<body>
    <h1>{input_file.stem.replace('_', ' ').title()}</h1>
    <div class="container">
        <div class="mermaid">
{content}
        </div>
        <div class="buttons">
            <button id="dark-mode">Toggle Dark Mode</button>
        </div>
    </div>
</body>
</html>"""
        
        # Write HTML output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created HTML output: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Error creating HTML for {input_file}: {e}")
        return None

def main():
    print("Generating examples and outputs for all diagram types...")
    
    # Discover diagram classes
    diagram_classes = discover_diagram_classes()
    print(f"Found {sum(len(cat_classes) for cat_classes in diagram_classes.values())} diagram types")
    
    # Generate example files
    examples_dir = generate_examples()
    print(f"Generated example files in {examples_dir}")
    
    # Generate HTML outputs
    generated_files = generate_html_outputs(examples_dir)
    print(f"Generated {len(generated_files)} HTML output files")
    
    # Open all HTML files in browser
    if generated_files:
        print("Opening HTML files in browser...")
        for output_file in generated_files:
            file_url = f"file://{output_file.absolute()}"
            print(f"Opening {file_url}")
            webbrowser.open_new_tab(file_url)
            # Short delay to prevent overwhelming the browser
            import time
            time.sleep(0.5)
    
    print("\nDone! All examples and outputs have been generated.")

if __name__ == "__main__":
    main() 