import { createServer } from "./server.js";
import { MCPClient } from "./services/mcp-client.js";
import { OllamaClient } from "./services/ollama.js";
import { ChatAgent } from "./agents/chat-agent.js";
import { AnonymizeChatAgent } from "./agents/anonymize-chat.agent.js";
import { createChatRouter } from "./routes/chat.js";

async function bootstrap() {
    const app = createServer();
    const mcpClient = new MCPClient();
    await mcpClient.connect();

    console.log("MCP connected");

    const ollama = new OllamaClient();
    const tools = await mcpClient.getOllamaTools();

    // const agent = new ChatAgent(
    //     mcpClient,
    //     ollama,
    //     tools
    // );

    const agent = new AnonymizeChatAgent(
        mcpClient,
        ollama,
        tools
    );

    app.use(
        "/chat",
        createChatRouter(agent)
    );

    const port = 3000;

    app.listen(port, () => {
        console.log(
            `Server listening on ${port}`
        );
    });
}

bootstrap().catch(error => {
    console.error(error);
    process.exit(1);
});