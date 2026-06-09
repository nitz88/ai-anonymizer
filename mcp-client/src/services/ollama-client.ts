import ollama from "ollama";
import { LLMProvider, ChatMessage } from "../models/models.js";

export class OllamaClient implements LLMProvider {
    constructor(
        private readonly model = "gemma4:latest"
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