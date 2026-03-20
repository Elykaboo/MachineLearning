export type PredictPayload = {
  quantity: number;
  unit_price: number;
  discount_pct: number;
  month: number;
  is_weekend: number;
  day_of_week: string;
  store_type: string;
  category: string;
  customer_type: string;
  gender: string;
  payment_method: string;
};

export type PredictResult = {
  linear_regression: string;
  logistic_regression: string;
  decision_tree: string;
  random_forest: string;
  neural_network: string;
};
