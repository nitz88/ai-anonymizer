from server import create_server

def main():
    mcp = create_server()
    mcp.run()

if __name__ == "__main__":
    main()