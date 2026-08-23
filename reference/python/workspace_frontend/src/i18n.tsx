import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

export type WorkspaceLanguage = "ru" | "en";

type LanguageContextValue = {
  language: WorkspaceLanguage;
  setLanguage: (language: WorkspaceLanguage) => void;
  text: (ru: string, en: string) => string;
};

// English is the non-provider fallback so existing isolated component tests remain explicit.
// The production application always mounts LanguageProvider with Russian as the initial language.
const LanguageContext = createContext<LanguageContextValue>({
  language: "en",
  setLanguage: () => undefined,
  text: (_ru, en) => en,
});

export function LanguageProvider({ children, initialLanguage = "ru" }: { children: ReactNode; initialLanguage?: WorkspaceLanguage }) {
  const [language, setLanguage] = useState<WorkspaceLanguage>(initialLanguage);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const value = useMemo<LanguageContextValue>(() => ({
    language,
    setLanguage,
    text: (ru, en) => language === "ru" ? ru : en,
  }), [language]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useWorkspaceLanguage(): LanguageContextValue {
  return useContext(LanguageContext);
}

export const navigationLabels: Record<string, { ru: string; en: string }> = {
  home: { ru: "Главная", en: "Home" },
  organization: { ru: "Организация", en: "Organization" },
  "my-work": { ru: "Моя работа", en: "My Work" },
  activity: { ru: "Активность", en: "Activity" },
  search: { ru: "Поиск", en: "Search" },
  records: { ru: "Записи", en: "Records" },
  documents: { ru: "Документы", en: "Documents" },
  knowledge: { ru: "Знания", en: "Knowledge" },
  copilot: { ru: "Спросить Arvectum", en: "Ask Arvectum" },
  governed: { ru: "Управляемые действия", en: "Governed actions" },
  products: { ru: "Продукты", en: "Products" },
  dogfooding: { ru: "Обратная связь", en: "Dogfooding" },
};
