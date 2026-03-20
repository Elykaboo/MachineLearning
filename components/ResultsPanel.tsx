import type { PredictResult } from "@/lib/types";

type ResultsPanelProps = {
  result: PredictResult | null;
};

const rows: Array<{ label: string; key: keyof PredictResult }> = [
  { label: "Linear Regression", key: "linear_regression" },
  { label: "Logistic Regression", key: "logistic_regression" },
  { label: "Decision Tree", key: "decision_tree" },
  { label: "Random Forest", key: "random_forest" },
  { label: "Neural Network", key: "neural_network" }
];

export function ResultsPanel({ result }: ResultsPanelProps) {
  return (
    <section className="mt-6 rounded-xl bg-white p-5 shadow-lg">
      <h2 className="mb-3 text-lg font-bold text-slateblue">Model Predictions</h2>
      <div className="space-y-3">
        {rows.map((row) => (
          <div key={row.key} className="grid grid-cols-1 gap-1 border-b border-slate-100 pb-2 last:border-none">
            <p className="text-sm font-semibold text-slate-700">{row.label}</p>
            <p className="text-base text-action">{result ? result[row.key] : "---"}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
