"use client";

import { useState } from "react";
import EmailClassifier from "@/components/EmailClassifier";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <EmailClassifier />
      </div>
    </main>
  );
}
