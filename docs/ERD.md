# Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ BOOKING : makes
    USER ||--o{ EVENT : creates
    CATEGORY ||--o{ EVENT : classifies
    EVENT ||--o{ BOOKING : receives

    USER {
        int id PK
        string username
        string email
        string password
    }

    CATEGORY {
        int id PK
        string name
        string slug
        text description
    }

    EVENT {
        int id PK
        string title
        string slug
        text description
        date event_date
        time event_time
        string location
        int capacity
        int category_id FK
        int created_by_id FK
        bool is_published
    }

    BOOKING {
        int id PK
        int user_id FK
        int event_id FK
        int ticket_count
        string confirmation_code
        string status
        datetime booked_at
    }
```

## Actors

| Actor | Description |
|-------|-------------|
| Guest | Browse events; must register to book |
| Registered User | Book tickets, view/cancel bookings |
| Staff | CRUD events and categories via `/manage/` |
| Admin | Full access via Django admin |
