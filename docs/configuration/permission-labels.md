# Permission Labels

The library ships 12 permissions across its three models. By default they have English labels.
Use `PERMISSIONS_MANAGER_PERMISSION_LABELS` to override any of them from your own `settings.py`.

---

## How it works

Labels are applied automatically after every `manage.py migrate` via Django's `post_migrate` signal.
This means:

- Labels survive database resets and fresh installs.
- You only need to declare the keys you want to change — omitted permissions keep the library default.

---

## All overridable permissions

```python title="settings.py"
PERMISSIONS_MANAGER_PERMISSION_LABELS = {
    # RoleModel
    "view_role":     "Can view and list roles",
    "add_role":      "Can create new roles",
    "change_role":   "Can modify a role's name, description and assigned permissions",
    "delete_role":   "Can permanently delete roles",
    "activate_role": "Can activate or deactivate roles",

    # UserRoleModel
    "view_userrole": "Can view role assignments",
    "assign_role":   "Can assign roles to users",
    "revoke_role":   "Can revoke role assignments from users",

    # PermissionGroupModel
    "view_permissiongroup":   "Can view and list permission groups",
    "add_permissiongroup":    "Can create new permission groups",
    "change_permissiongroup": "Can modify a permission group's name and permissions",
    "delete_permissiongroup": "Can delete permission groups",
}
```

---

## Example: Spanish labels

```python title="settings.py"
PERMISSIONS_MANAGER_PERMISSION_LABELS = {
    "view_role":     "Puede ver y listar roles",
    "add_role":      "Puede crear nuevos roles",
    "change_role":   "Puede modificar el nombre, descripción y permisos de un rol",
    "delete_role":   "Puede eliminar roles permanentemente",
    "activate_role": "Puede activar o desactivar roles",
    "view_userrole": "Puede ver asignaciones de roles",
    "assign_role":   "Puede asignar roles a usuarios",
    "revoke_role":   "Puede revocar asignaciones de roles",
    "view_permissiongroup":   "Puede ver y listar grupos de permisos",
    "add_permissiongroup":    "Puede crear nuevos grupos de permisos",
    "change_permissiongroup": "Puede modificar el nombre y permisos de un grupo",
    "delete_permissiongroup": "Puede eliminar grupos de permisos",
}
```

---

## Partial overrides

You don't need to list all 12. Only override what you need:

```python title="settings.py"
PERMISSIONS_MANAGER_PERMISSION_LABELS = {
    "assign_role": "Can grant roles to users",
    "revoke_role": "Can remove roles from users",
}
```
