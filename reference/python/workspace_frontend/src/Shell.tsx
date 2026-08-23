import { Activity } from "./Activity";
import { Copilot } from "./Copilot";
import { Discovery } from "./Discovery";
import { Dogfooding } from "./Dogfooding";
import { Governed } from "./Governed";
import { navigationLabels, useWorkspaceLanguage } from "./i18n";
import { MyWork } from "./MyWork";
import { ObjectDetail } from "./ObjectDetail";
import { Organization } from "./Organization";
import { Products } from "./Products";
import type { NavigationItem, WorkspaceContext } from "./types";

function activeItem(items: NavigationItem[]): NavigationItem {
  const current = window.location.pathname;
  if (current.startsWith("/objects/")) return items.find((item) => item.id === "search") ?? items[0];
  if (current.startsWith("/products/")) return items.find((item) => item.id === "products") ?? items[0];
  return items.find((item) => item.href === current) ?? items[0];
}

function navigateTo(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function Shell({ context, onLogout }: { context: WorkspaceContext; onLogout: () => void }) {
  const { language, setLanguage, text } = useWorkspaceLanguage();
  const active = activeItem(context.navigation);
  const currentPath = window.location.pathname;
  const objectId = currentPath.startsWith("/objects/") ? decodeURIComponent(currentPath.slice("/objects/".length)) : null;
  const productId = currentPath.startsWith("/products/") ? decodeURIComponent(currentPath.slice("/products/".length)) : null;
  const navigate = (item: NavigationItem) => (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    navigateTo(item.href);
  };
  const navLabel = (item: NavigationItem) => navigationLabels[item.id]?.[language] ?? item.label;

  return (
    <div className="app-shell">
      <a className="skip-link" href="#workspace-main">{text("К содержанию", "Skip to content")}</a>
      <aside className="sidebar" aria-label={text("Навигация Arvectum OS", "Workspace navigation")}>
        <div className="brand" aria-label="Arvectum OS">
          <span className="brand-mark" aria-hidden="true"><span>AV</span></span>
          <span className="brand-copy"><strong>Arvectum</strong><small>OS</small></span>
        </div>
        <nav aria-label={text("Навигация Arvectum OS", "Workspace navigation")}>
          <ul>
            {context.navigation.map((item) => (
              <li key={item.id}>
                <a href={item.href} onClick={navigate(item)} aria-current={item.id === active.id ? "page" : undefined}>
                  <span>{navLabel(item)}</span>
                  {item.availability !== "available" ? <small>{text("скоро", "planned")}</small> : null}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <div className="sidebar-controls">
          <div className="language-switch" role="group" aria-label={text("Язык интерфейса", "Interface language")}>
            <button type="button" className={language === "ru" ? "active" : ""} aria-pressed={language === "ru"} onClick={() => setLanguage("ru")}>RU</button>
            <button type="button" className={language === "en" ? "active" : ""} aria-pressed={language === "en"} onClick={() => setLanguage("en")}>EN</button>
          </div>
          <div className="sidebar-footnote">{text("Внутреннее рабочее пространство", "Internal workspace")} · {context.release.id}</div>
        </div>
      </aside>

      <div className="workspace-column">
        <header className="topbar">
          <div className="context-chip" aria-label={`${text("Организация", "Organization")}: ${context.organization.label}`}>
            <span className="eyebrow">{text("Организация", "Organization")}</span><strong>{context.organization.label}</strong>
          </div>
          <div className="context-chip" aria-label={`${text("Пользователь", "Authenticated actor")}: ${context.actor.label}`}>
            <span className="eyebrow">{text("Пользователь", "Authenticated actor")}</span><strong>{context.actor.label}</strong>
          </div>
          <form
            className="global-search"
            role="search"
            onSubmit={(event) => {
              event.preventDefault();
              const form = new FormData(event.currentTarget);
              const query = String(form.get("q") ?? "").trim();
              navigateTo(query ? `/search?q=${encodeURIComponent(query)}` : "/search");
            }}
          >
            <label className="visually-hidden" htmlFor="global-search-query">{text("Глобальный поиск", "Global search")}</label>
            <input id="global-search-query" name="q" type="search" maxLength={160} placeholder={text("Поиск по записям, документам и знаниям", "Search records, documents, knowledge")} />
            <button type="submit">{text("Найти", "Search")}</button>
          </form>
          <button type="button" className="quiet-button" onClick={onLogout}>{text("Выйти", "Sign out")}</button>
        </header>

        <main id="workspace-main" tabIndex={-1}>
          {objectId ? (
            <ObjectDetail objectId={objectId} />
          ) : active.id === "home" ? (
            <>
              <section className="hero home-hero" aria-labelledby="home-title">
                <div className="hero-signal" aria-hidden="true"><span /><span /><span /></div>
                <p className="eyebrow">{text("Рабочее пространство Arvectum OS", "Productive Workspace")}</p>
                <h1 id="home-title">{text("Контекст организации готов к работе.", "Your organization context is established.")}</h1>
                <p>
                  {text(
                    "Здесь собраны текущие задачи, активность, поиск по организационному контексту, помощь Arvectum AI и управляемые действия. Технические детали доступны по запросу, а значимые действия по-прежнему проходят через действующие контуры полномочий.",
                    "My Work surfaces current attention signals, Activity shows an observed non-authoritative timeline and current alerts, discovery finds governed organizational context, Ask Arvectum provides source-grounded assistance, and Governed actions keeps consequential work behind current authority gates.",
                  )}
                </p>
                <div className="status-grid">
                  <article><span>{text("Контекст", "Context")}</span><strong>{text("Определён сервером", "Server resolved")}</strong><p>{text("Браузер не выбирает организацию или пользователя.", "Browser input cannot choose the Organization or actor.")}</p></article>
                  <article><span>{text("ИИ-помощь", "AI assistance")}</span><strong>{text("С опорой на источники", "Grounded, transient")}</strong><p>{text("Факты, выводы и неопределённость остаются различимыми и проверяемыми.", "Sourced facts, synthesis and uncertainty stay distinguishable and inspectable.")}</p></article>
                  <article><span>{text("Полномочия", "Authority")}</span><strong>{text("Не подразумеваются", "Not implied")}</strong><p>{text("Сеанс, поиск, ответы ИИ и кнопки не создают организационных полномочий.", "Session, search results, Copilot answers and action buttons do not create Organizational Authority.")}</p></article>
                </div>
              </section>
              <MyWork embedded />
            </>
          ) : active.id === "organization" ? (
            <Organization organizationLabel={context.organization.label} />
          ) : active.id === "my-work" ? (
            <MyWork />
          ) : active.id === "activity" ? (
            <Activity />
          ) : active.id === "search" ? (
            <Discovery />
          ) : active.id === "records" ? (
            <Discovery kind="record" />
          ) : active.id === "documents" ? (
            <Discovery kind="document" />
          ) : active.id === "knowledge" ? (
            <Discovery kind="knowledge" />
          ) : active.id === "copilot" ? (
            <Copilot csrfToken={context.session.csrf_token} />
          ) : active.id === "governed" ? (
            <Governed csrfToken={context.session.csrf_token} />
          ) : active.id === "products" ? (
            <Products productId={productId} />
          ) : active.id === "dogfooding" ? (
            <Dogfooding csrfToken={context.session.csrf_token} />
          ) : (
            <section className="placeholder" aria-labelledby="placeholder-title">
              <p className="eyebrow">{text("Навигация", "Navigation spine")}</p>
              <h1 id="placeholder-title">{navLabel(active)}</h1>
              <p>{text("Этот раздел пока не активирован в текущей версии.", "This surface is not activated in the current release.")}</p>
              <p className="boundary-note">{text("Этот экран не раскрывает продуктовые или канонические бизнес-данные.", "No product or canonical business data is exposed by this placeholder.")}</p>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}
