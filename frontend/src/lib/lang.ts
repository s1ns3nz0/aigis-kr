export type Lang = "en" | "ja" | "ko";

const VALID_LANGS: ReadonlySet<Lang> = new Set(["en", "ja", "ko"]);

export function getLang(): Lang {
  if (typeof window === "undefined") return "ja";
  const raw = localStorage.getItem("aig_lang") as Lang | null;
  return raw && VALID_LANGS.has(raw) ? raw : "ja";
}

export function saveLang(lang: Lang) {
  localStorage.setItem("aig_lang", lang);
}
