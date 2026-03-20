"use client";

import { Header } from "@/components/Header";
import { InputForm } from "@/components/InputForm";
import { ResultsPanel } from "@/components/ResultsPanel";
import type { PredictPayload, PredictResult } from "@/lib/types";
import { useState } from "react";

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictResult | null>(null);

  const onPredict = async (payload: PredictPayload) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = (await response.json()) as { error?: string; predictions?: PredictResult };

      if (!response.ok || !data.predictions) {
        throw new Error(data.error ?? "Prediction request failed.");
      }

      setResult(data.predictions);
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : "Unexpected error occurred.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-8 md:px-6 md:py-10">
      <Header />
      <InputForm onPredict={onPredict} loading={loading} />
      {error ? <p className="mt-4 rounded-md bg-red-100 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      <ResultsPanel result={result} />
    </main>
  );
}
