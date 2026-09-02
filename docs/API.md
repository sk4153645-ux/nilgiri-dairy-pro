# API Reference

## Authentication Service

### `AuthService.register(email, password, dairy_name, dairy_phone)`
Register new user.

**Parameters:**
- `email`: User email address
- `password`: User password (min 6 chars)
- `dairy_name`: Name of dairy
- `dairy_phone`: Dairy phone number

**Returns:**
- `Tuple[bool, str]`: (success, message)

**Example:**
```python
success, msg = AuthService.register(
    email="farmer@dairy.com",
    password="secure123",
    dairy_name="Shree Ram Dairy",
    dairy_phone="9876543210"
)
```

### `AuthService.login(email, password)`
Authenticate user.

**Returns:**
- `Tuple[bool, str, Optional[dict]]`: (success, message, user_data)

---

## Dairy Service

### `DairyService.create_farmer(code, name, phone, address)`
Create new farmer.

**Returns:**
- `Tuple[bool, str, int]`: (success, message, farmer_id)

### `DairyService.list_farmers()`
List all active farmers.

**Returns:**
- `Tuple[bool, str, List[Dict]]`: (success, message, farmers)

### `DairyService.record_milk_purchase(...)`
Record milk purchase from farmer.

**Parameters:**
- `date`: Purchase date (YYYY-MM-DD)
- `shift`: Morning or Evening
- `farmer_code`: Farmer code
- `milk_type`: Cow or Buffalo
- `litres`: Quantity in litres
- `fat`: Fat percentage
- `snf`: SNF value
- `rate`: Rate per litre
- `notes`: Optional notes

**Returns:**
- `Tuple[bool, str, int]`: (success, message, purchase_id)

### `DairyService.get_daily_collection(date, shift)`
Get daily milk collection summary.

**Returns:**
- `Tuple[bool, str, Dict]`: (success, message, summary)

---

## Ledger Service

### `LedgerService.get_farmer_ledger(farmer_code)`
Get complete ledger for farmer.

**Returns:**
- `Tuple[bool, str, List[Dict]]`: (success, message, ledger_entries)

**Ledger Entry:**
```python
{
    'date': '2024-01-01',
    'type': 'Milk Purchase',  # or 'Payment'
    'amount': 472.5,
    'balance': 472.5,
    'litres': 10.5,
    'milk_type': 'Cow'
}
```

### `LedgerService.get_farmer_outstanding(farmer_code)`
Get outstanding amount owed to farmer.

**Returns:**
- `Tuple[bool, str, float]`: (success, message, outstanding)

---

## Report Service

### `ReportService.get_daily_report(date)`
Generate daily collection report.

**Returns:**
- `Tuple[bool, str, Dict]`: (success, message, report)

**Report Structure:**
```python
{
    'date': '2024-01-01',
    'morning': [{milk_type, entries, total_litres, avg_fat, total_amount}],
    'evening': [...],
    'sales': [...]
}
```

### `ReportService.get_monthly_report(year, month)`
Generate monthly summary.

### `ReportService.get_outstanding_report()`
Get all outstanding payments.

**Returns:**
- `Tuple[bool, str, List[Dict]]`: (success, message, outstanding_list)

---

## Notification Service

### `NotificationService.send_sms(phone, message)`
Send SMS notification.

**Parameters:**
- `phone`: Phone number
- `message`: Message content

**Returns:**
- `Tuple[bool, str]`: (success, message)

### `NotificationService.send_whatsapp(phone, message)`
Send WhatsApp notification.

**Returns:**
- `Tuple[bool, str]`: (success, message)

---

## Backup Service

### `BackupService.create_backup()`
Create database backup.

**Returns:**
- `Tuple[bool, str, str]`: (success, message, backup_path)

### `BackupService.restore_backup(backup_path)`
Restore from backup.

**Returns:**
- `Tuple[bool, str]`: (success, message)

### `BackupService.list_backups()`
List all available backups.

**Returns:**
- `Tuple[bool, str, List[Dict]]`: (success, message, backups)

---

## Exception Classes

### `ValidationError`
Raised when input validation fails.

```python
from src.core.exceptions import ValidationError

try:
    farmer = Farmer(code, name, phone)
    is_valid, error = farmer.validate()
    if not is_valid:
        raise ValidationError(error)
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Field: {e.field}")
```

### `DatabaseError`
Raised when database operations fail.

### `AuthenticationError`
Raised when authentication fails.

### `DuplicateError`
Raised when trying to create duplicate record.

### `NotFoundError`
Raised when resource not found.

### `BusinessLogicError`
Raised when business logic validation fails.

---

## Models

### Farmer Model
```python
from src.models.farmer import Farmer

farmer = Farmer(
    code="01",
    name="Ramesh Kumar",
    phone="9876543210",
    address="Village Address",
    rate_type="fixed",
    fixed_rate=45.0
)

is_valid, error = farmer.validate()
rate = farmer.get_rate(40.0)  # Returns 45.0 if fixed, else 40.0
```

### MilkEntry Model
```python
from src.models.milk_entry import MilkEntry

entry = MilkEntry(
    date="2024-01-01",
    shift="Morning",
    milk_type="Cow",
    litres=10.5,
    fat=4.5,
    snf=8.5,
    rate=45.0
)

total = entry.calculate_total()  # 472.5
```

### Payment Model
```python
from src.models.payment import Payment

payment = Payment(
    date="2024-01-01",
    entity_code="01",
    amount=5000.0,
    payment_mode="Cash"
)

is_valid, error = payment.validate()
```
