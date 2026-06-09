import { MCPClient } from "../services/mcp-client.js";
import { OllamaClient } from "../services/ollama.js";

export class ChatAgent {
    constructor(
        private readonly mcp: MCPClient,
        private readonly ollama: OllamaClient,
        private readonly tools: any[]
    ) {}

    async chat(userMessage: string) {
        
        const messages = [
            {
                role: "user",
                content: userMessage
            }
        ];

        const response = await this.ollama.chat(
            messages,
            this.tools
        );

        const toolCalls = response.message?.tool_calls ?? [];

        if (toolCalls.length > 0) {
            for (const toolCall of toolCalls) {
                
                const result = await this.mcp.callTool(
                    toolCall.function.name,
                    toolCall.function.arguments
                );
                
                messages.push(response.message);
                const toolResult = result as {
                    content?: Array<{
                        type: string;
                        text?: string;
                    }>;
                };

                const toolText =
                    toolResult.content?.[0]?.text ?? "";
                
                messages.push({
                    role: "tool",
                    content: JSON.stringify(toolText)
                });
            }
            return await this.ollama.chat(
                messages,
                this.tools
            );
        }

        return response;
    }
}