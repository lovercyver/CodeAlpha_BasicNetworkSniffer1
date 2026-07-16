#!/usr/bin/env python3
"""
Advanced Network Port Scanner
Developed By: Siraj Aldula

Features:
- TCP Port Scanning
- Multi-threading
- Service Detection
- Report Generation
- Open Port Identification

Usage:
python3 scanner.py <target> [start_port] [end_port]
"""

import socket
import threading
import sys
import time
from datetime import datetime


# Configuration
MAX_THREADS = 100
TIMEOUT = 1

open_ports = []
lock = threading.Lock()


# Common service database
SERVICES = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy"
}


# Scan individual port
def scan_port(target_ip, port):

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.settimeout(TIMEOUT)

            result = sock.connect_ex((target_ip, port))


            if result == 0:

                service = SERVICES.get(
                    port,
                    "Unknown"
                )

                with lock:

                    open_ports.append(
                        {
                            "port": port,
                            "service": service
                        }
                    )


    except Exception:
        pass



# Save scan report
def save_results(target, target_ip, start_port, end_port, elapsed):

    filename = "scan_results.txt"


    with open(filename, "w") as report:


        report.write("=" * 60 + "\n")
        report.write("NETWORK PORT SCANNER REPORT\n")
        report.write("=" * 60 + "\n\n")


        report.write(
            "Developed By: Siraj Aldula\n\n"
        )


        report.write(
            f"Target Host : {target}\n"
        )

        report.write(
            f"IP Address  : {target_ip}\n"
        )

        report.write(
            f"Port Range  : {start_port}-{end_port}\n"
        )

        report.write(
            f"Scan Time   : {elapsed:.2f} seconds\n"
        )

        report.write(
            f"Date        : {datetime.now()}\n\n"
        )


        report.write("-" * 60 + "\n")


        if open_ports:


            report.write(
                "OPEN PORTS\n"
            )

            report.write(
                "-" * 60 + "\n"
            )


            for item in sorted(open_ports, key=lambda x: x["port"]):

                report.write(
                    f"Port {item['port']} : OPEN "
                    f"({item['service']})\n"
                )


        else:

            report.write(
                "No open ports found.\n"
            )


        report.write("\n")
        report.write("=" * 60)



    print(
        "\n[+] Report saved as scan_results.txt"
    )




# Main function
def main():


    if len(sys.argv) < 2:

        print(
            "Usage: python3 scanner.py <target> [start_port] [end_port]"
        )

        sys.exit(1)



    target = sys.argv[1]


    start_port = (
        int(sys.argv[2])
        if len(sys.argv) > 2
        else 1
    )


    end_port = (
        int(sys.argv[3])
        if len(sys.argv) > 3
        else 65535
    )



    try:

        target_ip = socket.gethostbyname(target)


    except socket.gaierror:


        print(
            "[-] Unable to resolve hostname"
        )

        sys.exit(1)



    print("\n" + "=" * 60)

    print(
        "ADVANCED NETWORK PORT SCANNER"
    )

    print(
        "Developed By: Siraj Aldula"
    )

    print("=" * 60)


    print(
        f"Target      : {target}"
    )

    print(
        f"IP Address  : {target_ip}"
    )

    print(
        f"Port Range  : {start_port}-{end_port}"
    )

    print("=" * 60)



    start_time = time.time()



    threads = []



    for port in range(start_port, end_port + 1):


        while len(threads) >= MAX_THREADS:


            threads = [
                t for t in threads
                if t.is_alive()
            ]


            time.sleep(0.01)



        thread = threading.Thread(

            target=scan_port,

            args=(target_ip, port)

        )


        threads.append(thread)

        thread.start()



    for thread in threads:

        thread.join()



    elapsed = time.time() - start_time



    open_ports.sort(
        key=lambda x: x["port"]
    )


    save_results(
        target,
        target_ip,
        start_port,
        end_port,
        elapsed
    )



    print("\n[+] Scan Completed")

    print(
        f"[+] Total Open Ports: {len(open_ports)}"
    )

    print(
        f"[+] Time Taken: {elapsed:.2f} seconds"
    )



if __name__ == "__main__":

    main()
