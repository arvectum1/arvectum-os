import { MyWork } from "./MyWork";
import { Products } from "./Products";
import { useWorkspaceLanguage } from "./i18n";

export function Work() {
  const { text } = useWorkspaceLanguage();
  return <section className="work-page" aria-labelledby="work-title">
    <header className="hero">
      <p className="eyebrow">{text("Рабочее пространство", "Workspace")}</p>
      <h1 id="work-title">{text("Работа", "Work")}</h1>
      <p>{text("Здесь собраны текущие задачи и доступные продуктовые контексты.", "Current work and available product contexts are collected here.")}</p>
    </header>
    <MyWork />
    <Products />
  </section>;
}
