# 🔴 SLUX FRAMEWORK

<p align="left">
  <img src="https://img.shields.io/badge/Version-1.0-red.svg" alt="Version">
  <img src="https://img.shields.io/badge/Author-slur--dev-cyan.svg" alt="Author">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python">
</p>

**SLUX FRAMEWORK** is a powerful, automated package manager and installer for 97 top-tier cybersecurity, OSINT, and penetration testing tools. It is designed with a clean, Zphisher-style UI and features automated OS detection to seamlessly work across Termux, Debian/Kali Linux, and Arch Linux.

---

## 🚀 Features
* **97 Premium Tools:** Curated list of only the most standard and effective tools (No unmaintained bloatware).
* **Automated OS Detection:** Automatically detects Termux, APT, or Pacman package managers and installs base dependencies (`git`, `python`, `golang`).
* **Conflict Handling:** If a tool is already installed, SLUX will automatically update it via `git pull`.
* **Clean UI:** Interactive Command-Line Interface with a detailed description mode (`long -l`).

---

## 🛠️ Installation & Usage

Run the following commands in your terminal to install and launch the SLUX Framework:

```bash
# Clone the repository
git clone [https://github.com/slur-dev/slux-framework.git](https://github.com/slur-dev/slux-framework.git)

# Navigate to the directory
cd slux-framework

# Run the script
python3 slux.py