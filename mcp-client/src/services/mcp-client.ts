import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

export class MCPClient {
    private mcp!: Client;
    private transport!: StreamableHTTPClientTransport;
    private toolCache?: any[];
    
    constructor(private readonly serverName = "127.0.0.1",
                private readonly serverPort = 8000) {
        this.createMCPClient();
    }

    private createMCPClient() {
        this.transport = new StreamableHTTPClientTransport(
            new URL(`http://${this.serverName}:${this.serverPort}/mcp`),
        );

        this.mcp = new Client({
            name: "MCP Client",
            version: "1.0.0"
        });
    }

    public async connect() {
        console.log(`Connecting to MCP server ${this.serverName} on port ${this.serverPort}...`);
        await this.mcp.connect(this.transport);
    }

    public async listTools() {
        if (this.toolCache) {
            return this.toolCache;
        }
        const result = await this.mcp.listTools();

        this.toolCache = result.tools;

        return this.toolCache;
    }

    public async listPrompts() {
        return this.mcp.listPrompts();
    }

    public async getPrompt(name: string, args: Record<string, string>) {
        return this.mcp.getPrompt({
            name: name,
            arguments: args
        });
    }

    public async callTool(name: string, args: Record<string, unknown>) {
        return this.mcp.callTool({
            name,
            arguments: args
        });
    }

    public async disconnect() {
        await this.transport.close();
    }

}