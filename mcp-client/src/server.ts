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

    app.use((req, res, next) => {
        console.log("REQ:", req.method, req.url);
        next();
    });

    return app;
}