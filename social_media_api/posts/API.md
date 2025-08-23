
## 📖 API Documentation – Posts & Comments

### Base URL

```
http://127.0.0.1:8000/api/
```

---

## 🔹 Posts Endpoints

### 1. List All Posts

**Endpoint:**

```
GET /api/posts/
```

**Response Example (200 OK):**

```json
[
  {
    "id": 1,
    "title": "My First Post",
    "content": "This is the body of the post",
    "author": "john_doe",
    "created_at": "2025-08-23T10:45:00Z",
    "updated_at": "2025-08-23T10:50:00Z"
  }
]
```

---

### 2. Retrieve a Single Post

**Endpoint:**

```
GET /api/posts/{id}/
```

**Example:**

```
GET /api/posts/1/
```

**Response (200 OK):**

```json
{
  "id": 1,
  "title": "My First Post",
  "content": "This is the body of the post",
  "author": "john_doe",
  "created_at": "2025-08-23T10:45:00Z",
  "updated_at": "2025-08-23T10:50:00Z"
}
```

---

### 3. Create a Post

**Endpoint:**

```
POST /api/posts/
```

**Request Body (JSON):**

```json
{
  "title": "Another Post",
  "content": "This is some new content"
}
```

**Response (201 Created):**

```json
{
  "id": 2,
  "title": "Another Post",
  "content": "This is some new content",
  "author": "john_doe",
  "created_at": "2025-08-23T11:00:00Z",
  "updated_at": "2025-08-23T11:00:00Z"
}
```

---

### 4. Update a Post

**Endpoint:**

```
PUT /api/posts/{id}/
```

**Request Body (JSON):**

```json
{
  "title": "Updated Title",
  "content": "Updated body of the post"
}
```

**Response (200 OK):**

```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated body of the post",
  "author": "john_doe",
  "created_at": "2025-08-23T10:45:00Z",
  "updated_at": "2025-08-23T11:05:00Z"
}
```

---

### 5. Delete a Post

**Endpoint:**

```
DELETE /api/posts/{id}/
```

**Response (204 No Content):**

```
(empty response)
```

---

## 🔹 Comments Endpoints

### 1. List Comments for a Post

**Endpoint:**

```
GET /api/posts/{post_id}/comments/
```

**Response Example:**

```json
[
  {
    "id": 1,
    "post": 1,
    "author": "jane_doe",
    "text": "Nice post!",
    "created_at": "2025-08-23T11:10:00Z"
  }
]
```

---

### 2. Create a Comment

**Endpoint:**

```
POST /api/posts/{post_id}/comments/
```

**Request Body (JSON):**

```json
{
  "text": "This is a new comment"
}
```

**Response (201 Created):**

```json
{
  "id": 2,
  "post": 1,
  "author": "john_doe",
  "text": "This is a new comment",
  "created_at": "2025-08-23T11:15:00Z"
}
```

---

### 3. Update a Comment

**Endpoint:**

```
PUT /api/comments/{id}/
```

**Request Body (JSON):**

```json
{
  "text": "Updated comment text"
}
```

**Response (200 OK):**

```json
{
  "id": 1,
  "post": 1,
  "author": "jane_doe",
  "text": "Updated comment text",
  "created_at": "2025-08-23T11:10:00Z",
  "updated_at": "2025-08-23T11:20:00Z"
}
```

---

### 4. Delete a Comment

**Endpoint:**

```
DELETE /api/comments/{id}/
```

**Response (204 No Content):**

```
(empty response)
```

---

✅ That covers **all CRUD operations for Posts and Comments** with request/response examples.
If you want, I can also show you how to **auto-generate this documentation** with **DRF + drf-yasg (Swagger/OpenAPI)** so you don’t have to manually maintain docs.


