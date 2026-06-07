# django-permissions-manager

Role-based permission management (RBAC) for Django, built with **hexagonal architecture** and **DDD**.

---

## What it does

- **Global roles** — system-wide roles that apply to all users equally.
- **Scoped roles** — roles tied to a specific entity (e.g. a company, a project, a tenant).
- **Permission groups** — named bundles of permissions that can be bulk-assigned to roles.
- **Transparent Django integration** — plugs into `user.has_perm()`, `@permission_required`, `PermissionRequiredMixin`, and DRF's `DjangoModelPermissions` with zero extra code in your views.
- **Permission caching** — works with any Django cache backend (locmem, Redis, Memcached). Cache is invalidated automatically via signals.

The library provides the full RBAC engine — domain logic, repositories, use cases — but **does not expose HTTP endpoints**. You build your own views using whatever stack you prefer and call the provided use cases directly.

---

## Requirements

| Dependency | Version |
|---|---|
| Python | >= 3.11 |
| Django | >= 6.0 |

---

## Install

```bash
pip install django-permissions-manager
```

---

## Quick links

<div class="grid cards" markdown>

- :material-rocket-launch: **[Getting Started](getting-started/installation.md)**  
  Install the library and run your first migration.

- :material-tune: **[Configuration](configuration/settings.md)**  
  All available settings with defaults and examples.

- :material-book-open-variant: **[Usage](usage/checking-permissions.md)**  
  How to check permissions, manage roles and hook into signals.

- :material-code-braces: **[API Reference](api/use-cases.md)**  
  Every use case and factory function documented.

</div>
