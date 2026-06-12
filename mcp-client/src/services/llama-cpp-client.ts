import { LLMProvider, ChatMessage } from "../models/models.js";

export class LlamaCppProvider implements LLMProvider {

    constructor(
        private readonly baseUrl: string = "http://127.0.0.1:8080"
    ) {
        console.log("Using llamaCPP provider");
    }

    async chat(messages: ChatMessage[]): Promise<any> {
        const response = await fetch(
            `${this.baseUrl}/v1/chat/completions`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    messages,
                    temperature: 0.7
                })
            }
        );

        const json = await response.json();
        console.log("Real response from LLM");
        console.log(json);
        
        return {
            content: json.choices?.[0]?.message?.content
        };
    }
}