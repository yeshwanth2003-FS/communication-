import socket
import threading

SERVER_IP = "192.168.0.150"  # Laptop A IP
SERVER_PORT = 2904


def receive_messages(sock):
    """Receive messages from Hercules continuously."""
    while True:
        try:
            data = sock.recv(4096)

            if not data:
                print("\nConnection closed by Laptop A.")
                break

            print("\nLaptop A:", data.decode("utf-8", errors="replace"))
            print("You: ", end="", flush=True)

        except OSError:
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
        client.connect((SERVER_IP, SERVER_PORT))
        print("Connected to Hercules on Laptop A.")
        print("Type a message and press Enter.")
        print("Type 'exit' to disconnect.\n")

        receiver = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )
        receiver.start()

        while True:
            message = input("You: ")

            if message.lower() == "exit":
                break

            client.sendall(message.encode("utf-8"))

    except ConnectionRefusedError:
        print("Connection refused. Check that Hercules is listening.")

    except TimeoutError:
        print("Connection timed out. Check the IP and network.")

    except OSError as error:
        print("Network error:", error)

    finally:
        client.close()
        print("Disconnected.")

if __name__ == "__main__":
    main()