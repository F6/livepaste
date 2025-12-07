#!/usr/bin/env python3
import argparse
import requests
import asyncio
import websockets
import json
import sys


def login(args):
    """Authenticate with username and password to get JWT token."""
    url = args.server.rstrip('/') + '/api/login'
    params = {'username': args.username, 'password': args.password}
    try:
        r = requests.post(url, params=params)
        r.raise_for_status()
        data = r.json()
        print('Login successful!')
        print('Token:', data['access_token'])
        print('Username:', data['username'])
        print('Expires in:', data['expires_in'], 'seconds')
    except requests.exceptions.HTTPError as e:
        print('Login failed:', e.response.status_code, e.response.text)
        sys.exit(1)


def create(args):
    url = args.server.rstrip('/') + '/api/sessions'
    params = {}
    if args.passphrase:
        params['passphrase'] = args.passphrase
    headers = {}
    if args.token:
        headers['Authorization'] = f'Bearer {args.token}'
    try:
        r = requests.post(url, params=params, headers=headers)
        r.raise_for_status()
        print('created', r.json())
    except requests.exceptions.HTTPError as e:
        print('error', e.response.status_code, e.response.text)
        sys.exit(1)


def join(args):
    url = args.server.rstrip('/') + '/api/sessions/' + args.passphrase + '/join'
    r = requests.post(url)
    if r.status_code != 200:
        print('error', r.status_code, r.text)
        sys.exit(1)
    print('joined, content:', r.json().get('content'))


async def ws_listen(server, passphrase):
    proto = 'wss' if server.startswith('https') else 'ws'
    host = server.replace('http://', '').replace('https://', '')
    uri = f"{proto}://{host}/ws/{passphrase}"
    async with websockets.connect(uri) as ws:
        print('connected to', uri)
        try:
            while True:
                msg = await ws.recv()
                print('msg:', msg)
        except Exception as e:
            print('disconnected', e)


def listen(args):
    asyncio.run(ws_listen(args.server, args.passphrase))


def send(args):
    # send via websocket if possible, otherwise fallback to polling update endpoint
    proto = 'wss' if args.server.startswith('https') else 'ws'
    host = args.server.replace('http://', '').replace('https://', '')
    uri = f"{proto}://{host}/ws/{args.passphrase}"
    async def _send_ws():
        async with websockets.connect(uri) as ws:
            await ws.send(json.dumps({"type": "update", "content": args.content}))
    try:
        asyncio.run(_send_ws())
        print('sent via websocket')
    except Exception as e:
        print('failed to send:', e)


def main():
    p = argparse.ArgumentParser(prog='livepaste-cli')
    p.add_argument('--server', default='http://localhost:8000', help='Server URL')
    p.add_argument('--token', default='', help='JWT token for authentication')
    sub = p.add_subparsers(dest='cmd')
    
    a = sub.add_parser('login')
    a.add_argument('username', help='Username')
    a.add_argument('password', help='Password')
    a.set_defaults(func=login)

    a = sub.add_parser('create')
    a.add_argument('--passphrase', help='Custom passphrase for session')
    a.set_defaults(func=create)

    a = sub.add_parser('join')
    a.add_argument('passphrase', help='Session passphrase to join')
    a.set_defaults(func=join)

    a = sub.add_parser('listen')
    a.add_argument('passphrase', help='Session passphrase to listen to')
    a.set_defaults(func=listen)

    a = sub.add_parser('send')
    a.add_argument('passphrase', help='Session passphrase to send to')
    a.add_argument('content', help='Content to send')
    a.set_defaults(func=send)

    args = p.parse_args()
    if not args.cmd:
        p.print_help(); sys.exit(1)
    args.func(args)


if __name__ == '__main__':
    main()
