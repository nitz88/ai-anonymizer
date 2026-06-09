import { Router } from "express";

export function createChatRouter(agent: any) {
    const router = Router();

    router.post("/", async (req, res) => {
         try {
            const message = req.body?.message;

            console.log("Received message:", message);

            if (!message) {
                return res.status(400).json({
                    error: "message required"
                });
            }

            const result = await agent.chat(message);
            console.log("Result message:", result);
            return res.json(result);
        } catch (error) {
            console.error(error);
            return res.status(500).json({
                error: "internal error"
            });
        }
    });

    return router;
}