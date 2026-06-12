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

export interface ChatResult {
    type: "text";
    text: string;
    anonymized?: boolean;
}

export interface MCPTextContent {
    type: "text";
    text: string;
}

export interface MCPToolResponse {
    content: MCPTextContent[];
    isError?: boolean;
}