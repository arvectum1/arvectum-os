import { useWorkspaceLanguage } from "./i18n";

const destinations = [
  { href: "/organization", ru: "Организация", en: "Organization", ruDetail: "Общий технический контекст организации.", enDetail: "Technical organization context." },
  { href: "/activity", ru: "Активность", en: "Activity", ruDetail: "Подробная наблюдаемая активность.", enDetail: "Detailed observed activity." },
  { href: "/governed", ru: "Управляемые действия", en: "Governed actions", ruDetail: "Проверка контекста и действующих ограничений.", enDetail: "Inspect context and current gates." },
  { href: "/dogfooding", ru: "Обратная связь", en: "Dogfooding", ruDetail: "Зафиксировать наблюдение о работе Workspace.", enDetail: "Record a Workspace use observation." },
];

function navigate(href: string, event: React.MouseEvent<HTMLAnchorElement>) {
  event.preventDefault();
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function System({ release }: { release: string }) {
  const { text } = useWorkspaceLanguage();
  return <section className="hero" aria-labelledby="system-title">
    <p className="eyebrow">Arvectum OS</p>
    <h1 id="system-title">{text("Система", "System")}</h1>
    <p>{text("Диагностика, аудит и технический контекст Arvectum OS.", "Diagnostics, audit, and technical Arvectum OS context.")}</p>
    <div className="status-grid">
      {destinations.map((item) => <article key={item.href}>
        <strong>{text(item.ru, item.en)}</strong>
        <p>{text(item.ruDetail, item.enDetail)}</p>
        <a href={item.href} onClick={(event) => navigate(item.href, event)}>{text("Открыть", "Open")}</a>
      </article>)}
      <article><span>{text("Версия Workspace", "Workspace release")}</span><strong>{release}</strong><p>{text("Точная версия текущего внутреннего приложения.", "Exact release of this internal application.")}</p></article>
    </div>
  </section>;
}
