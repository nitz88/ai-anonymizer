import { ChatMessage, LLMProvider, MCPToolResponse } from "../models/models.js";
import { MCPClient } from "../services/mcp-client.js";

export class AnonymizeChatAgent {
    constructor(
        private readonly mcp: MCPClient,
        private readonly llmProvider: LLMProvider
    ) {}

    private extractToolResult(result: any) {
        try {

            if (!result.isError) {
                const text = result.content?.[0]?.text;

                return JSON.parse(text);
            } else {
                console.error("We have got error while passing result");
                return null;
            }
            
        } catch (error) {
            console.error("We have got error while passing result");
            console.error(error);
            return null;
        }
        
    }

    async chat(userMessage: string) {
        const anonymizedRaw = await this.mcp.callTool("anonymize_text",{
            text: userMessage
        });

        console.log("Received text from anonymize_text tool");
        console.log(anonymizedRaw);

        const anonymized = this.extractToolResult(anonymizedRaw);

        console.log("Anonymized message:", anonymized);
        let messages: ChatMessage[] = [];
        
        if (anonymized && anonymized.hasPii) {
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

            messages = [
                {
                    role: "system",
                    content: promptText
                },
                {
                    role: "user",
                    content: anonymized.anonymizedText
                }
            ];
        } else {
            messages = [
                {
                    role: "user",
                    content: userMessage
                }
            ]
        }

        console.log("Prompt message which is sent to LLM");
        console.dir(messages);

        const response = await this.llmProvider.chat(
            messages
        );;

        console.log("chat service response:");
        console.dir(response, { depth: null });

        if (anonymized.hasPii) {
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
            const restored = restoredRaw as MCPToolResponse;
            return {
                type: "text",
                text:  restored.content[0]?.text ?? "",
                anonymized: true
            }
        } else {
            return {
                type: "text",
                text: response.content,
                anonymized: false
            };
        }
    }
}