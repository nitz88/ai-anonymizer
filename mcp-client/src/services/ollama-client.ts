import ollama from "ollama";
import { LLMProvider, ChatMessage } from "../models/models.js";

export class OllamaClient implements LLMProvider {
    constructor(
        private readonly model = "qwen2.5-coder:3b"
    ) {
        console.log("Using ollama provider");
    }

    async chat(messages: ChatMessage[], tools: any[] = []): Promise<any> {
        const response = await ollama.chat({
            model: this.model,
            messages,
            tools
        });
        
        return {
            content: response?.message?.content || ""
        };
    }
}