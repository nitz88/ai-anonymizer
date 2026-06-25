from server import create_server

def main():
    mcp = create_server()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()