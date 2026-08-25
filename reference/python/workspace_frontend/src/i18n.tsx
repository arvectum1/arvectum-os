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
  today: { ru: "Главная", en: "Home" },
  work: { ru: "Задачи", en: "Tasks" },
  information: { ru: "Документы", en: "Documents" },
  copilot: { ru: "Arvectum AI", en: "Arvectum AI" },
  system: { ru: "Настройки", en: "Settings" },
};
