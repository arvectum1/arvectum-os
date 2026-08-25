import { useCallback, useEffect, useMemo, useState } from "react";
import { loadGovernedExperience, loadMyWork, WorkspaceApiError } from "./api";
import { useWorkspaceLanguage } from "./i18n";
import type { AttentionItem, GovernedExperienceProjection, MyWorkProjection } from "./types";
import "./Activity.css";

type ReadyState = { kind: "ready"; work: MyWorkProjection; governed: GovernedExperienceProjection };
type LoadState = { kind: "loading" } | ReadyState | { kind: "error"; code: string; reloadRequired: boolean };
type ActivityEntry = { id: string; observedAt: string; label: string; title: string; detail: string; source: string; href: string; alert: boolean; scenario: boolean };
const ALERT_GROUPS = new Set(["decision-required", "blocked-failed", "reconciliation-required"]);

function displayTime(value: string, language: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString(language === "ru" ? "ru-RU" : "en-US");
}

export function Activity() {
  const { language, text } = useWorkspaceLanguage();
  const [state, setState] = useState<LoadState>({ kind: "loading" });
  const refresh = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      const [work, governed] = await Promise.all([loadMyWork(), loadGovernedExperience()]);
      setState({ kind: "ready", work, governed });
    } catch (error) {
      if (error instanceof WorkspaceApiError) setState({ kind: "error", code: error.code, reloadRequired: error.reloadRequired });
      else setState({ kind: "error", code: "ACTIVITY_UNAVAILABLE", reloadRequired: false });
    }
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);

  const entries = useMemo(() => {
    if (state.kind !== "ready") return [];
    const attention = state.work.items.filter((item) => item.evidence_mode === "live").map((item: AttentionItem) => ({
      id: `attention-${item.id}`,
      observedAt: item.observed_at ?? state.work.generated_at,
      label: item.group === "recent-outcome" ? text("Зафиксированный результат", "Observed outcome") : item.group === "informational" ? text("Информация", "Observed information") : text("Сигнал внимания", "Attention signal"),
      title: item.title, detail: item.reason, source: item.source, href: item.open_href,
      alert: ALERT_GROUPS.has(item.group), scenario: item.evidence_mode === "scenario",
    }));
    const governed: ActivityEntry = {
      id: "governed-current-state", observedAt: state.governed.generated_at,
      label: text("Состояние управляемого процесса", "Governed state observed"),
      title: `${text("Управляемое выполнение", "Governed execution")}: ${state.governed.execution.status}`,
      detail: state.governed.execution.meaning, source: state.governed.presentation.source, href: "/governed", alert: false, scenario: false,
    };
    return [...attention, governed].sort((a, b) => (Date.parse(b.observedAt) || 0) - (Date.parse(a.observedAt) || 0));
  }, [state, text]);

  if (state.kind === "loading") return <section className="activity-page" aria-live="polite"><p>{text("Загружаем текущую активность…", "Loading current activity sources…")}</p></section>;
  if (state.kind === "error") return <section className="activity-page" role="alert"><p className="eyebrow">{text("Активность", "Activity")}</p><h1>{text("Активность недоступна.", "Activity is unavailable.")}</h1><p>{state.reloadRequired ? text("Версия приложения изменилась. Перезагрузите страницу перед использованием этой проекции.", "The application release changed. Reload before relying on this projection.") : text("Не удалось безопасно перепроверить текущие источники. Сохранённые детали активности скрыты.", "Current source scope could not be safely revalidated. No retained activity detail is shown.")}</p><code>{state.code}</code><button type="button" onClick={() => state.reloadRequired ? window.location.reload() : void refresh()}>{state.reloadRequired ? text("Перезагрузить", "Reload application") : text("Повторить", "Try again")}</button></section>;

  const alerts = entries.filter((entry) => entry.alert);
  return <section className="activity-page" aria-labelledby="activity-title">
    <div className="my-work-heading"><div><p className="eyebrow">{text("Активность", "Activity")}</p><h1 id="activity-title">{text("События и сигналы", "Events and signals")}</h1><p>{text("Наблюдения за текущими процессами и состояниями рабочего пространства.", "Observations of current workspace processes and states.")}</p></div><button type="button" className="quiet-button" onClick={() => void refresh()}>{text("Обновить", "Refresh")}</button></div>
    <p className="boundary-note">{text("Это не хранилище событий, не журнал аудита, не источник уведомительных полномочий и не очередь согласований. Время ниже — время наблюдения, если источник явно не доказывает время события. Статус прочитано/не прочитано не записывается.", "This is not an Event store, audit log, notification authority, approval queue, or source of Organizational Authority. Times below are observation times unless a source explicitly proves occurrence time. No read/unread state is recorded.")}</p>
    <section className="activity-alerts" aria-labelledby="current-alerts-title"><p className="eyebrow">{text("Маршрутизация внимания", "Attention routing")}</p><h2 id="current-alerts-title">{text("Текущие сигналы", "Current alerts")}</h2><p>{text("Сигналы используют ту же семантику, что и «Моя работа»; отдельная модель приоритетов не создаётся.", "Alerts reuse My Work attention semantics; P9.09 does not invent a second priority model.")}</p>{alerts.length === 0 ? <p>{text("В текущей авторизованной проекции нет активных сигналов.", "No current alert is visible in this authorized projection.")}</p> : <div className="attention-list">{alerts.map((entry) => <article className="attention-card" key={`alert-${entry.id}`}><div className="attention-card-topline"><span>{text("Текущий сигнал", "Current alert")}</span>{entry.scenario ? <span>{text("Сценарные данные", "Scenario evidence")}</span> : null}</div><h3>{entry.title}</h3><p>{entry.detail}</p><dl><div><dt>{text("Источник", "Source")}</dt><dd>{entry.source}</dd></div></dl><div className="attention-card-footer"><small>{text("Наблюдалось", "Observed")} {displayTime(entry.observedAt, language)}</small><a href={entry.href}>{text("Открыть контекст", "Inspect context")}</a></div></article>)}</div>}</section>
    <section className="activity-timeline" aria-labelledby="activity-timeline-title"><p className="eyebrow">{text("Лента наблюдений", "Observed timeline")}</p><h2 id="activity-timeline-title">{text("Недавняя видимая активность", "Recent visible activity")}</h2><ol className="activity-list">{entries.map((entry) => <li key={entry.id}><article><div className="attention-card-topline"><span>{entry.label}</span>{entry.scenario ? <span>{text("Сценарные данные", "Scenario evidence")}</span> : null}</div><time dateTime={entry.observedAt}>{displayTime(entry.observedAt, language)}</time><h3>{entry.title}</h3><p>{entry.detail}</p><p><strong>{text("Источник", "Source")}:</strong> {entry.source}</p><a href={entry.href}>{text("Открыть контекст", "Inspect context")}</a></article></li>)}</ol></section>
  </section>;
}
