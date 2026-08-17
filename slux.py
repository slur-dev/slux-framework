#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# ---------------------------------------------------------
# CONFIGURATION & GLOBAL VARIABLES
# ---------------------------------------------------------
INSTALL_DIR = os.path.expanduser("~/SLUX_TOOLS")

# Zphisher-style clean ANSI colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ---------------------------------------------------------
# TOOL DATABASE (1 - 97) with Descriptions
# ---------------------------------------------------------
TOOLS = {
    # Recon & OSINT
    1: {"name": "Amass", "url": "https://github.com/owasp-amass/amass.git", "desc": "In-depth DNS enumeration and network mapping tool."},
    2: {"name": "BBOT", "url": "https://github.com/blacklanternsecurity/bbot.git", "desc": "Recursive OSINT framework for executing automated reconnaissance."},
    3: {"name": "Maigret", "url": "https://github.com/soxoj/maigret.git", "desc": "Collects a dossier on a person by username across thousands of sites."},
    4: {"name": "GHunt", "url": "https://github.com/mxrch/GHunt.git", "desc": "Extracts information from Google accounts using just an email."},
    5: {"name": "CrossLinked", "url": "https://github.com/m8sec/CrossLinked.git", "desc": "LinkedIn enumeration tool to extract valid employee names."},
    6: {"name": "SpiderFoot", "url": "https://github.com/smicallef/spiderfoot.git", "desc": "Automates OSINT collection across multiple data sources."},
    7: {"name": "CloudEnum", "url": "https://github.com/initstring/cloud_enum.git", "desc": "Finds public cloud resources associated with a specific keyword."},
    8: {"name": "Recon-ng", "url": "https://github.com/lanmaster53/recon-ng.git", "desc": "Full-featured Web Reconnaissance framework written in Python."},
    9: {"name": "TruffleHog", "url": "https://github.com/trufflesecurity/trufflehog.git", "desc": "Searches through git repositories for high entropy strings and secrets."},
    10: {"name": "Holehe", "url": "https://github.com/megadose/holehe.git", "desc": "Checks if an email is attached to an account on various sites."},
    
    # Web App Security
    11: {"name": "Nuclei", "url": "https://github.com/projectdiscovery/nuclei.git", "desc": "Fast and customizable vulnerability scanner based on simple YAML templates."},
    12: {"name": "FFuF", "url": "https://github.com/ffuf/ffuf.git", "desc": "Fast web fuzzer written in Go for discovering hidden directories and files."},
    13: {"name": "SQLMap", "url": "https://github.com/sqlmapproject/sqlmap.git", "desc": "Automates the process of detecting and exploiting SQL injection flaws."},
    14: {"name": "Ghauri", "url": "https://github.com/r0oth3x49/ghauri.git", "desc": "Advanced cross-platform tool that automates detecting and exploiting SQL injection."},
    15: {"name": "Katana", "url": "https://github.com/projectdiscovery/katana.git", "desc": "A next-generation crawling and spidering framework for web applications."},
    16: {"name": "Kiterunner", "url": "https://github.com/assetnote/kiterunner.git", "desc": "Contextual API scanning tool for discovering hidden API endpoints."},
    17: {"name": "Dalfox", "url": "https://github.com/hahwul/dalfox.git", "desc": "Powerful utility for finding and exploiting XSS vulnerabilities."},
    18: {"name": "Commix", "url": "https://github.com/commixproject/commix.git", "desc": "Automates the detection and exploitation of command injection vulnerabilities."},
    19: {"name": "Arjun", "url": "https://github.com/s0md3v/Arjun.git", "desc": "Finds hidden HTTP parameters for web applications."},
    20: {"name": "JWT_Tool", "url": "https://github.com/ticarpi/jwt_tool.git", "desc": "Toolkit for testing, tweaking and cracking JSON Web Tokens."},
    
    # Password Cracking
    21: {"name": "Hashcat", "url": "https://github.com/hashcat/hashcat.git", "desc": "World's fastest and most advanced password recovery utility."},
    22: {"name": "John the Ripper", "url": "https://github.com/openwall/john.git", "desc": "Fast password cracker with extensive hash type support."},
    23: {"name": "Hydra", "url": "https://github.com/vanhauser-thc/thc-hydra.git", "desc": "Very fast network logon cracker supporting many different services."},
    24: {"name": "NetExec", "url": "https://github.com/Pennyw0rth/NetExec.git", "desc": "Network service exploitation tool that helps automate security assessments."},
    25: {"name": "Crowbar", "url": "https://github.com/galkan/crowbar.git", "desc": "Brute forcing tool that can be used during penetration tests."},
    26: {"name": "CeWL", "url": "https://github.com/digininja/CeWL.git", "desc": "Custom wordlist generator that spiders a given website."},
    27: {"name": "Mentalist", "url": "https://github.com/sc0tfree/mentalist.git", "desc": "Graphical tool for custom wordlist generation based on human patterns."},
    28: {"name": "Name-That-Hash", "url": "https://github.com/Ciphey/NameThatHash.git", "desc": "Automatically identifies the type of password hash you have."},
    29: {"name": "Ncrack", "url": "https://github.com/nmap/ncrack.git", "desc": "High-speed network authentication cracking tool."},
    30: {"name": "THC-pptp-bruter", "url": "https://github.com/vanhauser-thc/thc-pptp-bruter.git", "desc": "Brute-force tool specifically designed for PPTP VPN endpoints."},
    
    # Network & Infra
    31: {"name": "Nmap", "url": "https://github.com/nmap/nmap.git", "desc": "The industry standard for network exploration and security auditing."},
    32: {"name": "RustScan", "url": "https://github.com/RustScan/RustScan.git", "desc": "The modern port scanner that finds open ports incredibly fast."},
    33: {"name": "Masscan", "url": "https://github.com/robertdavidgraham/masscan.git", "desc": "The fastest Internet port scanner designed to scan the entire web in minutes."},
    34: {"name": "Naabu", "url": "https://github.com/projectdiscovery/naabu.git", "desc": "A fast port scanner written in Go that focuses on reliability and simplicity."},
    35: {"name": "Impacket", "url": "https://github.com/fortra/impacket.git", "desc": "A collection of Python classes for working with network protocols."},
    36: {"name": "Responder", "url": "https://github.com/lgandx/Responder.git", "desc": "LLMNR, NBT-NS and MDNS poisoner with built-in rogue authentication servers."},
    37: {"name": "Bettercap", "url": "https://github.com/bettercap/bettercap.git", "desc": "The Swiss Army knife for WiFi, Bluetooth Low Energy, and Ethernet networks."},
    38: {"name": "ZMap", "url": "https://github.com/zmap/zmap.git", "desc": "A fast single-packet network scanner designed for Internet-wide network surveys."},
    39: {"name": "Sliver", "url": "https://github.com/BishopFox/sliver.git", "desc": "An open source cross-platform adversary emulation and C2 framework."},
    40: {"name": "BloodHound.py", "url": "https://github.com/dirkjanm/BloodHound.py.git", "desc": "Python-based ingestor for BloodHound to map Active Directory environments."},
    
    # Wi-Fi & Radio
    41: {"name": "Aircrack-ng", "url": "https://github.com/aircrack-ng/aircrack-ng.git", "desc": "Complete suite of tools to assess WiFi network security."},
    42: {"name": "HCXTools", "url": "https://github.com/ZerBea/hcxtools.git", "desc": "Portable set of tools for capturing wlan traffic and converting it for hashcat."},
    43: {"name": "Wifite2", "url": "https://github.com/derv82/wifite2.git", "desc": "Automated wireless attack tool for auditing WEP, WPA, and WPS encrypted networks."},
    44: {"name": "EAPHammer", "url": "https://github.com/s0lst1c3/eaphammer.git", "desc": "Tool for performing targeted evil twin attacks against WPA2-Enterprise networks."},
    45: {"name": "Airgeddon", "url": "https://github.com/v1s1t0r1sh3r3/airgeddon.git", "desc": "Multi-use bash script for wireless networks auditing."},
    46: {"name": "Kismet", "url": "https://github.com/kismetwireless/kismet.git", "desc": "Wireless network and device detector, sniffer, and intrusion detection system."},
    47: {"name": "Reaver", "url": "https://github.com/t6x/reaver-wps-fork-t6x.git", "desc": "Brute force attack tool against WiFi Protected Setup (WPS) registrar PINs."},
    
    # Post-Exploitation
    48: {"name": "Metasploit", "url": "https://github.com/rapid7/metasploit-framework.git", "desc": "The world's most used penetration testing framework."},
    49: {"name": "PEASS-ng", "url": "https://github.com/peass-ng/PEASS-ng.git", "desc": "Privilege escalation tools for Windows and Linux/Unix and macOS."},
    50: {"name": "Ligolo-ng", "url": "https://github.com/nicocha30/ligolo-ng.git", "desc": "Advanced tunneling and pivoting tool that uses a TUN interface."},
    
    # Phishing & SocEng
    51: {"name": "Evilginx2", "url": "https://github.com/kgretzky/evilginx2.git", "desc": "Standalone man-in-the-middle attack framework used for phishing login credentials."},
    52: {"name": "GoPhish", "url": "https://github.com/gophish/gophish.git", "desc": "Open-source phishing toolkit designed for businesses and penetration testers."},
    53: {"name": "SET", "url": "https://github.com/trustedsec/social-engineer-toolkit.git", "desc": "The Social-Engineer Toolkit is an open-source framework designed for social engineering."},
    54: {"name": "Zphisher", "url": "https://github.com/htr-tech/zphisher.git", "desc": "Automated phishing tool with multiple templates for various popular websites."},
    55: {"name": "PyPhisher", "url": "https://github.com/KasRoudra/PyPhisher.git", "desc": "Easy to use phishing tool with multiple webpage templates."},
    
    # Mobile Pentesting
    56: {"name": "Frida", "url": "https://github.com/frida/frida.git", "desc": "Dynamic instrumentation toolkit for developers, reverse-engineers, and researchers."},
    57: {"name": "Objection", "url": "https://github.com/sensepost/objection.git", "desc": "Runtime mobile exploration toolkit powered by Frida."},
    58: {"name": "MobSF", "url": "https://github.com/MobSF/Mobile-Security-Framework-MobSF.git", "desc": "Automated, all-in-one mobile application pentesting framework."},
    59: {"name": "Apktool", "url": "https://github.com/iBotPeaches/Apktool.git", "desc": "A tool for reverse engineering 3rd party, closed, binary Android apps."},
    
    # Cloud & Containers
    60: {"name": "Pacu", "url": "https://github.com/RhinoSecurityLabs/pacu.git", "desc": "The AWS exploitation framework designed for testing the security of cloud environments."},
    61: {"name": "ScoutSuite", "url": "https://github.com/nccgroup/ScoutSuite.git", "desc": "Multi-cloud security-auditing tool to assess security posture of cloud environments."},
    62: {"name": "Trivy", "url": "https://github.com/aquasecurity/trivy.git", "desc": "Comprehensive and versatile security scanner for containers and other artifacts."},
    
    # Advanced Web Attacks
    63: {"name": "XSStrike", "url": "https://github.com/s0md3v/XSStrike.git", "desc": "Advanced XSS detection suite equipped with four hand-written parsers."},
    64: {"name": "SSRFmap", "url": "https://github.com/swisskyrepo/SSRFmap.git", "desc": "Automatic SSRF fuzzer and exploitation tool."},
    65: {"name": "GraphQLmap", "url": "https://github.com/swisskyrepo/GraphQLmap.git", "desc": "A scripting engine to interact with a graphql endpoint for pentesting purposes."},
    66: {"name": "LFISuite", "url": "https://github.com/D35m0nd142/LFISuite.git", "desc": "Totally automatic tool able to discover and exploit Local File Inclusion vulnerabilities."},
    
    # C2 & Reversing
    67: {"name": "Mythic", "url": "https://github.com/its-a-feature/Mythic.git", "desc": "A collaborative, multi-platform, red teaming command and control framework."},
    68: {"name": "Covenant", "url": "https://github.com/cobbr/Covenant.git", "desc": "A collaborative .NET C2 framework for red teamers."},
    69: {"name": "Ghidra", "url": "https://github.com/NationalSecurityAgency/ghidra.git", "desc": "A software reverse engineering framework created and maintained by the NSA."},
    70: {"name": "Ropper", "url": "https://github.com/sashs/Ropper.git", "desc": "Discover ROP gadgets in executable files and build ROP chains."},
    
    # OPSEC & Anonymity
    71: {"name": "Tor", "url": "https://gitlab.torproject.org/tpo/core/tor.git", "desc": "Free software and open network that helps defend against traffic analysis."},
    72: {"name": "Proxychains-ng", "url": "https://github.com/rofl0r/proxychains-ng.git", "desc": "Forces any tcp connection made by any given application to follow through proxy."},
    73: {"name": "AnonSurf", "url": "https://github.com/Und3rf10w/kali-anonsurf.git", "desc": "Script to route all OS traffic through TOR for anonymity."},
    74: {"name": "TorGhost", "url": "https://github.com/SusmithKrishnan/torghost.git", "desc": "A script that redirects all internet traffic through the SOCKS5 tor proxy."},
    75: {"name": "Nipe", "url": "https://github.com/htrgouvea/nipe.git", "desc": "Script to make Tor Network your default gateway."},
    76: {"name": "Macchanger", "url": "https://github.com/alobbs/macchanger.git", "desc": "A utility for viewing and manipulating the MAC address of network interfaces."},
    77: {"name": "Kalitorify", "url": "https://github.com/brainfucksec/kalitorify.git", "desc": "Transparent proxy through Tor for Kali Linux OS."},
    78: {"name": "ProxyBroker", "url": "https://github.com/constverum/ProxyBroker.git", "desc": "An open source tool that asynchronously finds public proxies and checks them."},
    79: {"name": "I2P", "url": "https://github.com/i2p/i2p.i2p.git", "desc": "An anonymous overlay network intended to protect communication from surveillance."},
    80: {"name": "Privoxy", "url": "https://www.privoxy.org/git/privoxy.git", "desc": "A non-caching web proxy with advanced filtering capabilities for enhancing privacy."},
    
    # Network Sniffing
    81: {"name": "Wireshark", "url": "https://gitlab.com/wireshark/wireshark.git", "desc": "The world's foremost and widely-used network protocol analyzer."},
    82: {"name": "Tshark", "url": "https://gitlab.com/wireshark/wireshark.git", "desc": "A network protocol analyzer that lets you capture packet data from a live network."},
    83: {"name": "Mitmproxy", "url": "https://github.com/mitmproxy/mitmproxy.git", "desc": "An interactive TLS-capable intercepting HTTP proxy for penetration testers."},
    84: {"name": "Zeek", "url": "https://github.com/zeek/zeek.git", "desc": "A powerful network analysis framework that focuses on security monitoring."},
    85: {"name": "Tcpdump", "url": "https://github.com/the-tcpdump-group/tcpdump.git", "desc": "A powerful command-line packet analyzer."},
    86: {"name": "Ngrep", "url": "https://github.com/jpr5/ngrep.git", "desc": "Strives to provide most of GNU grep's common features, applying them to the network layer."},
    87: {"name": "Suricata", "url": "https://github.com/OISF/suricata.git", "desc": "A free and open source, mature, fast and robust network threat detection engine."},
    88: {"name": "Maltrail", "url": "https://github.com/stamparm/maltrail.git", "desc": "A malicious traffic detection system."},
    89: {"name": "Net-Creds", "url": "https://github.com/DanMcInerney/net-creds.git", "desc": "Sniffs sensitive data from an interface or pcap."},
    90: {"name": "Arkime", "url": "https://github.com/arkime/arkime.git", "desc": "A large scale, open source, indexed packet capture and search tool."},
    
    # Masterpieces
    91: {"name": "Mimikatz", "url": "https://github.com/gentilkiwi/mimikatz.git", "desc": "Tool used to extract plaintexts passwords, hash, PIN code and kerberos tickets from memory."},
    92: {"name": "Havoc C2", "url": "https://github.com/HavocFramework/Havoc.git", "desc": "A modern and malleable post-exploitation command and control framework."},
    93: {"name": "Empire", "url": "https://github.com/BC-SECURITY/Empire.git", "desc": "A post-exploitation framework that includes a pure-PowerShell2.0 Windows agent."},
    94: {"name": "Xray", "url": "https://github.com/chaitin/xray.git", "desc": "A powerful security assessment tool for Web security."},
    95: {"name": "Radare2", "url": "https://github.com/radareorg/radare2.git", "desc": "A free/libre toolchain for easing tasks like software reverse engineering."},
    96: {"name": "YARA", "url": "https://github.com/VirusTotal/yara.git", "desc": "The pattern matching swiss knife for malware researchers."},
    97: {"name": "Autopsy", "url": "https://github.com/sleuthkit/autopsy.git", "desc": "A digital forensics platform and graphical interface to other digital forensics tools."}
}

# ---------------------------------------------------------
# BANNERS & CORE FUNCTIONS
# ---------------------------------------------------------

BANNER = r"""
  ____  _     _   _  __  __   _____ ____      _    __  __ _______        _____  ____  _  __
 / ___|| |   | | | | \ \/ /  |  ___|  _ \    / \  |  \/  | ____\ \      / / _ \|  _ \| |/ /
 \___ \| |   | | | |  \  /   | |_  | |_) |  / _ \ | |\/| |  _|  \ \ /\ / / | | | |_) | ' / 
  ___) | |___| |_| |  /  \   |  _| |  _ <  / ___ \| |  | | |___  \ V  V /| |_| |  _ <| . \ 
 |____/|_____|\___/  /_/\_\  |_|   |_| \_\/_/   \_\_|  |_|_____|  \_/\_/  \___/|_| \_\_|\_\
"""

def display_banner():
    print(f"{RED}{BANNER}")
    print(f"{CYAN}-------------------------------------------------------------------------")
    print(f"{GREEN}              Created by : {WHITE}slur-dev {CYAN}(github.com/slur-dev)     ")
    print(f"{CYAN}-------------------------------------------------------------------------{RESET}")

def show_disclaimer():
    disclaimer = f"""{RED}
======================================================================
                         LEGAL DISCLAIMER
======================================================================
{WHITE}1. OWNERSHIP:{RESET} The SLUX Framework is strictly an automation wrapper 
designed to simplify the installation of various open-source 
cybersecurity tools. I do not own, maintain, or claim credit for 
any of the 97 tools included in this script. All credits and rights 
belong to their respective original developers.

{WHITE}2. USAGE:{RESET} This script and the tools it installs are provided for 
educational purposes and authorized security testing only. 

{WHITE}3. LIABILITY:{RESET} The creator of SLUX holds no responsibility for any 
damage, legal issues, or misuse caused by the user. 
{RED}======================================================================{RESET}
"""
    print(disclaimer)
    while True:
        agree = input(f"{YELLOW}[?] Do you agree to these terms? (y/n): {RESET}").strip().lower()
        if agree == 'y':
            print(f"\n{GREEN}[+] Terms accepted. Starting SLUX FRAMEWORK...\n{RESET}")
            break
        elif agree == 'n':
            print(f"\n{RED}[-] You must agree to the terms to use this tool. Exiting.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[-] Invalid input. Please type 'y' or 'n'.{RESET}")

def detect_os_and_install_deps():
    print(f"{CYAN}[*] Detecting Operating System and Package Manager...{RESET}")
    pkg_manager = None
    update_cmd = []
    install_cmd = []

    if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
        print(f"{GREEN}[+] Termux detected.{RESET}")
        pkg_manager = "pkg"
        update_cmd = ["pkg", "update", "-y"]
        install_cmd = ["pkg", "install", "-y", "git", "python", "golang"]
    elif shutil.which("apt"):
        print(f"{GREEN}[+] Debian/Kali Linux detected.{RESET}")
        pkg_manager = "apt"
        update_cmd = ["sudo", "apt", "update", "-y"]
        install_cmd = ["sudo", "apt", "install", "-y", "git", "python3", "python3-pip", "golang"]
    elif shutil.which("pacman"):
        print(f"{GREEN}[+] Arch Linux detected.{RESET}")
        pkg_manager = "pacman"
        update_cmd = ["sudo", "pacman", "-Sy"]
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm", "git", "python", "python-pip", "go"]
    else:
        print(f"{RED}[-] Could not determine compatible package manager. Ensure git, python, and go are installed.{RESET}")
        return

    try:
        print(f"{CYAN}[*] Updating repositories using {pkg_manager}...{RESET}")
        subprocess.run(update_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{CYAN}[*] Installing base dependencies (git, python, golang)...{RESET}")
        subprocess.run(install_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{GREEN}[+] Base dependencies installed successfully.\n{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}[-] Error installing dependencies: {e}{RESET}")

def prepare_directory():
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)
        print(f"{GREEN}[+] Created tools directory at: {WHITE}{INSTALL_DIR}{RESET}")
    else:
        print(f"{CYAN}[*] Tools directory verified: {WHITE}{INSTALL_DIR}{RESET}")

def install_tool(tool_id):
    if tool_id not in TOOLS:
        print(f"{RED}[-] Invalid tool number selected.{RESET}")
        return

    tool = TOOLS[tool_id]
    tool_name = tool["name"]
    tool_url = tool["url"]
    
    print(f"\n{CYAN}[*] Selected: {WHITE}{tool_name}{RESET}")
    target_path = os.path.join(INSTALL_DIR, tool_name.replace(" ", "_").lower())

    if os.path.exists(target_path):
        print(f"{CYAN}[*] Directory {WHITE}{target_path}{CYAN} already exists. Attempting to pull latest changes...{RESET}")
        try:
            subprocess.run(["git", "-C", target_path, "pull"], check=True)
            print(f"{GREEN}[+] {WHITE}{tool_name}{GREEN} successfully updated.{RESET}")
        except subprocess.CalledProcessError:
            print(f"{RED}[-] Failed to update {tool_name}. You may need to resolve git conflicts manually.{RESET}")
    else:
        print(f"{CYAN}[*] Cloning {WHITE}{tool_url}{CYAN} into {WHITE}{target_path}{CYAN}...{RESET}")
        try:
            subprocess.run(["git", "clone", tool_url, target_path], check=True)
            print(f"{GREEN}[+] {WHITE}{tool_name}{GREEN} successfully installed.{RESET}")
        except subprocess.CalledProcessError:
            print(f"{RED}[-] Failed to clone {tool_name}. Verify the URL or your internet connection.{RESET}")

def display_short_menu():
    print(f"\n{CYAN}=" * 80)
    print(f"{YELLOW}                        AVAILABLE TOOLS LIST                    ")
    print(f"{CYAN}={RESET}" * 80)
    
    col_width = 30
    keys = list(TOOLS.keys())
    for i in range(0, len(keys), 3):
        row = ""
        for j in range(3):
            if i + j < len(keys):
                tid = keys[i+j]
                name = TOOLS[tid]["name"]
                row += f"{GREEN}[{WHITE}{tid:02}{GREEN}]{WHITE} {name}".ljust(col_width + 15)
        print(row)
    print(f"{CYAN}={RESET}" * 80)

def display_long_menu():
    print(f"\n{CYAN}=" * 95)
    print(f"{YELLOW}                          DETAILED TOOLS LIST (LONG VIEW)             ")
    print(f"{CYAN}={RESET}" * 95)
    
    for tid, data in TOOLS.items():
        name = data["name"]
        desc = data["desc"]
        print(f"{GREEN}[{WHITE}{tid:02}{GREEN}]{WHITE} {name.ljust(18)} {CYAN}- {WHITE}{desc}")
        
    print(f"{CYAN}={RESET}" * 95)

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        show_disclaimer()
        detect_os_and_install_deps()
        prepare_directory()
        
        show_long = False
        
        while True:
            if show_long:
                display_long_menu()
                show_long = False  # Reset back to short menu for next iteration
            else:
                display_short_menu()
                
            print(f"\n{CYAN}[*]{WHITE} Type the number of the tool to install (1-97).")
            print(f"{CYAN}[*]{WHITE} Type {YELLOW}'long -l'{WHITE} to see the detailed list with descriptions.")
            print(f"{CYAN}[*]{WHITE} Type {GREEN}'all'{WHITE} to install everything ({RED}WARNING: Requires significant disk space{WHITE}).")
            print(f"{CYAN}[*]{WHITE} Type {RED}'exit'{WHITE} to quit.")
            
            choice = input(f"\n{RED}SLUX {WHITE}> {GREEN}").strip().lower()
            print(f"{RESET}", end="")
            
            if choice == 'exit' or choice == 'quit':
                print(f"{CYAN}[*] Exiting SLUX FRAMEWORK. Goodbye.{RESET}")
                sys.exit(0)
            elif choice == 'long -l':
                show_long = True
                os.system('cls' if os.name == 'nt' else 'clear')
                display_banner()
                continue
            elif choice == 'all':
                print(f"{YELLOW}[*] Beginning bulk installation of all 97 tools...{RESET}")
                for t_id in TOOLS.keys():
                    install_tool(t_id)
                print(f"{GREEN}[+] Bulk installation complete.{RESET}")
            elif choice.isdigit():
                num = int(choice)
                if 1 <= num <= 97:
                    install_tool(num)
                else:
                    print(f"{RED}[-] Number out of range. Please select between 1 and 97.{RESET}")
            else:
                print(f"{RED}[-] Invalid input. Please enter a valid number or command.{RESET}")
                
            input(f"\n{YELLOW}[?] Press Enter to continue...{RESET}")
            os.system('cls' if os.name == 'nt' else 'clear')
            display_banner()

    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Installation interrupted by user. Exiting gracefully.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()