# Architecture

`django-permissions-manager` is built around **Hexagonal Architecture** (Ports & Adapters) and **Domain-Driven Design (DDD)**. The goal is to keep the business rules completely isolated from Django, so the core logic is testable without a database and swappable without changing application code.

---

## Layer overview

```
┌───────────────────────────────────────────────────────────────┐
│                       Infrastructure                          │
│                                                               │
│  Django models · Django ORM · Repositories · Signals         │
│  Views · Mixins · Backends · Management commands             │
│                         │  ▲                                  │
│                         ▼  │  (implements / fires)           │
├───────────────────────────────────────────────────────────────┤
│                        Application                            │
│                                                               │
│  Use cases (CreateRole, AssignRole, CheckPermission, …)       │
│                         │  ▲                                  │
│                         ▼  │  (calls / returns)              │
├───────────────────────────────────────────────────────────────┤
│                          Domain                               │
│                                                               │
│  Entities · Value objects · Repository interfaces (ports)     │
│  Domain services (RoleManager, PermissionChecker)             │
└───────────────────────────────────────────────────────────────┘
```

---

## Domain layer

The domain layer owns the **business rules** and knows nothing about Django.

### Entities

| Entity | Identifier | Key invariants |
|---|---|---|
| `Role` | UUID | Name must be unique; system roles cannot be deactivated |
| `Permission` | UUID | Code is in `app_label.codename` format |
| `PermissionGroup` | UUID | Name must be unique |
| `UserRole` | UUID | Tracks who assigned the role and when |

### Value objects

| Value object | Wraps | Validates |
|---|---|---|
| `RoleName` | `str` | Non-empty, max 100 characters |
| `PermissionCode` | `str` | Must match `<app>.<codename>` pattern |
| `UserId` | `str` | Non-empty string |
| `EntityReference` | `(type, id)` | Both parts non-empty |

### Repository ports (interfaces)

Ports are abstract base classes in `django_permissions_manager.domain.repositories`. They define *what* the application needs; the infrastructure provides *how*.

| Port | Purpose |
|---|---|
| `RoleRepository` | Full CRUD for roles |
| `PermissionReadRepository` | Read-only permission queries |
| `PermissionRepository` | Extends read — adds `save()` |
| `UserRoleRepository` | Assignment CRUD |
| `PermissionGroupRepository` | Group CRUD |

!!! note "ISP in action"
    Use cases that only need to *look up* permissions depend on `PermissionReadRepository`, not the full `PermissionRepository`. This matches the [Interface Segregation Principle](https://en.wikipedia.org/wiki/Interface_segregation_principle) — callers depend on the narrowest interface they actually need.

### Domain services

| Service | Responsibility |
|---|---|
| `RoleManager` | Activates/deactivates roles; enforces uniqueness; fires `role_status_changed` |
| `PermissionChecker` | Determines if a user holds a given permission through any of their roles |

---

## Application layer

Use cases orchestrate the domain. Each use case:

- Accepts plain Python values (strings, lists, booleans).
- Calls the domain through repository ports and domain services.
- Returns a **DTO** (data-transfer object) — a plain dataclass with no Django dependencies.
- Never touches the database directly.

```
CreateRoleUseCase
    │
    ├── RoleRepository.save()         ← port
    ├── PermissionReadRepository.get_by_code()  ← port
    └── RoleManager.ensure_unique()   ← domain service
```

---

## Infrastructure layer

The infrastructure layer provides **concrete adapters** that fulfil the domain ports.

### Django repositories

Each repository adapter maps between Django ORM objects and domain entities using a **mapper**.

```
DjangoRoleRepository
    │
    ├── implements: RoleRepository
    ├── uses:       RoleModel (ORM)
    └── via:        RoleMapper (domain ↔ ORM)
```

### Mappers

Mappers live in `django_permissions_manager.infrastructure.django.mappers` and perform pure, stateless conversions.

```python
# ORM → domain entity
role: Role = RoleMapper.to_domain(role_model_instance)

# domain entity → ORM model
role_model: RoleModel = RoleMapper.to_model(role_entity)
```

### Signal adapters

Django signals (`role_assigned`, `role_revoked`, `role_status_changed`) decouple domain events from side effects. The infrastructure fires them; your application connects handlers without touching the domain.

---

## Dependency flow

```
Infrastructure  →  Application  →  Domain
     (adapter)      (use case)      (port)
```

Arrows point *inward*. The domain never imports from application or infrastructure. Application never imports from infrastructure. This is the **Dependency Inversion Principle** applied at the architectural level.

---

## Data flow example — assigning a role

```
HTTP request
    │
    ▼
View / API handler
    │  calls
    ▼
get_assign_role_use_case()           ← service factory (infrastructure)
    │  returns wired
    ▼
AssignRoleToUserUseCase.execute()    ← application
    │  calls
    ├── DjangoRoleRepository.get_by_id()    ← infrastructure
    │       └── RoleMapper.to_domain()
    ├── DjangoUserRoleRepository.save()     ← infrastructure
    │       └── UserRoleMapper.to_model()
    └── role_assigned.send()               ← infrastructure signal
            └── cache invalidation receiver
```
