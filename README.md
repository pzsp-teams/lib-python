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

### 1. Configuration

Create a `.env` in your project with your Azure AD credentials:

```ini
CLIENT_ID=your-client-id-uuid
TENANT_ID=your-tenant-id-uuid
EMAIL=user@example.com
SCOPES=User.Read,Team.ReadBasic.All,Channel.ReadBasic.All
AUTH_METHOD=DEVICE_CODE [or INTERACTIVE]
```

Scopes needed by all functions could be found in [.env.template](https://github.com/pzsp-teams/lib-python/tree/main/.env.template).

### 2. Basic usage

Here is a minimal example showing how to initialize the client and list joined teams:

```python
from teams_lib_pzsp2_z1.client import TeamsClient
from teams_lib_pzsp2_z1.config import CacheMode

def main():
    # Initialize the client.
    # This spawns the Go subprocess and performs authentication.
    client = TeamsClient()

    try:
        print("Fetching teams...")
        teams = client.teams.list_my_joined()

        for team in teams:
            print(f"Team: {team.display_name} | ID: {team.id}")

            # Example: List channels in the first team
            channels = client.channels.list_channels(team.id)
            print(f"  -> Found {len(channels)} channels.")

    except RuntimeError as e:
        print(f"An error occurred: {e}")

    finally:
        # Crucial: Close the client to ensure background cache writes finish
        # and the Go subprocess is terminated gracefully.
        client.close()

if __name__ == "__main__":
    main()
```

## 📚 Documentation

Full API reference, architecture details, and configuration guides are available here:

👉 [Read the Documentation](https://pzsp-teams.github.io/lib-python/)

## Authentication

The library loads credentials from environment variables. Ensure your Azure App Registration has the necessary **API Permissions** (e.g., `Team.ReadBasic.All`, `Channel.ReadBasic.All`) granted in the Azure Portal.

Supported Authentication Methods (`AUTH_METHOD`):

- **INTERACTIVE**: Opens a browser window automatically.

- **DEVICE_CODE**: Prints a code to the console to login via microsoft.com/devicelogin.

## Cache & Lifecycle

If caching is enabled (SYNC or ASYNC), the Go backend stores metadata locally (e.g., `teams_cache.json`) to speed up reference resolution.

⚠️ Important: client.close()
Because the Go backend might be running background goroutines (especially for Async Cache), you **must** call `client.close()` before your script exits. This ensures:

1. Pending cache writes are flushed to disk.

2. The Go subprocess is terminated correctly.

```python
client.close()
```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/pzsp-teams/lib-python/blob/main/LICENSE) file for details.
