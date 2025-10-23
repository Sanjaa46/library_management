<a id="readme-top"></a>


# Номын сангийн удирдлагын системийн API гарын авлага

## Ерөнхий танилцуулга

#### Энэхүү гарын авлага нь фронтэнд-ээс () номын сангийн удирдлагын системийг хэрхэн ашиглах талаар тайлбарлана.

## Үндсэн боломжууд

- Хэрэглэгч бүртгүүлэх
- Нэвтрэх
- Нууц үгээ солих
- Гишүүнчлэл худалдан авах
- Ном хайх
- Ном зээлэх
- Онцлох номнуудын жагсаалт авах
- Тухайн номын мэдээлэл авах
- Хэрэглэгч өөрийн профайлыг харах


## Номын сангийн удирдлагын системийн API-г хэрхэн ашиглах

Бүх endpoint-ууд хүсэлт болон хариуг JSON хэлбэрээр авна.

## Хэрэглэгч шинээр бүртгүүлэх

### Endpoint: `POST /api/method/library_management.auth.signup_user`

#### Шинэ бүртгэл үүсгэхэд Library Member мөн үүснэ.

### Хүсэлтийн параметрүүд:

| Parameter  | Type   | Required | Description                   |
| ---------- | ------ | -------- | ----------------------------- |
| first_name | string | Yes      | User's first name             |
| last_name  | string | Yes      | User's last name              |
| email      | string | Yes      | User's email (must be unique) |
| phone      | string | Yes      | User's phone number           |
| password   | string | Yes      | User's password               |


### Жишээ хүсэлт
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "11223344",
  "password": "pass"
}
```
### Хариу
- Амжилттай (201 Created):
```json
{
    "message": {
        "success": true
    }
}
```


## Хэрэглэгч нэвтрэх

### Endpoint: `POST /api/method/library_management.auth.login`

##### Хэрэглэгч нэвтрэх үед JWT access болон refresh токен буцаана.

### Хүсэлтийн параметрүүд:

| Parameter | Type   | Required | Description           |
| --------- | ------ | -------- | --------------------- |
| email     | string | Yes      | Registered user email |
| password  | string | Yes      | User password         |

### Хүсэлтийн жишээ:

```json
{
  "email": "john.doe@example.com",
  "password": "pass"
}
```

### Хариу:
- Амжилттай (200 OK):
```json
{
    "message": {
        "access_token": "<ACCESS_TOKEN>",
        "expires_in": 900,
        "refresh_token": "<REFRESH_TOKEN>"
    }
}
```
- Амжилтгүй (Invalid credentials):
```json
{
    "message": "Incorrect password",
    "exc_type": "AuthenticationError"
}
```
### Notes:
- Access токений дуусах хугацаа 900 секунд
- Refresh токенийг ашиглан дахин access токен авах боломжтой. Refresh токений дуусах хугацаа 30 хоног


## Access токен шинэчлэх
### Endpoint: `POST /api/method/library_management.auth.refresh`
#### Access токений хугацаа дуусахад refresh токеноо ашиглан шинэ access токен авах хүсэлт явуулна.

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| refresh_token | string | Yes      | Valid refresh token |

### Хүсэлтийн жишээ:
```json
{
    "refresh_token": "<REFRESH_TOKEN>"
}
```
### Хариу:
```json
{
    "message": {
        "access_token": "<ACCESS_TOKEN>",
        "expires_in": 900
    }
}
```






## Номын жагсаалт авах
### Endpoint: `GET /api/method/library_management.api.get_books`
#### Номын жагсаалтыг төлөвөөр нь шүүж авна.

### Authentication:
- Header `XAuthToken: <JWT_ACCESS_TOKEN>`

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| status        | string | No       | Status of books     |

### Хүсэлтийн жишээ:
```json
{
    "status": "Available"
}
```
### Хариу:
```json
{
  "message": {
    "data": [
      {
        "article_name": "TestArticle1",
        "author": "Robert",
        "status": "Issued",
        "image": "/files/richpoor.jpeg"
      },
      ...
    ]
  }
}
```


## Ном нэрээр хайх
### Endpoint: `GET /api/method/library_management.api.search`
#### Өгөгдлийн сан дахь номнуудаас нэрээр хайлт хийх

### Authentication:
- Header `XAuthToken: <JWT_ACCESS_TOKEN>`

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| query         | string | No       | Search Query        |
| page          | int    | Yes      | Number of page      |
| page_size     | int    | Yes      | Book's number for each page |

### Хүсэлтийн жишээ:
```json
{
    "query": "TestArticle",
    "page": 1,
    "page_size": 2
}

```
### Хариу:
```json
{
  "message": {
    "results": [
      {
        "name": "TestArticle3"
      },
      {
        "name": "TestArticle2"
      }
    ],
    "total": 4,
    "page": 1,
    "page_size": 2,
    "total_pages": 2
  }
}

```




## Тухайн номын мэдээллийг харах
### Endpoint: `GET /api/method/library_management.api.book_info`
#### Тухайн номын мэдээллийг харах

### Authentication:
- Header `XAuthToken: <JWT_ACCESS_TOKEN>`

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| article_name  | string | Yes      | Book name           |

### Хүсэлтийн жишээ:
```json
{
    "article_name": "Rich and Poor"
}
```
### Хариу:
Амжилттай (200 Ok):
```json
{
  "message": {
    "article_name": "Rich and Poor",
    "author": "Robert",
    "description": "<div class=\"ql-editor read-mode\"><p>test desc</p></div>",
    "isbn": "ISBN-1",
    "status": "Issued",
    "image": "/private/files/richpoor.jpeg"
  }
}
```
Амжилтгүй (417 Expectation Failed):
```json
{
  "exception": "frappe.exceptions.ValidationError: Enter book name!",
  "exc_type": "ValidationError",
  "_exc_source": "library_management (app)",
  "exc": "...",
  "_server_messages": "..."
}
```





## Зээлсэн номуудыг харах
### Endpoint: `GET /api/method/library_management.api.my_books`
#### Нэвтэрсэн хэрэглэгч өөрийн зээлсэн номуудыг харах.

### Authentication:
- Header `XAuthToken: <JWT_ACCESS_TOKEN>`

### Хариу:
```json
{
  "message": {
    "books": [
      "Rich and Poor"
    ]
  }
}
```





## Нэвтэрсэн хэрэглэгчийн мэдээлэл (profile)
### Endpoint: ` /api/method/library_management.api.profile`
#### Нэвтэрсэн хэрэглэгчийн нэр, овог, утас болон имейл гэсэн мэдээллүүдийг явуулна.

### Authentication:
- Header `XAuthToken: <JWT_ACCESS_TOKEN>`

### Хариу:
```json
{
  "message": {
    "first_name": "John",
    "last_name": "Doe",
    "phone": "11223344",
    "email": "john.doe@gmail.com"
  }
}
```





## Нууц үгээ солих
### Endpoint: `POST /api/method/library_management.api.change_password`
#### Нэвтэрсэн хэрэглэгч өөрийн хуучин нууц үгийг солих

### Authentication:
- Header `XAuthToken: <JWT_ACCESS_TOKEN>`

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| old_password  | string | Yes      | Old Password        |
| new_password  | string | Yes      | New Password        |

### Хүсэлтийн жишээ:
```json
{
  "old_password": "pass",
  "new_password": "new_pass"
}
```
### Хариу:
Амжилттай (200 Ok):
```json
{
  "message": {
    "Success": true,
    "message": "Password updated successfully!"
  }
}
```
Амжилтгүй (401 Unauthorized):
```json
{
  "exception": "frappe.exceptions.AuthenticationError: Old password is incorrect",
  "exc_type": "AuthenticationError",
  "_exc_source": "library_management (app)",
  "exc": "...",
  "_server_messages": "..."
}
```




## Нууц үг мартсан
### Endpoint: `POST /api/method/library_management.api.forgot_password`
#### Хэрэглэгч нууц үгээ мартсан тохиолдолд бүртгэл үүсгэхдээ ашигласан имейл хаягруу нууц үг сэргээх холбоосыг явуулна. Энэхүү холбоосд нууц үг сэргээх токенийг агуулна. Токен нь нэг цагийн хүчинтэй.

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description                     |
| ------------- | ------ | -------- | ------------------------------- |
| email         | string | Yes      | User's registered email address |

### Хүсэлтийн жишээ:
```json
{
  "email": "john.doe@example.com"
}
```
### Хариу:
Амжилттай (200 Ok):
```json
{
  "message": {
    "Success": true,
    "message": "Password reset link sent!"
  }
}
```
Амжилтгүй (417 Expectation failed):
```json
{
  "exc_type": "ValidationError",
  "_server_messages": "[\"{\\\"message\\\":\\\"User not found!\\\",...}\"]"
}
```

```json
{
  "exc_type": "ValidationError",
  "_server_messages": "[\"{\\\"message\\\":\\\"Email is required!...}\"]"
}
```




## Нууц үг сэргээх
### Endpoint: `POST /api/method/library_management.api.reset_password`
#### Хэрэглэгч нууц үг сэргээх токеноор таньж хэрэглэгчийн нууц үгийг солино.

### Хүсэлтийн параметрүүд:

| Parameter     | Type   | Required | Description               |
| ------------- | ------ | -------- | ------------------------- |
| token         | string | Yes      | User's reset password key |
| new_password  | string | Yes      | User's new password       |

### Хүсэлтийн жишээ:
```json
{
  "token": "<reset_password_key>",
  "new_password": "newPass123"
}
```
### Хариу:
Амжилттай (200 Ok):
```json
{
  "message": {
    "Success": true,
    "message": "Password reseted succesfully!"
  }
}
```
Амжилтгүй (417 Expectation failed):
```json
{
  "exc_type": "ValidationError",
  "_server_messages": "[\"{\\\"message\\\":\\\"Invalid link!\\\",...]"
}
```



## Гишүүнчлэл төлбөр төлөх холбоос авах
### Endpoint: `GET /api/method/library_management.api.create_checkout_session`
#### Нэвтэрсэн хэрэглэгчид гишүүнчлэлийн төлбөр төлөх холбоос үүсгэж өгнө.

### Хариу:
Амжилттай (200 Ok):
```json
{
  "message": {
    "sessionId": "cs_test_a18C...",
    "url": "https://checkout.stripe.com/c/pay/cs_test_a18C...#..."
  }
}
```



<p align="right">(<a href="#readme-top">back to top</a>)</p>