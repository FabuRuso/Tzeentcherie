# Tzeentcherie Project
## Showcase DRF backend server, implementing basic feeding-classifield functional with flat user-role system

> [!IMPORTANT]
> ### This README.md (especially the raw view) contains too wide tables

> ### Headers to faster orientation
> * [Features](#features)
> * [Technologies](#technologies)
> * [Run the project](#run-the-project)
> * [Scheme of db](#scheme-of-db)
> * [Views query](#views-query)
> * [DEBUG releasing data in db](#debug-releasing-data-in-db)

### Features 
- Date-ordered output list of `Tzeentcheries`<br/>
&emsp;&mdash; short buissnesslike classifieds
- Flat user-role model
- Admin API for operation with users, tzeentcheries and roles
- Scalable REST API (GET, POST, PATCH, DELETE) interfaces for CRUD with divided responsibility
- JWT-login system with soft deletion and salted-hash password saving

---

### Technologies
- Python 3.12
- Django 6
- Django REST framework
- PyJWT
- bcrypt
- SQLite3

---

### Run the project
```bash
git clone <repo>
cd <project>
python -m venv venv
# Linux: source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### Scheme of db

| `User`      | type   | comment        |
|  ----       | ----   | -------        |
| id          | `pk`   | *auto unique*  |
| email       | `str`  | *unique*       |
| forename    | `str`  | &mdash;        |
| patronymic  | `str`  | *may be null*  |
| surname     | `str`  | &mdash;        |
| password_hs | `str`  | *256-bytechar* |
| is_active   | `bool` | de-activation  |

---

| `Role`                | type   | comment                     |
|  ----                 | ----   | -------                     |
| id                    | `pk`   | *auto unique*               |
| role_name             | `str`  | *unique*                    |
| god_perm              | `bool` | super-user                  |
| edit_roles_perm       | `bool` | editing roles               |
| post_owned_perm       | `bool` | creating own objects        |
| put_owned_perm        | `bool` | editing own objects         |
| delete_owned_perm     | `bool` | deleting own object         |
| put_not_owned_perm    | `bool` | editing not own objects     |
| delete_not_owned_perm | `bool` | deleting not own objects    |
| put_users_perm        | `bool` | editing info of other users |
| deactivate_users_perm | `bool` | deactivating of users       |
| delete_users_perm     | `bool` | full deleting of users      |

---

| `RoleAssignment` | type   | comment       |
|  --------------  | ----   | -------       |
| id               | `pk`   | *auto unique* |
| user             | `User` | *ForeignKey*  |
| role             | `Role` | *ForeignKey*  |

---

| `Tzeentcherie` | type       | comment                                 |
|  ------------  | ----       | -------                                 |
| id             | `pk`       | *auto unique*                           |
| title          | `str`      | *unique*                                |
| description    | `str`      | &mdash;                                 |
| owner          | `User`     | *ForeignKey*                            |
| created_at     | `datetime` | *auto*<br/>output list is ordered by it |

---

### Views query

Every query starts with `api/` — it will be omitted in the table

Every method starts with `test/core/views/` — it will be omitted in the table

Only **successful** statuses are represented

| method   | query                               | views                                                            | status          | body-params                                                                                  | comment                                                         |
| ------   | -----                               | -----                                                            | ------          | -----------                                                                                  | -------                                                         |
| `GET`    | `hello/`                            | `hello/hello(request)`                                           | `418`           | —                                                                                            | —                                                               |
| `POST`   | `register/`                         | `register/register(request)`                                     | `201`           | `email`<br/>`forename`<br/>`patronymic`<br/>`surname`<br/>`password`<br/>`password_confirm`  | register a user                                                 |
| `POST`   | `login/`                            | `login/login(request)`                                           | `200`           | `email`<br/>`password`                                                                       | —                                                               |
| `GET`    | `profile/`                          | `profile/profile(request)`                                       | `200`           | —                                                                                            | get own profile                                                 |
| `PUT`    | `profile/`                          | `profile/profile(request)`                                       | `200`           | `forename`<br/>`patronymic`<br/>`surname`                                                    | update profile                                                  |
| `DELETE` | `deactivate/`                       | `deactivate/deactivate(request)`                                 | `200`           | —                                                                                            | soft delete account                                             |
| `POST`   | `owned/tzeentcherie/<title>/`       | `owned_act/owned_act(request, title)`                            | `201`           | `description` (optional)                                                                     | create owned tzeentcherie                                       |
| `PUT`    | `owned/tzeentcherie/<title>/`       | `owned_act/owned_act(request, title)`                            | `200`           | `description`                                                                                | update owned tzeentcherie                                       |
| `DELETE` | `owned/tzeentcherie/<title>/`       | `owned_act/owned_act(request, title)`                            | `200`           | —                                                                                            | delete owned tzeentcherie                                       |
| `GET`    | `owned/tzeentcherie/<title>/`       | `owned_act/owned_act(request, title)`                            | `200`           | —                                                                                            | get owned tzeentcherie                                          |
| `PUT`    | `not-owned/tzeentcherie/<title>/`   | `not_owned_act/not_owned_act(request, title)`                    | `200`           | `description`                                                                                | moderate (edit) foreign tzeentcherie                            |
| `DELETE` | `not-owned/tzeentcherie/<title>/`   | `not_owned_act/not_owned_act(request, title)`                    | `200`           | —                                                                                            | moderate (delete) foreign tzeentcherie                          |
| `GET`    | `not-owned/tzeentcherie/<title>/`   | `not_owned_act/not_owned_act(request, title)`                    | `200`           | —                                                                                            | view foreign tzeentcherie                                       |
| `PUT`    | `users/<email>/`                    | `users_act/users_act(request, email)`                            | `200`           | `forename`<br/>`patronymic`<br/>`surname`                                                    | admin edit user info                                            |
| `PATCH`  | `users/<email>/`                    | `users_act/users_act(request, email)`                            | `200`           | —                                                                                            | admin soft deactivate user                                      |
| `DELETE` | `users/<email>/`                    | `users_act/users_act(request, email)`                            | `200`           | —                                                                                            | admin permanently delete user                                   |
| `GET`    | `users/<email>/`                    | `users_act/users_act(request, email)`                            | `200`           | —                                                                                            | admin view user details                                         |
| `PUT`    | `role/<email>/`                     | `role_set/role_set(request, email)`                              | `200`           | `role_name`                                                                                  | assign role to user                                             |
| `GET`    | `role/<email>/`                     | `role_set/role_set(request, email)`                              | `200`           | —                                                                                            | get user role                                                   |
| `PUT`    | `roles/<role_name>/`                | `role_act/role_act(request, role_name)`                          | `200`<br/>`201` | all permission fields (e.g., `god_perm`, `edit_roles_perm`, …)                               | create or update role                                           |
| `GET`    | `roles/<role_name>/`                | `role_act/role_act(request, role_name)`                          | `200`           | —                                                                                            | get role details                                                |
| `DELETE` | `roles/<role_name>/`                | `role_act/role_act(request, role_name)`                          | `204`           | —                                                                                            | delete role (if unused)                                         |
| `GET`    | `list/`                             | `full_list/full_list(request)`                                   | `200`           | `offset` (optional, default 0)                                                               | public or signed list of tzeentcherie                           |
| `PUT`    | `debug/release/`                    | `release_debug_placeholders/release_debug_placeholders(request)` | `201`           | —                                                                                            | create admin & moderator test accounts (only when `DEBUG=True`) |

---

### DEBUG releasing data in db

if `DEBUG`-field in `test/test/settings.py` was setted in `True`,<br/>
&emsp;there is the debug-placeholders-endpoint in `/api/debug/release/`

For unsetted permissions in `Role` see default values of the Django model

| `User`     | admin               | moder                   |
|  ----      | -----               | -----                   |
| email      | `admin@himmel.test` | `moderator@admins.test` |
| forename   | `Herr`              | `Dr`                    |
| patronymic | &mdash;             | &mdash;                 |
| surname    | `Goetze`            | `Who`                   |
| password   | `admin`             | `moder`                 |

| `Role`                | admin   | moder   |
|  ----                 | -----   | -----   |
| role_name             | `admin` | `moder` |
| god_perm              | `True`  | &mdash; |
| edit_roles_perm       | `True`  | &mdash; |
| put_not_owned_perm    | &mdash; | `True`  |
| delete_not_owned_perm | &mdash; | `True`  |

And accordant `RoleAssignment`

---
