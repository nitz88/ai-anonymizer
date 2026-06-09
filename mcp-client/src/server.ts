import express from "express";
import cors from "cors";

export function createServer() {
    const app = express();

    app.use(cors());

    app.use(
        express.json({
            limit: "1mb"
        })
    );

    return app;
}