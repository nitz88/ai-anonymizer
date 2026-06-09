import { ChatMessage, LLMProvider } from "../models/models.js";
import { MCPClient } from "../services/mcp-client.js";
import { OllamaClient } from "../services/ollama-client.js";

export class AnonymizeChatAgent {
    constructor(
        private readonly mcp: MCPClient,
        private readonly llmProvider: LLMProvider
    ) {}

    private extractToolResult(result: any) {
        const text = result.content?.[0]?.text;

        return JSON.parse(text);
    }

    async chat(userMessage: string) {
        const anonymizedRaw = await this.mcp.callTool("anonymize_text",{
            text: userMessage
        });

        const anonymized = this.extractToolResult(anonymizedRaw);

        console.log("Anonymized message:", anonymized);

        const promptResult =
            await this.mcp.getPrompt(
                "anonymize_before_send",
                {
                    session_id:
                        anonymized.sessionId
                }
            );

        const promptText = promptResult.messages
            .filter(
                m => m.content.type === "text"
            )
            .map(
                m => m.content.type === "text"
                    ? m.content.text
                    : ""
            )
            .join("\n");

        const messages: ChatMessage[] = [
            {
                role: "system",
                content: promptText
            },
            {
                role: "user",
                content: anonymized.anonymizedText
            }
        ];

        const response = await this.llmProvider.chat(
            messages
        );;

        console.log("chat service response:");
        console.dir(response, { depth: null });

        const restoredRaw =
            await this.mcp.callTool(
                "deanonymize_text",
                {
                    text:
                        response.content,

                    session_id:
                        anonymized.sessionId
                }
            );
        
        return restoredRaw;
    }
}