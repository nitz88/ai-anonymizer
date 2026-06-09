import { createServer } from "./server.js";
import { MCPClient } from "./services/mcp-client.js";
import { OllamaClient } from "./services/ollama-client.js";
import { ChatAgent } from "./agents/chat-agent.js";
import { AnonymizeChatAgent } from "./agents/anonymize-chat.agent.js";
import { createChatRouter } from "./routes/chat.js";
import { LlamaCppProvider } from "./services/llama-cpp-client.js";

export function createLLMClient() {
    const args = process.argv.slice(2);
    const providerArg = args.find(a => a.startsWith("--provider="));

    const provider = providerArg?.split("=")[1] ?? process.env.LLM_PROVIDER ?? "";

    console.log("provider", provider);
    
    switch (provider) {
        case "ollama":
            return new OllamaClient();

        default:
            return new LlamaCppProvider();
    }
}

async function bootstrap() {
    const app = createServer();
    const mcpClient = new MCPClient();

    await mcpClient.connect();

    console.log("MCP connected");
    
    const llm = createLLMClient();
   
    const agent = new AnonymizeChatAgent(
        mcpClient,
        llm
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