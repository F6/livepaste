# livepaste

Synchronized online clipboard solution, quickly transfer text, image and file across devices with web browser / cli tool.

## Features

The app basically works like an online temporary co-op document.
A centralized backend server manages all sessions and handles object storage.
The user connects to the server with a web app or a command line interface.

Once connected, the user can opt to log-in to the server.
To access a clipboard, the user can now create a new clipboard session or join an existing session.
To prevent misuse, log-in is required to create new clipboard session, while anonymous users can only join existing session.
If creating a new session, the server will require the user to create a passphrase for the session, or the server can generate one for the user.
Other users / devices will be able to connect to the session using the passphrase as identifier.

After joining a session, all client clipboard content will keep synchronized with the server.
The synchronization status is shown real-time in the user interface.

All users who have access to a clipboard session can choose to end current session.
Upon session end, all users connected to the session is disconnected and the clipboard content is emptied.

If all users disconnects from a session, the session keeps alive for a week, 
and upon expiration, the content in the session is also cleared.

## Backend

The backend is constructed with FastAPI.
Log-in is managed with OAuth token.
For each clipboard session, a corresponding WebSocket session is established for the user.
If the user environment does not allow websocket connection, then a polling API is available as fall-back.

Since the application is intended to be used as a light-weight small-scale self-deployed project, 
for maximum flexibility, all data is stored simply in memory, and is persisted by serializing into JSON periodically and saved to the disk.

For image and file storage, the application supports local disk directory / generic OSS.

## Web Frontend

The frontend web UI is constructed with vue and tailwindcss.
The 

## Command Line Interface

The CLI is a simple Python 3 script.

