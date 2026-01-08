# Teams API Python Wrapper

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-online-green)](https://pzsp-teams.github.io/lib-python/)

<br>

A high-performance **Python wrapper** for the Microsoft Teams Graph API. It leverages a compiled **Go (Golang)** backend to handle heavy lifting, concurrency, and caching, while providing a clean, fully typed Pythonic interface.

## 🚀 Key Features

- **Performance of Go**: Uses a compiled Go subprocess for efficient API communication and state management.
- **Pythonic Interface**: Fully typed using `dataclasses` and `Enums`. Native support for IDE autocompletion and type checkers (`mypy`).
- **Intelligent Cache**: Background caching of Team/Channel IDs to minimize API throttling and latency (handled transparently by the backend).
- **Simplified Auth**: Wraps MSAL authentication flows configuration.

## 📦 Installation

```bash
pip install teams-lib-pzsp2-z1
```

## 🛠️ Architecture
This library acts as a bridge. When initialized, it spawns a dedicated Go subprocess (`teamsClientLib`) and communicates via JSON-RPC over `stdin`/`stdout`.

The `TeamsClient` aggregates domain-specific services:

- **client.teams**: Manage team lifecycles (create, list, delete).

- **client.channels**: Manage standard and private channels.

- **client.chats**: Handle messages, mentions, and chat participants.

## 💻 Quick Start