import { MCPClient } from "../services/mcp-client.js";
import { OllamaClient } from "../services/ollama.js";

export class AnonymizeChatAgent {
    constructor(
        private readonly mcp: MCPClient,
        private readonly ollama: OllamaClient,
        private readonly tools: any[]
    ) {}

    private extractToolResult(result: any) {
        const text = result.content?.[0]?.text;

        return JSON.parse(text);
    }

    async chat(userMessage: string) {
        console.log("Original user message:", userMessage);
        
        const anonymizedRaw = await this.mcp.callTool("anonymize_text",{
            text: userMessage
        });

        const anonymized = this.extractToolResult(anonymizedRaw);

        console.log("Anonymized message:", anonymized.anonymizedText);

        const promptResult =
            await this.mcp.getPrompt(
                "anonymize_before_send",
                {
                    session_id:
                        anonymized.sessionId
                }
            );

        console.log("Prompt result:");
        console.dir(promptResult, { depth: null });

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

        const messages = [
            {
                role: "system",
                content: promptText
            },
            {
                role: "user",
                content: anonymized.anonymizedText
            }
        ];

        console.log(
            JSON.stringify(messages, null, 2)
        );

        const response = await this.ollama.chat(
            messages
        );;

        console.log("Ollama response:");
        console.dir(response, { depth: null });

        const restoredRaw =
            await this.mcp.callTool(
                "deanonymize_text",
                {
                    text:
                        response.message.content,

                    session_id:
                        anonymized.sessionId
                }
            );
        
        console.log("Restored message:", restoredRaw);

        // const restored =
        //     this.extractToolResult(
        //         restoredRaw
        //     );

        // console.log("Restored message after extraction:", restored);

        // return restored.restoredText;
        // return await this.ollama.chat(
        //     messages,
        //     this.tools
        // );
        return restoredRaw;
    }
}