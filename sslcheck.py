import ssl
import socket
import datetime

def check_ssl_certificate(domain):
    try:
        cafile = "/etc/ssl/cert.pem"  # Replace with the actual path to your CA bundle file
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Use ssl.PROTOCOL_TLS_CLIENT
        context.load_verify_locations(cafile=cafile)
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert['notAfter']

                date_formats = ["%b %d %H:%M:%S %Y %Z", "%Y%m%d%H%M%SZ"]
                not_after = None
                for date_format in date_formats:
                    try:
                        not_after = datetime.datetime.strptime(not_after_str, date_format)
                        break
                    except ValueError:
                        pass

                if not_after:
                    now = datetime.datetime.now()

                    if not_after > now:
                        print(f"SSL certificate for {domain} is valid until {not_after}.")
                    else:
                        print(f"SSL certificate for {domain} has expired on {not_after}.")
                else:
                    print(f"Could not parse 'notAfter' field in the SSL certificate.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    domain_to_check = "www.netflix.com"  # Change to the domain you want to check
    check_ssl_certificate(domain_to_check)


