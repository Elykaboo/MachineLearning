import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const pythonApiBase = process.env.PYTHON_API_URL ?? "http://127.0.0.1:8000";

  try {
    const payload = await request.json();
    const response = await fetch(`${pythonApiBase.replace(/\/$/, "")}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data?.detail ?? data?.error ?? "Python API returned an error." },
        { status: response.status }
      );
    }

    return NextResponse.json({ predictions: data.predictions }, { status: 200 });
  } catch (error) {
    const fallback = `Cannot reach Python API at ${pythonApiBase}. Start retail_api.py for local use, or set PYTHON_API_URL to your deployed backend URL.`;
    const message = error instanceof Error && error.message ? `${error.message}. ${fallback}` : fallback;
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
