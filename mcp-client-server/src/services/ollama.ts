import ollama from "ollama";

export class OllamaClient {
    constructor(
        private readonly model = "qwen3.5:4b"
    ) {}

    async chat(messages: any[], tools?: any[]) {
        const chat = ollama.chat({
            model: this.model,
            messages,
            tools
        });
        console.log("Ollama chat:", chat);
        return chat;
    }
}