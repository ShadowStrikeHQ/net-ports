import socket
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Set up command-line argument parsing.
    """
    parser = argparse.ArgumentParser(description="Map open ports and running services on a given host and port range.")
    parser.add_argument('host', type=str, help="Target host to scan (e.g., '127.0.0.1' or 'example.com').")
    parser.add_argument('--start-port', type=int, default=1, help="Starting port number for the scan (default: 1).")
    parser.add_argument('--end-port', type=int, default=1024, help="Ending port number for the scan (default: 1024).")
    return parser.parse_args()

def scan_port(host, port):
    """
    Check if a port is open on the given host.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set timeout for connection attempt
            result = s.connect_ex((host, port))
            if result == 0:  # Port is open
                service = socket.getservbyport(port, 'tcp') if port <= 65535 else 'Unknown'
                return port, service
    except socket.error as e:
        logging.error(f"Socket error on port {port}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error on port {port}: {e}")
    return None, None

def main():
    """
    Main function to handle the scanning process.
    """
    args = setup_argparse()
    host = args.host
    start_port = args.start_port
    end_port = args.end_port

    logging.info(f"Starting scan on host: {host} from port {start_port} to {end_port}")
    
    try:
        for port in range(start_port, end_port + 1):
            port, service = scan_port(host, port)
            if port:
                logging.info(f"Open port found: {port} (Service: {service})")
    except KeyboardInterrupt:
        logging.warning("Scan interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred during the scan: {e}")
    finally:
        logging.info("Scan completed.")

# Usage example:
# To scan localhost ports 1 through 1024, run the following:
# python main.py 127.0.0.1 --start-port 1 --end-port 1024
if __name__ == "__main__":
    main()