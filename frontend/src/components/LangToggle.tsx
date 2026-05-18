"use client";

import { Lang } from "@/lib/lang";

interface Props {
  lang: Lang;
  onChange: (lang: Lang) => void;
}

export default function LangToggle({ lang, onChange }: Props) {
  const buttons: { code: Lang; label: string }[] = [
    { code: "en", label: "EN" },
    { code: "ja", label: "JA" },
    { code: "ko", label: "KO" },
  ];

  return (
    <div className="flex items-center gap-0.5 bg-gd-surface border border-gd-subtle rounded-lg p-0.5">
      {buttons.map(({ code, label }) => {
        const active = lang === code;
        return (
          <button
            key={code}
            onClick={() => onChange(code)}
            className={`px-2.5 py-1 rounded text-xs transition-all ${
              active
                ? "bg-gd-accent-glow text-gd-text-primary"
                : "text-gd-text-muted hover:text-gd-text-secondary"
            }`}
            style={{ fontWeight: active ? 520 : 440 }}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
