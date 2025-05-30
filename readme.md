## API Testing

You can import the included Postman collection to test the API:

**File:** `New Collection.postman_collection.json`

Steps:
1. Open Postman.
2. Click "Import".
3. Select the file.
4. Use the included endpoints for login, upload, download, etc.


## Secure File Download Handling

This system enforces strict rules to ensure **only authenticated client users** can securely download files via unique, time-limited URLs.

### How It Works

1. **Secure Download URL Generation**  
   When a client user hits the `/download-file/{file_id}` endpoint, the server responds with a **secure, encrypted link** (usually containing a signed JWT token or a UUID).  
   Example:
   ```json
   {
     "download-link": "http://yourdomain.com/client/download-file/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "message": "success"
   }

### Client-Only Access Enforcement

The token embedded in the URL contains the `user_id`, `file_id`, and optionally an `exp` (expiry time).

When the download URL is accessed:

-  The token is **decoded and verified** for integrity and expiration.
-  The server checks that the **user role is `Client User`**.
-  The token’s embedded `user_id` must match the **authenticated client** making the request.

If any of these validations fail, access is denied and a `403 Forbidden` response is returned.
