# Architecture Documentation

## System Architecture

Nilgiri Dairy Pro follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────┐
│     UI Layer (Kivy Screens)         │
│  (Presentation & User Interaction)  │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Services Layer (Business Logic)  │
│  - AuthService                       │
│  - DairyService                      │
│  - LedgerService                     │
│  - ReportService                     │
│  - NotificationService               │
│  - BackupService                     │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Models Layer (Data Validation)   │
│  - Farmer, Customer, MilkEntry       │
│  - Payment, BaseModel                │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│   Data Access Layer (Repository)     │
│  - FarmerRepository                  │
│  - CustomerRepository                │
│  - MilkPurchaseRepository            │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│   Database Layer (Connection Pool)   │
│  - Connection Pooling                │
│  - Query Execution                   │
│  - Migration Management              │
└─────────────────────────────────────┘
```

## Design Patterns Used

### 1. **Repository Pattern**
Abstracts database access through repository classes.
```python
farmer = FarmerRepository.get_by_code(code)
```

### 2. **Service Layer Pattern**
Business logic separated from UI.
```python
success, msg = DairyService.record_milk_purchase(...)
```

### 3. **Singleton Pattern**
Database connection is a singleton for efficiency.
```python
db = get_db()  # Always returns same instance
```

### 4. **Validation Pattern**
All models validate themselves before use.
```python
farmer = Farmer(code, name, phone)
is_valid, error = farmer.validate()
```

### 5. **Exception Hierarchy**
Custom exceptions for proper error handling.
```python
try:
    farmer_id = DairyService.create_farmer(...)
except DuplicateError as e:
    # Handle duplicate
except ValidationError as e:
    # Handle validation
```

## Key Features

### Security
- **SQL Injection Prevention**: All queries use parameterized statements
- **Password Hashing**: bcrypt for secure password storage
- **Input Validation**: Comprehensive validation on all inputs
- **Audit Trail**: Every change is logged

### Performance
- **Connection Pooling**: Reuses database connections
- **Query Optimization**: Indexed frequently accessed columns
- **Caching**: Frequently accessed data cached in memory
- **Async Operations**: Long operations run asynchronously

### Reliability
- **Transaction Support**: Multiple operations in single transaction
- **Error Handling**: Comprehensive try-catch with logging
- **Backup/Restore**: Automatic backups with restore capability
- **Database Migrations**: Schema version control

### Maintainability
- **Modular Code**: Each module has single responsibility
- **Docstrings**: Every function documented
- **Type Hints**: Full type annotation for clarity
- **Logging**: Comprehensive logging for debugging

## Data Flow Example: Recording Milk Purchase

```
1. User Input (UI Layer)
   └─→ date, farmer_code, litres, rate

2. Model Validation (Models Layer)
   └─→ MilkEntry.validate()
       - Validates date format
       - Validates quantity range
       - Validates farmer exists

3. Business Logic (Services Layer)
   └─→ DairyService.record_milk_purchase()
       - Gets farmer details
       - Applies fixed/variable rate
       - Calculates total
       - Triggers audit log

4. Data Access (Repository Layer)
   └─→ MilkPurchaseRepository.create()
       - Builds INSERT query
       - Passes to database

5. Database Execution (Database Layer)
   └─→ DatabaseConnection.execute_insert()
       - Gets connection from pool
       - Executes parameterized query
       - Returns last_insert_id

6. Response Flow (Back Up)
   └─→ Return (success, message, purchase_id)
       └─→ Update UI with result
```

## Error Handling Strategy

### Hierarchy
```
DairyException (Base)
├─ ValidationError
├─ DatabaseError
├─ AuthenticationError
├─ NotFoundError
├─ DuplicateError
└─ BusinessLogicError
```

### Handling Example
```python
try:
    farmer_id = DairyService.create_farmer(code, name)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    show_popup("Error", str(e))
except DuplicateError as e:
    logger.warning(f"Duplicate entry: {e}")
    show_popup("Duplicate", "Code already exists")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    show_popup("Error", "Operation failed")
```

## Logging Strategy

### Levels Used
- **DEBUG**: Function entry/exit, variable values
- **INFO**: Operation success, important events
- **WARNING**: Recoverable errors (duplicate, validation failure)
- **ERROR**: Unexpected errors, exceptions
- **CRITICAL**: System failures

### Log Format
```
2024-01-15 10:30:45 - nilgiri_dairy - INFO - Milk purchase recorded: 01 - 10.5L @ 45.0/L = 472.5
```

## Testing Strategy

### Test Coverage
- Unit tests for validators
- Model validation tests
- Repository tests (CRUD)
- Service integration tests
- Target: 80%+ code coverage

### Running Tests
```bash
pytest                          # Run all tests
pytest --cov=src tests/        # With coverage
pytest -v                       # Verbose output
pytest tests/test_validators.py # Specific test file
```
