import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { tool, video_url, provider, api_key } = await req.json();

    if (!process.env.MCP_SERVER_URL) {
      return NextResponse.json(
        { error: "MCP_SERVER_URL env var is not set on Vercel" },
        { status: 500 }
      );
    }

    const transport = new SSEClientTransport(
      new URL(process.env.MCP_SERVER_URL)
    );
    const client = new Client({ name: "web-client", version: "1.0.0" });
    await client.connect(transport);

    const result = await client.callTool({
      name: tool,
      arguments: { video_url, provider, api_key },
    });

    await client.close();

    const text = (result.content as Array<{ type: string; text: string }>)[0]?.text ?? "";
    return NextResponse.json({ result: text });
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
