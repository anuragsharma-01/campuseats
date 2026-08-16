# HTTP Log

## Request 1 — Get Post

### Command

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1

### Response

```text
 
HTTP/2 200 
date: Sat, 15 Aug 2026 12:38:18 GMT
content-type: application/json; charset=utf-8
content-length: 292
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=UyhbZ%2F0MO1mJoZS7M4Hj8SWBXp3NkwnJgHEYoqocyDE%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785191026"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=UyhbZ%2F0MO1mJoZS7M4Hj8SWBXp3NkwnJgHEYoqocyDE%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785191026"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785191063
age: 16350
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b8416df8adb660-AMS
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}% 
### Annotation

- Status: `200 OK` — the server successfully returned the requested post.
- Content-Type: `application/json` — the response body is formatted as JSON.

## Request 2 — Get User

### Command

```bash
curl -i https://jsonplaceholder.typicode.com/users/1
```

### Full Response

```text
HTTP/2 200
date: Sat, 15 Aug 2026 12:41:42 GMT
content-type: application/json; charset=utf-8
content-length: 509
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"1fd-+2Y3G3w049iSZtw5t1mzSnunngE"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=m23T6Tj%2BQUZnIwphHAim1ChY9yjwiqMeEy5yHiMrfN0%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785634999"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=m23T6Tj%2BQUZnIwphHAim1ChY9yjwiqMeEy5yHiMrfN0%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785634999}
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785635057
age: 2987
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b846660a190b6a-AMS
alt-svc: h3=":443"; ma=86400

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}
```

### Annotation

* **Status:** `200 OK` — the server successfully returned the requested user.
* **Content-Type:** `application/json; charset=utf-8` — the response body is JSON, encoded using UTF-8.

---

## Request 3 — Get Todo

### Command

```bash
curl -i https://jsonplaceholder.typicode.com/todos/1
```

### Full Response

```text
HTTP/2 200
date: Sat, 15 Aug 2026 12:44:06 GMT
content-type: application/json; charset=utf-8
content-length: 83
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"53-hfEnumeNh6YirfjyjaujcOPPT+s"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=Iw0JC8rIKAJwHSPInLC3NbMfAyzWfNxuyfn8atD37yE%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1752022215"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=Iw0JC8rIKAJwHSPInLC3NbMfAyzWfNxuyfn8atD37yE%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1752022215"
server: cloudflare
vary: Origin
accept-encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1752022235
age: 4
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b849ea29f83379-AMS
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

### Annotation

* **Status:** `200 OK` — the server successfully returned the requested todo item.
* **Content-Type:** `application/json; charset=utf-8` — the response body is JSON encoded using UTF-8.

---

## Request 4 — Get Comment

### Command

```bash
curl -i https://jsonplaceholder.typicode.com/comments/1
```

### Full Response

```text
HTTP/2 200
date: Sat, 15 Aug 2026 12:44:51 GMT
content-type: application/json; charset=utf-8
content-length: 268
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"10c-KJ4I9RM/+33TKdV8CFsIvqsDSP0"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=C4h1dyT15nRwK%2F71KPxt4SaGNEn%2FaIGnlUSl%2Fzx9%2FNY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785740413"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=C4h1dyT15nRwK%2F71KPxt4SaGNEn%2FaIGnlUSl%2Fzx9%2FNY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785740413}
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 919
x-ratelimit-reset: 1785740416
age: 17375
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a2b84b05cd590e35-AMS
alt-svc: h3=":443"; ma=86400

{
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
}
```

### Annotation

* **Status:** `200 OK` — the server successfully returned the requested comment.
* **Content-Type:** `application/json; charset=utf-8` — the response body is JSON encoded using UTF-8.

---
## Request 5 — Deliberate 404

### Command

```bash
curl -i https://jsonplaceholder.typicode.com/posts/999999
```

### Full Response

```text
HTTP/2 404
date: Sat, 15 Aug 2026 12:45:34 GMT
content-type: application/json; charset=utf-8
content-length: 2
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=R6Be0ldli2FnyTntQV7WxiIHR%2FGGL1sV3LCIAwXng70%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786784215"}],"max_age":3600}
reporting-endpoints: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=R6Be0ldli2FnyTntQV7WxiIHR%2FGGL1sV3LCIAwXng70%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786784215"}],"max_age":3600}
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 996
x-ratelimit-reset: 1786784263
age: 13719
cf-cache-status: HIT
cf-ray: a2b84c14ed768072-AMS
alt-svc: h3=":443"

{}
```

### Annotation

* **Status:** `404 Not Found` — the requested post does not exist, so the server could not find the requested resource.
* **Content-Type:** `application/json; charset=utf-8` — the response body is formatted as JSON using UTF-8.

---
thank you