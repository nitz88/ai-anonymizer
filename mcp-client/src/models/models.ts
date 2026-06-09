export interface ChatMessage {
    role: "system" | "user" | "assistant" | "tool";
    content: string;
}

export interface ChatResponse {
    content: string;
}

export interface NormalizedLLMResponse {
    content: string;
    raw: unknown;
}

export interface LLMAdapter {
    chat(input: any): Promise<NormalizedLLMResponse>;
}

export interface LLMProvider {
    chat(
        messages: ChatMessage[],
        tools?: any[]
    ): Promise<any>;
}