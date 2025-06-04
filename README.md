# 🕵️ Honeypot

A modular Python honeypot designed to simulate **SSH** and **web login** services in order to detect, log, and analyse unauthorised access attempts. This project is ideal for learning about cyber threat behaviour, system deception, and network defence strategies.

---

## 🚀 Project Overview

This project showcases skills in:

- **Cybersecurity** – SSH and HTTP attack surface simulation.
- **Software Engineering** – Multi-threading, argument parsing, and secure logging
- **System Design** – Shell simulation, custom authentication, protocol-level emulation, credential capture, and separation of concerns across services.



---

## ⚠️ SSH RSA Key Required

The SSH honeypot uses the [Paramiko](http://www.paramiko.org/) library and requires an RSA private key for initialisation. This key is **not included** in the repository and must be set in a file named `key_files.py`, which is ignored for security reasons.

Example for `key_files.py`:

```python
import paramiko
host_key = paramiko.RSAKey(filename="path_to_your_private_key")
```

To generate a key:

```bash
ssh-keygen -t rsa -b 2048 -f my_rsa_key
```

---

## 📦 Features

- 🛡️ **SSH Honeypot** with emulated shell commands
- 🌐 **Web Honeypot** simulating a WordPress-style login page
- 🧾 **Credential Logging** for both SSH and HTTP
- 💬 **Command Logging** with IP tracking
- 🧵 **Threaded SSH Connections**
- 🛠️ **Command-Line Interface (CLI)** for full control

---

## 🧠 Usage Guide

Use the CLI to provision honeypots:

```bash
python honeypot.py -a <address> -p <port> [options]
```

### CLI Options

| Flag         | Description                                      |
|--------------|--------------------------------------------------|
| `-a`, `--address` | IP address to bind to (e.g. `127.0.0.1`)     |
| `-p`, `--port`    | Port to listen on                            |
| `--ssh`           | Run SSH honeypot                             |
| `--http`          | Run Web honeypot                             |
| `-u`, `--username`| (Optional) Required username                 |
| `-pw`, `--password`| (Optional) Required password               |

---

## 🖥️ SSH Honeypot

Launch SSH honeypot:

```bash
python honeypot.py -a 127.0.0.1 -p 2223 --ssh
```

Then connect using:

```bash
ssh -p 2223 anyuser@127.0.0.1
```

> If no `-u` and `-pw` are supplied, any username/password combination will be accepted.

### Emulated Shell Commands

| Command             | Output                      |
|---------------------|-----------------------------|
| `pwd`               | `\usr\local`                |
| `whoami`            | `corpuser`                  |
| `ls`                | `jumpbox1.conf`             |
| `cat jumpbox1.conf` | `Go to deeboodah.com`       |
| `exit`              | Ends session                |
| any other command   | Echoed back as-is           |

All activity is logged to `cmd_audits.log` and `audits.log`.

---

## 🌐 Web Honeypot

Launch Web honeypot:

```bash
python honeypot.py -a 127.0.0.1 -p 5000 --http
```

Navigate to:

```
http://127.0.0.1:5000/
```

### Behaviour

- A fake WordPress login page appears.
- All login attempts (username/password and IP) are logged to `http_audits.log` and `audits.log`.
- If no credentials are provided via CLI:
  - **Default username**: `admin`
  - **Default password**: `password`
- If login is successful, the response is simply:

```
yes
```

Otherwise, users see an "Invalid username or password" message.

---

## 📝 Log Files

| Log File           | Source         | Description                                                              |
|--------------------|----------------|--------------------------------------------------------------------------|
| `audits.log`       | SSH & HTTP     | General connection events and login attempts from both honeypots         |
| `cmd_audits.log`   | SSH            | Logs each command entered in the SSH session                             |
| `http_audits.log`  | HTTP           | Logs IP address, username, and password from web login attempts          |

### `audits.log` (Combined Log)

This file contains general connection events and login attempts for **both** honeypots.

#### Sample Entries:
```
127.0.0.1 connected to the server.
Client 127.0.0.1 attempted to connect with,  Username='username' Password='123'
2025-06-03 17:26:47,963 Client with IP address: 127.0.0.1 entered
 Username: admin, Password: password
```

#### Log Sources:
- **SSH Honeypot**:
  - IP addresses of clients that connect
  - Login attempts with username/password combinations

- **Web Honeypot**:
  - Timestamps and credentials submitted via the web login form

> 📌 This log is useful for tracking all access attempts at a high level. For detailed analysis, use the individual logs (`cmd_audits.log`, `http_audits.log`).

---

## 🧩 Skills Demonstrated

- **Cyber Deception Design** – Tricking attackers with believable services
- **Secure Event Logging** – File rotation and per-module loggers
- **Socket Programming** – Custom SSH handshake and threading
- **User Simulation** – Fake shell and web login interfaces
- **CLI Engineering** – Flexible deployment with custom arguments

---

## 🔮 Potential Improvements

- Add a web dashboard for viewing logs
- Add Telnet or SMTP honeypot modules
- Dockerise for portable deployment
- Integrate with ELK or Splunk for real-time analysis

---

## 📁 Project Structure

```
├── honeypot.py             # Main CLI entry point
├── ssh_honeypot.py         # SSH honeypot logic
├── web_honeypot.py         # Web honeypot logic
├── key_files.py            # (User-defined) RSA key for SSH
├── templates/
│   └── wp-admin.html       # Fake WordPress login page
├── cmd_audits.log          # SSH command logs
├── http_audits.log         # Web login log
├── audits.log              # Combined SSH & Web connection log
```

---
