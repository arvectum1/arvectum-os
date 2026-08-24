import { Activity } from "./Activity";
import { Copilot } from "./Copilot";
import { Discovery } from "./Discovery";
import { Dogfooding } from "./Dogfooding";
import { Governed } from "./Governed";
import { MyWork } from "./MyWork";
import { ObjectDetail } from "./ObjectDetail";
import { Organization } from "./Organization";
import { Products } from "./Products";
import { System } from "./System";
import { Work } from "./Work";
import { navigationLabels, useWorkspaceLanguage } from "./i18n";
import type { NavigationItem, WorkspaceContext } from "./types";

function groupForPath(path: string): string {
  if (path === "/" || path === "/today") return "today";
  if (path === "/work" || path === "/my-work" || path === "/products" || path.startsWith("/products/")) return "work";
  if (path === "/information" || path === "/search" || path === "/records" || path === "/documents" || path === "/knowledge" || path.startsWith("/objects/")) return "information";
  if (path === "/copilot") return "copilot";
  return "system";
}

function navigateTo(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function Today() {
  const { text } = useWorkspaceLanguage();
  return <>
    <section className="hero home-hero" aria-labelledby="today-title">
      <p className="eyebrow">{text("Рабочий день", "Working day")}</p>
      <h1 id="today-title">{text("Вот что сейчас требует внимания", "Here is what needs attention now")}</h1>
      <p>{text("Начните с текущей работы, найдите нужный контекст или спросите Arvectum.", "Start with current work, find context, or ask Arvectum.")}</p>
    </section>
    <MyWork embedded />
    <section className="quick-actions" aria-labelledby="quick-actions-title">
      <h2 id="quick-actions-title">{text("Быстрые действия", "Quick actions")}</h2>
      <div className="status-grid">
        <article><strong>{text("Открыть всю работу", "Open all work")}</strong><p>{text("Посмотреть очередь и продуктовые контексты.", "Review the queue and product contexts.")}</p><a href="/work" onClick={(event) => { event.preventDefault(); navigateTo("/work"); }}>{text("Открыть работу", "Open work")}</a></article>
        <article><strong>{text("Найти информацию", "Find information")}</strong><p>{text("Найти документ, запись или знание.", "Find a document, record, or knowledge context.")}</p><a href="/information" onClick={(event) => { event.preventDefault(); navigateTo("/information"); }}>{text("Найти информацию", "Find information")}</a></article>
        <article><strong>{text("Спросить Arvectum", "Ask Arvectum")}</strong><p>{text("Получить ответ с проверяемыми источниками.", "Get an answer with inspectable sources.")}</p><a href="/copilot" onClick={(event) => { event.preventDefault(); navigateTo("/copilot"); }}>{text("Спросить Arvectum", "Ask Arvectum")}</a></article>
      </div>
    </section>
  </>;
}

export function Shell({ context, onLogout }: { context: WorkspaceContext; onLogout: () => void }) {
  const { language, setLanguage, text } = useWorkspaceLanguage();
  const currentPath = window.location.pathname;
  const activeId = groupForPath(currentPath);
  const active = context.navigation.find((item) => item.id === activeId) ?? context.navigation[0];
  const objectId = currentPath.startsWith("/objects/") ? decodeURIComponent(currentPath.slice("/objects/".length)) : null;
  const productId = currentPath.startsWith("/products/") ? decodeURIComponent(currentPath.slice("/products/".length)) : null;
  const navLabel = (item: NavigationItem) => navigationLabels[item.id]?.[language] ?? item.label;
  const navigate = (item: NavigationItem) => (event: React.MouseEvent<HTMLAnchorElement>) => { event.preventDefault(); navigateTo(item.href); };

  let content: React.ReactNode;
  if (objectId) content = <ObjectDetail objectId={objectId} />;
  else if (currentPath === "/products" || productId) content = <Products productId={productId} />;
  else if (currentPath === "/my-work") content = <MyWork />;
  else if (currentPath === "/search" || currentPath === "/information") content = <Discovery />;
  else if (currentPath === "/records") content = <Discovery kind="record" />;
  else if (currentPath === "/documents") content = <Discovery kind="document" />;
  else if (currentPath === "/knowledge") content = <Discovery kind="knowledge" />;
  else if (currentPath === "/organization") content = <Organization organizationLabel={context.organization.label} />;
  else if (currentPath === "/activity") content = <Activity />;
  else if (currentPath === "/governed") content = <Governed csrfToken={context.session.csrf_token} />;
  else if (currentPath === "/dogfooding") content = <Dogfooding csrfToken={context.session.csrf_token} />;
  else if (activeId === "today") content = <Today />;
  else if (activeId === "work") content = <Work />;
  else if (activeId === "information") content = <Discovery />;
  else if (activeId === "copilot") content = <Copilot csrfToken={context.session.csrf_token} />;
  else content = <System release={context.release.id} />;

  return <div className="app-shell">
    <a className="skip-link" href="#workspace-main">{text("К содержанию", "Skip to content")}</a>
    <aside className="sidebar" aria-label={text("Навигация Arvectum OS", "Workspace navigation")}>
      <div className="brand" aria-label="Arvectum OS"><span className="brand-mark" aria-hidden="true"><span>AV</span></span><span className="brand-copy"><strong>Arvectum</strong><small>OS</small></span></div>
      <nav aria-label={text("Навигация Arvectum OS", "Workspace navigation")}><ul>{context.navigation.map((item) => <li key={item.id}><a href={item.href} onClick={navigate(item)} aria-current={item.id === active.id ? "page" : undefined}><span>{navLabel(item)}</span></a></li>)}</ul></nav>
      <div className="sidebar-controls"><div className="language-switch" role="group" aria-label={text("Язык интерфейса", "Interface language")}><button type="button" className={language === "ru" ? "active" : ""} aria-pressed={language === "ru"} onClick={() => setLanguage("ru")}>RU</button><button type="button" className={language === "en" ? "active" : ""} aria-pressed={language === "en"} onClick={() => setLanguage("en")}>EN</button></div><div className="sidebar-footnote">{text("Внутреннее рабочее пространство", "Internal workspace")} · {context.release.id}</div></div>
    </aside>
    <div className="workspace-column">
      <header className="topbar">
        <div className="context-chip" aria-label={`${text("Организация", "Organization")}: ${context.organization.label}`}><span className="eyebrow">{text("Организация", "Organization")}</span><strong>{context.organization.label}</strong></div>
        <div className="context-chip" aria-label={`${text("Пользователь", "Authenticated actor")}: ${context.actor.label}`}><span className="eyebrow">{text("Пользователь", "Authenticated actor")}</span><strong>{context.actor.label}</strong></div>
        <form className="global-search" role="search" onSubmit={(event) => { event.preventDefault(); const query = String(new FormData(event.currentTarget).get("q") ?? "").trim(); navigateTo(query ? `/information?q=${encodeURIComponent(query)}` : "/information"); }}>
          <label className="visually-hidden" htmlFor="global-search-query">{text("Глобальный поиск", "Global search")}</label><input id="global-search-query" name="q" type="search" maxLength={160} placeholder={text("Найти документ, запись, знание…", "Find a document, record, knowledge…")} /><button type="submit">{text("Найти", "Search")}</button>
        </form>
        <button type="button" className="quiet-button" onClick={onLogout}>{text("Выйти", "Sign out")}</button>
      </header>
      <main id="workspace-main" tabIndex={-1}>{content}</main>
    </div>
  </div>;
}
