# livepaste CLI

Python command-line interface for interacting with livepaste sessions.

## Installation

1. Install dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. On Linux/macOS:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Authentication

The CLI uses JWT-based authentication. You must first login with your username and password.

### Login
```powershell
python cli.py login <username> <password>
```

Example:
```powershell
python cli.py login admin mypassword123
```

Output:
```
Login successful!
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Username: admin
Expires in: 86400 seconds
```

Save the token for use with other commands.

## Commands

### Create Session

Create a new livepaste session (requires authentication token):

```powershell
python cli.py --token <jwt_token> create [--passphrase custom-phrase]
```

Examples:
```powershell
# Auto-generate passphrase
python cli.py --token <jwt_token> create

# Custom passphrase
python cli.py --token <jwt_token> create --passphrase myroom
```

### Join Session

Join an existing session (no authentication required):

```powershell
python cli.py join <passphrase>
```

Example:
```powershell
python cli.py join myroom
```

Output:
```
joined, content: Hello from other users
```

### Listen to Session

Listen for real-time updates from a session via WebSocket:

```powershell
python cli.py listen <passphrase>
```

Example:
```powershell
python cli.py listen myroom
```

This will display any updates (text, images, files) sent to the session in real-time.

### Send Updates

Send text updates to a session via WebSocket:

```powershell
python cli.py send <passphrase> "<content>"
```

Example:
```powershell
python cli.py send myroom "Hello from CLI!"
```

## Global Options

- `--server <url>`: Specify backend server URL (default: http://localhost:8000)
- `--token <jwt_token>`: JWT authentication token for commands requiring authorization

## Typical Workflow

```powershell
# Step 1: Login to get JWT token
python cli.py login admin password123
# Copy the token from output

# Step 2: Create a session
python cli.py --token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... create --passphrase myroom
# Output: created {'passphrase': 'myroom'}

# Step 3 (Terminal 1): Listen for updates
python cli.py listen myroom

# Step 4 (Terminal 2): Send updates
python cli.py send myroom "Hello from CLI"

# Step 5 (Terminal 3): Join and view content
python cli.py join myroom
```

## Environment

By default, the CLI connects to `http://localhost:8000`. To connect to a different server:

```powershell
python cli.py --server http://example.com:8000 login admin password123
python cli.py --server http://example.com:8000 --token <token> create
```

## Troubleshooting

- **"Login failed: 401"** - Invalid username or password
- **"error 404"** - Session not found
- **"failed to send"** - WebSocket connection failed; ensure the server is running
- **"missing authorization"** - Token required but not provided; use `--token` option
