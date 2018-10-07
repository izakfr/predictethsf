from listener import InfuraClient

if __name__ == "__main__":
    client = InfuraClient(network='prod')
    client.run()