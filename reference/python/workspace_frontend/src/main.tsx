import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { LanguageProvider } from "./i18n";
import "./styles.css";
import "./governed.css";
import "./brand.css";

const root = document.getElementById("root");
if (!root) throw new Error("Workspace root element is missing");

createRoot(root).render(
  <StrictMode>
    <LanguageProvider initialLanguage="ru">
      <App />
    </LanguageProvider>
  </StrictMode>,
);
