import json
import asyncio
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters

BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = BASE_DIR.parent

TEST_CASES = BASE_DIR / "test_cases.json"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

REPORT_FILE = OUTPUT_DIR / "report.html"


async def run_test_suite():

    print("BASE_DIR =", BASE_DIR)
    print("TEST_CASES =", TEST_CASES)
    print("PROJECT_ROOT =", PROJECT_ROOT)

    with open(TEST_CASES, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "--with",
            "mcp",
            "src/run_stdio.py"
        ],
        cwd=str(PROJECT_ROOT)
    )

    results = []

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            for tc in test_cases:

                response = await session.call_tool(
                    "anonymize_text",
                    {
                        "text": tc["input"]
                    }
                )

                tool_result = response.content[0].text

                try:
                    parsed = json.loads(tool_result)
                except Exception:
                    parsed = {
                        "rawResponse": tool_result
                    }

                results.append({
                    "id": tc["id"],
                    "input": tc["input"],
                    "result": parsed
                })

    generate_html(results)

    print(f"Report generated: {REPORT_FILE}")


def generate_html(results):

    rows = []

    for r in results:

        result = r["result"]

        anonymized = result.get("anonymizedText", "")
        has_pii = result.get("hasPii", "")
        entities = result.get("entities", [])

        rows.append(f"""
        <tr>
            <td>{r['id']}</td>
            <td>{escape_html(r['input'])}</td>
            <td>{escape_html(anonymized)}</td>
            <td>{has_pii}</td>
            <td>{len(entities)}</td>
        </tr>
        """)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Anonymizer Test Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }}

            th {{
                background: #f5f5f5;
            }}

            tr:nth-child(even) {{
                background: #fafafa;
            }}
        </style>

    </head>
    <body>

        <h1>MCP Anonymizer Test Report</h1>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Input</th>
                    <th>Anonymized Output</th>
                    <th>Has PII</th>
                    <th>Entity Count</th>
                </tr>
            </thead>

            <tbody>
                {''.join(rows)}
            </tbody>

        </table>

    </body>
    </html>
    """

    REPORT_FILE.write_text(html, encoding="utf-8")


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


if __name__ == "__main__":
    asyncio.run(run_test_suite())