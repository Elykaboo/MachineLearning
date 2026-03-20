import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Retail Intelligence System",
  description: "ML-powered retail predictions with Next.js and Tailwind"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
