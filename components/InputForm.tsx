import { categoryOptions, customerOptions, dayOptions, genderOptions, paymentOptions, storeOptions } from "@/lib/constants";
import type { PredictPayload } from "@/lib/types";
import { useState } from "react";

type InputFormProps = {
  onPredict: (payload: PredictPayload) => Promise<void>;
  loading: boolean;
};

const inputClass =
  "w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm outline-none transition focus:border-action focus:ring-2 focus:ring-blue-200";

export function InputForm({ onPredict, loading }: InputFormProps) {
  const [form, setForm] = useState<PredictPayload>({
    quantity: 10,
    unit_price: 150,
    discount_pct: 10,
    month: 6,
    day_of_week: "Monday",
    is_weekend: 0,
    store_type: "Supermarket",
    category: "Staples",
    customer_type: "Member",
    gender: "Male",
    payment_method: "Cash"
  });

  const setField = <K extends keyof PredictPayload>(key: K, value: PredictPayload[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onPredict(form);
  };

  return (
    <form onSubmit={submit} className="rounded-xl bg-white p-5 shadow-lg">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-3">
          <Field label="Quantity">
            <input className={inputClass} type="number" value={form.quantity} onChange={(e) => setField("quantity", Number(e.target.value))} />
          </Field>
          <Field label="Unit Price (PHP)">
            <input className={inputClass} type="number" value={form.unit_price} onChange={(e) => setField("unit_price", Number(e.target.value))} />
          </Field>
          <Field label="Discount (%)">
            <input className={inputClass} type="number" value={form.discount_pct} onChange={(e) => setField("discount_pct", Number(e.target.value))} />
          </Field>
          <Field label="Month (1-12)">
            <input className={inputClass} type="number" min={1} max={12} value={form.month} onChange={(e) => setField("month", Number(e.target.value))} />
          </Field>
          <Field label="Day of Week">
            <select className={inputClass} value={form.day_of_week} onChange={(e) => setField("day_of_week", e.target.value)}>
              {dayOptions.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </Field>
          <label className="flex items-center gap-2 text-sm font-semibold text-slateblue">
            <input type="checkbox" checked={form.is_weekend === 1} onChange={(e) => setField("is_weekend", e.target.checked ? 1 : 0)} />
            Weekend?
          </label>
        </div>

        <div className="space-y-3">
          <SelectField label="Store Type" value={form.store_type} options={storeOptions} onChange={(value) => setField("store_type", value)} />
          <SelectField label="Product Category" value={form.category} options={categoryOptions} onChange={(value) => setField("category", value)} />
          <SelectField label="Customer Type" value={form.customer_type} options={customerOptions} onChange={(value) => setField("customer_type", value)} />
          <SelectField label="Gender" value={form.gender} options={genderOptions} onChange={(value) => setField("gender", value)} />
          <SelectField label="Payment" value={form.payment_method} options={paymentOptions} onChange={(value) => setField("payment_method", value)} />
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="mt-5 w-full rounded-lg bg-action px-4 py-3 text-base font-bold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {loading ? "Running Predictions..." : "Get Predictions from All 5 Models"}
      </button>
    </form>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-semibold text-slateblue">{label}</span>
      {children}
    </label>
  );
}

function SelectField<T extends string>({
  label,
  value,
  options,
  onChange
}: {
  label: string;
  value: string;
  options: readonly T[];
  onChange: (value: T) => void;
}) {
  return (
    <Field label={label}>
      <select className={inputClass} value={value} onChange={(e) => onChange(e.target.value as T)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </Field>
  );
}
