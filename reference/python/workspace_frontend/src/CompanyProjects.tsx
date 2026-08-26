import { useEffect, useState } from "react";
import { loadCompanyPortfolio } from "./f11Api";
import type { CompanyPortfolioProjection, CompanyProjectCard } from "./f11Types";
import { useWorkspaceLanguage } from "./i18n";
import "./CompanyWorkspace.css";

type State =
  | { kind: "loading" }
  | { kind: "ready"; data: CompanyPortfolioProjection }
  | { kind: "error"; code: string };

const TARGET_LABELS: Record<string, { ru: string; en: string }> = {
  web: { ru: "Веб / GitHub / ChatGPT", en: "Web / GitHub / ChatGPT" },
  "mac-mini": { ru: "Mac mini", en: "Mac mini" },
  macbook: { ru: "MacBook", en: "MacBook" },
  "windows-laptop": { ru: "Ноутбук Windows", en: "Windows laptop" },
  "windows-test-laptop": { ru: "Стендовый ноутбук Windows", en: "Windows test laptop" },
  "linux-test-laptop": { ru: "Стендовый ноутбук Linux", en: "Linux test laptop" },
  unspecified: { ru: "Не указано", en: "Not specified" },
};

function OwnerList({ title, items, empty }: { title: string; items: string[]; empty: string }) {
  return <section className="project-owner-section">
    <h3>{title}</h3>
    {items.length ? <ul>{items.map((item) => <li key={item}>{item}</li>)}</ul> : <p className="project-empty-value">{empty}</p>}
  </section>;
}

function ProjectCard({ project }: { project: CompanyProjectCard }) {
  const { language, text } = useWorkspaceLanguage();
  const status = project.roadmap.status ?? (
    project.state === "reconciliation-required"
      ? text("Требуется reconciliation", "Reconciliation required")
      : project.state === "unavailable"
        ? text("Источник недоступен", "Source unavailable")
        : text("Статус не указан", "Status not specified")
  );
  const targetItems = project.execution_targets
    .filter((target) => target !== "unspecified")
    .map((target) => TARGET_LABELS[target]?.[language] ?? target);
  const noSourceData = text("Нет данных в каноническом источнике", "No data in canonical source");

  return <article className="company-card company-project-card">
    <header className="company-card-head">
      <div>
        <p className="eyebrow">{project.id} · {project.kind}</p>
        <h2>{project.label}</h2>
        {project.roadmap.source_updated ? <p className="project-source-updated">{text("Источник обновлён", "Source updated")}: {project.roadmap.source_updated}</p> : null}
      </div>
      <span className={`company-state company-state-${project.state}`}>{status}</span>
    </header>

    {project.state !== "current-source-backed" ? <p className="project-state-message">{project.message}</p> : null}

    <div className="project-owner-grid">
      <OwnerList title={text("Где сейчас", "Current position")} items={project.roadmap.current} empty={noSourceData} />
      <OwnerList title={text("Что уже сделано", "Completed")} items={project.roadmap.done} empty={noSourceData} />
      <OwnerList title={text("Что можно делать сейчас", "Available now")} items={project.roadmap.unlocked} empty={noSourceData} />
      <OwnerList title={text("Ветки развития", "Development branches")} items={project.roadmap.branches} empty={noSourceData} />
      <OwnerList title={text("Что заблокировано / ждёт", "Blocked / pending")} items={project.roadmap.blocked} empty={text("Нет явно зафиксированных блокеров", "No explicit blockers recorded")} />
      <OwnerList title={text("Где выполнять", "Execution target")} items={targetItems} empty={text("Не указано в каноническом источнике", "Not specified in canonical source")} />
    </div>

    <details className="project-technical-details">
      <summary>{text("Источник и технические доказательства", "Source and technical evidence")}</summary>
      <dl className="company-facts">
        <div><dt>{text("Репозиторий", "Repository")}</dt><dd><code>{project.repository ?? "—"}</code></dd></div>
        <div><dt>{text("Roadmap / status source", "Roadmap / status source")}</dt><dd><code>{project.roadmap_path ?? "—"}</code></dd></div>
        <div><dt>{text("Authority mode", "Authority mode")}</dt><dd>{project.authority_mode}</dd></div>
        <div><dt>{text("Версия roadmap", "Roadmap version")}</dt><dd>{project.roadmap.version ?? "—"}</dd></div>
        <div><dt>{text("Точный commit", "Exact commit")}</dt><dd>{project.source ? <code>{project.source.commit_sha}</code> : "—"}</dd></div>
        <div><dt>{text("SHA-256 содержимого", "Content SHA-256")}</dt><dd>{project.source ? <code>{project.source.content_sha256}</code> : "—"}</dd></div>
        <div><dt>{text("Получено", "Fetched")}</dt><dd>{project.source?.fetched_at ?? "—"}</dd></div>
        <div><dt>{text("Свежесть fetch", "Fetch freshness")}</dt><dd>{project.source?.freshness ?? text("не подтверждена", "not established")}</dd></div>
      </dl>
    </details>
  </article>;
}

export function CompanyProjects() {
  const { text } = useWorkspaceLanguage();
  const [state, setState] = useState<State>({ kind: "loading" });
  const refresh = () => {
    setState({ kind: "loading" });
    void loadCompanyPortfolio()
      .then((data) => setState({ kind: "ready", data }))
      .catch((error) => setState({ kind: "error", code: error instanceof Error ? error.message : "COMPANY_PORTFOLIO_UNAVAILABLE" }));
  };
  useEffect(() => { refresh(); }, []);

  if (state.kind === "loading") return <section className="company-page" aria-live="polite">{text("Читаем канонические дорожные карты…", "Reading canonical roadmaps…")}</section>;
  if (state.kind === "error") return <section className="company-page" role="alert"><p className="eyebrow">F11B · Provisional 0.1.0</p><h1>{text("Портфель проектов недоступен", "Project portfolio unavailable")}</h1><p>{text("Workspace не подменяет недоступный canonical source данными из чата, памяти модели или технической активности.", "Workspace does not replace an unavailable canonical source with chat, model memory, or technical activity.")}</p><code>{state.code}</code><div><button type="button" onClick={refresh}>{text("Повторить", "Retry")}</button></div></section>;

  const sourceBacked = state.data.projects.filter((project) => project.state === "current-source-backed").length;
  const reconciliation = state.data.projects.filter((project) => project.state === "reconciliation-required").length;
  const unavailable = state.data.projects.filter((project) => project.state === "unavailable").length;

  return <section className="company-page" aria-labelledby="company-projects-title">
    <header className="company-page-head project-page-head">
      <div>
        <p className="eyebrow">F11B · Product Contract Provisional 0.1.0</p>
        <h1 id="company-projects-title">{text("Проекты компании", "Company projects")}</h1>
        <p>{text("Единая read-only сводка: где сейчас каждый проект, что уже сделано, что доступно дальше, какие ветки и блокеры есть и где выполнять работу.", "One read-only view of where each project is, what is complete, what is available next, its branches and blockers, and where the work belongs.")}</p>
      </div>
      <button type="button" onClick={refresh}>{text("Обновить", "Refresh")}</button>
    </header>

    <div className="project-portfolio-summary" aria-label={text("Состояние источников", "Source status")}>
      <span><strong>{sourceBacked}</strong>{text("с актуальным источником", "source-backed")}</span>
      <span><strong>{reconciliation}</strong>{text("требуют reconciliation", "need reconciliation")}</span>
      <span><strong>{unavailable}</strong>{text("недоступны", "unavailable")}</span>
    </div>

    <details className="company-boundary-details">
      <summary>{text("Как читать эту страницу", "How to read this page")}</summary>
      <p>{text("Workspace ничего не записывает обратно в roadmaps и не подменяет отсутствующие факты данными из чата или памяти. Технический источник и exact SHA спрятаны в каждой карточке под отдельным раскрывающимся блоком.", "Workspace writes nothing back to roadmaps and does not fill missing facts from chat or memory. The exact technical source and SHA are available inside each project under a separate disclosure.")}</p>
    </details>

    <div className="company-grid">{state.data.projects.map((project) => <ProjectCard project={project} key={project.id} />)}</div>
  </section>;
}
