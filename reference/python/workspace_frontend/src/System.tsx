import { useWorkspaceLanguage } from "./i18n";

const destinations = [
  { href: "/organization", ru: "Организация", en: "Organization", ruDetail: "Общий контекст организации и структура.", enDetail: "Organization context and structure." },
  { href: "/activity", ru: "Активность", en: "Activity", ruDetail: "Наблюдаемые события и сигналы.", enDetail: "Observed events and signals." },
  { href: "/governed", ru: "Управляемые действия", en: "Governed actions", ruDetail: "Проверка текущего состояния и ограничений.", enDetail: "Inspect current state and gates." },
  { href: "/my-work?mode=scenario", ru: "Тестовые сценарии", en: "Test scenarios", ruDetail: "Отдельно просмотреть сценарные данные.", enDetail: "Inspect scenario data separately." },
  { href: "/dogfooding", ru: "Обратная связь", en: "Feedback", ruDetail: "Сообщить о наблюдении или проблеме.", enDetail: "Report an observation or issue." },
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
    <h1 id="system-title">{text("Система и настройки", "System and settings")}</h1>
    <p>{text("Диагностика, аудит и технический контекст рабочего пространства.", "Diagnostics, audit, and technical workspace context.")}</p>
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
