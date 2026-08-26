import { useEffect, useState } from "react";
import { loadCompanyPortfolio } from "./f11Api";
import type { CompanyPortfolioProjection, CompanyProjectCard } from "./f11Types";
import { useWorkspaceLanguage } from "./i18n";
import "./CompanyWorkspace.css";

type State =
  | { kind: "loading" }
  | { kind: "ready"; data: CompanyPortfolioProjection }
  | { kind: "error"; code: string };

function ProjectCard({ project }: { project: CompanyProjectCard }) {
  const { text } = useWorkspaceLanguage();
  const status = project.roadmap.status ?? text("Требуется reconciliation", "Reconciliation required");
  return <article className="company-card">
    <header className="company-card-head">
      <div><p className="eyebrow">{project.id} · {project.kind}</p><h2>{project.label}</h2></div>
      <span className={`company-state company-state-${project.state}`}>{status}</span>
    </header>
    <p>{project.message}</p>
    <dl className="company-facts">
      <div><dt>{text("Репозиторий", "Repository")}</dt><dd><code>{project.repository}</code></dd></div>
      <div><dt>{text("Roadmap", "Roadmap")}</dt><dd><code>{project.roadmap_path ?? "—"}</code></dd></div>
      <div><dt>{text("Authority mode", "Authority mode")}</dt><dd>{project.authority_mode}</dd></div>
      <div><dt>{text("Точное состояние", "Exact state")}</dt><dd>{project.source ? <code>{project.source.commit_sha}</code> : "—"}</dd></div>
      <div><dt>{text("Получено", "Fetched")}</dt><dd>{project.source?.fetched_at ?? "—"}</dd></div>
      <div><dt>{text("Свежесть", "Freshness")}</dt><dd>{project.source?.freshness ?? text("не подтверждена", "not established")}</dd></div>
    </dl>
    {project.roadmap.current.length ? <section className="company-subsection"><h3>{text("Сейчас", "Current")}</h3><ul>{project.roadmap.current.map((item) => <li key={item}>{item}</li>)}</ul></section> : null}
    {project.roadmap.unlocked.length ? <section className="company-subsection"><h3>{text("Доступные ветки", "Available lanes")}</h3><ul>{project.roadmap.unlocked.map((item) => <li key={item}>{item}</li>)}</ul></section> : null}
    {project.roadmap.blocked.length ? <section className="company-subsection"><h3>{text("Заблокировано / ожидает", "Blocked / pending")}</h3><ul>{project.roadmap.blocked.map((item) => <li key={item}>{item}</li>)}</ul></section> : null}
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

  return <section className="company-page" aria-labelledby="company-projects-title">
    <header className="company-page-head"><p className="eyebrow">F11B · Product Contract Provisional 0.1.0</p><h1 id="company-projects-title">{text("Проекты компании", "Company projects")}</h1><p>{text("Read-only сводка по зарегистрированным проектам. Статус берётся только из канонического roadmap каждого проекта на точном commit SHA.", "Read-only view of registered projects. Status comes only from each project's canonical roadmap at an exact commit SHA.")}</p><p className="boundary-note">{text("Эта страница не изменяет roadmap, не запускает удалённое выполнение и не выдаёт права или Organizational Authority.", "This page does not change roadmaps, invoke remote execution, or grant permission or Organizational Authority.")}</p><button type="button" onClick={refresh}>{text("Обновить из канонических источников", "Refresh canonical sources")}</button></header>
    <div className="company-grid">{state.data.projects.map((project) => <ProjectCard project={project} key={project.id} />)}</div>
  </section>;
}
