import jwt
import frappe, hashlib, secrets, requests
from datetime import datetime, timedelta
from urllib.parse import urlencode

CONF = frappe.get_conf()
CLIENT_ID = CONF.get("google_client_id")
CLIENT_SECRET = CONF.get("google_client_secret")
AUTH_URI = CONF.get("google_auth_uri", "https://accounts.google.com/o/oauth2/auth")
TOKEN_URI = CONF.get("googel_token_uri", "https://oauth2.googleapis.com/token")
SECRET = CONF.get("jwt_secret")
ALGO = CONF.get("jwt_algorithm", "HS256")
ACCESS_EXPIRES = CONF.get("access_token_expires_seconds", 900)
REFRESH_DAYS = CONF.get("refresh_token_expires_days", 30)

def _hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

# Signup endpoint
@frappe.whitelist(methods=["POST"], allow_guest=True)
def signup_user(first_name, last_name, email, phone, password):
    if frappe.db.exists("User", email):
        return {"error": "User already exists"}
    
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "enabled": 1,
        "new_password": password,
        "role_profile_name": "Library Member"
    })
    user.insert(ignore_permissions=True)

    library_member = frappe.get_doc({
        "doctype": "Library Member",
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email,
        "phone": phone
    })
    library_member.insert(ignore_permissions=True)

    frappe.db.commit()
    return {"success": True}


# Login endpoint
@frappe.whitelist(methods=["POST"], allow_guest=True)
def login(email, password):
    '''
    get_value(doctype, filters, fieldname) / get_value(doctype, name, fieldname)
    Returns list
    '''
    users = frappe.db.get_values("User", {"email": email, "enabled": 1}, ["name"], as_dict=True)

    # frappe.log_error("Login function called")
    frappe.log_error(f"Login function called: {users}")

    if not users:
        frappe.throw("Invalid credentials", frappe.AuthenticationError)

    user = users[0]
    username = user['name']
    
    '''
    check_password() Validate username/email and password combination.
    Returns True or False
    '''
    try:
        ok = frappe.auth.LoginManager().check_password(username, password)
        if not ok:
            frappe.log_error(f"Invalid credentials for user: {username}")
            frappe.throw("Invalid Credentials", frappe.AuthenticationError)
    except Exception as e:
        frappe.log_error(f"Error during password validation: {e}")
        frappe.throw("Invalid Credentials", frappe.AuthenticationError)

    # Create JWT
    now = datetime.now()

    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ACCESS_EXPIRES)).timestamp()),
        "typ": "access"
    }
    access_token = jwt.encode(payload, SECRET, algorithm=ALGO)

    # Create refresh token 
    raw_refresh = secrets.token_urlsafe(48)
    hashed = _hash_token(raw_refresh)
    expires_at = now + timedelta(days=REFRESH_DAYS)

    rt = frappe.get_doc({
        "doctype": "Refresh Token",
        "user": username,
        "refresh_token": hashed,
        "expires_at": expires_at
        })
    rt.insert(ignore_permissions=True)

    frappe.db.commit()

    frappe.log_error(f"User {username} logged in successfully")
    print(access_token)
    return {
        "access_token": access_token,
        "expires_in": ACCESS_EXPIRES,
        "refresh_token": raw_refresh,
    }

# refresh endpoint
@frappe.whitelist(methods=["POST"], allow_guest=True)
def refresh(refresh_token):

    if not refresh_token:
        frappe.throw("Missing refresh_token", frappe.AuthenticationError)


    now = datetime.now()
    hashed = _hash_token(refresh_token)

    frappe.log_error(f"Hashed token: {hashed}")

    try:
        row = frappe.get_all(
            "Refresh Token",
            filters={"refresh_token": hashed, "expires_at": [">", now]},
            fields=["user"],
            limit=1
        )
    except Exception as e:
        frappe.log_error(f"Error querying refresh token: {e}")
        frappe.throw("Internal server error", frappe.AuthenticationError)

    if not row:
        frappe.log_error("Invalid or expired refresh token")
        frappe.throw("Invalid or expired refresh token", frappe.AuthenticationError)

    user = row[0].user

    # Issue new access token
    payload = {
        "sub": user,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ACCESS_EXPIRES)).timestamp()),
        "typ": "access"
    }
    try:
        access_token = jwt.encode(payload, SECRET, algorithm=ALGO)
    except Exception as e:
        frappe.log_error(f"Error encoding access token: {e}")
        frappe.throw("Internal server error", frappe.AuthenticationError)

    frappe.log_error(f"New access token issued for user: {user}")
    return {
        "access_token": access_token,
        "expires_in": ACCESS_EXPIRES,
    }

# JWT auth helper
def require_auth(fn):
    def wrapper(*args, **kwargs):
        # Remove 'cmd' from kwargs as it's not needed by the actual function
        kwargs.pop('cmd', None)

        # Look for your custom header instead of Authorization
        token = frappe.local.request.headers.get("XAuthToken") or ""
        frappe.logger().info(f"XAuthToken header: {token}")

        if not token:
            frappe.throw("Missing XAuthToken header", frappe.AuthenticationError)

        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGO])
            frappe.set_user(payload['sub'])
            frappe.log_error(f"Decoded payload: {payload}")
        except jwt.ExpiredSignatureError:
            frappe.throw("Token expired", frappe.AuthenticationError)
        except Exception as e:
            frappe.log_error(f"Token validation error: {e}")
            frappe.throw("Invalid token", frappe.AuthenticationError)

        # Set Frappe's current user for the request
        frappe.local.user = payload["sub"]
        frappe.set_user(payload["sub"])

        return fn(*args, **kwargs)

    return wrapper

# Google Oauth2 login
@frappe.whitelist(allow_guest=True)
def google_oauth_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "http://localhost:8080/api/method/library_management.auth.google_oauth_callback/",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{AUTH_URI}?{urlencode(params)}"
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = url


@frappe.whitelist(allow_guest=True)
def google_oauth_callback(code=None):
    try:
        # Validate code parameter
        if not code:
            frappe.throw("Authorization code not provided")
        
        # Exchange code for tokens
        token_res = requests.post(
            TOKEN_URI,
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8080/api/method/library_management.auth.google_oauth_callback/"
            }
        )
        
        token_res.raise_for_status()  # Raise error for bad status codes
        token_data = token_res.json()
        
        access_token = token_data.get("access_token")
        if not access_token:
            frappe.throw("Failed to get access token from Google")
        
        # Get user info
        user_res = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        user_res.raise_for_status()
        user_data = user_res.json()
        
        email = user_data.get("email")
        full_name = user_data.get("name", "")
        google_id = user_data.get("id", "")
        
        if not email:
            frappe.throw("Email not provided by Google")
        
        # Check if user exists
        user = frappe.db.get_value("User", {"email": email})
        
        if not user:
            # Create new user
            first_name, last_name = (full_name.split(" ", 1) + [""])[:2]
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "enabled": 1,
                "role_profile_name": "Library Member",
                "google_oauth_id": google_id,
                "send_welcome_email": 0  # Don't send welcome email
            })
            user_doc.flags.ignore_password_policy = True
            user_doc.insert(ignore_permissions=True)
            
            library_member = frappe.get_doc({
                "doctype": "Library Member",
                "first_name": first_name,
                "last_name": last_name,
                "email_address": email
            })
            library_member.insert(ignore_permissions=True)
            user = email
        
        # Login the user
        frappe.local.login_manager.login_as(user)
        frappe.local.login_manager.post_login()
        
        frappe.db.commit()
        
        # Redirect to frontend
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/frontend"
        
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"Google OAuth Error: {str(e)}")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/frontend?error=oauth_failed"
        
    except Exception as e:
        frappe.log_error(f"OAuth Callback Error: {str(e)}")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/frontend?error=login_failed"