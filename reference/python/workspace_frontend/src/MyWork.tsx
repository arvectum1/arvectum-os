import { useCallback, useEffect, useState } from "react";
import { loadMyWork, WorkspaceApiError } from "./api";
import { useWorkspaceLanguage } from "./i18n";
import type {
  AttentionGroup,
  AttentionItem,
  AttentionUrgency,
  MyWorkProjection,
} from "./types";

type LoadState =
  | { kind: "loading" }
  | { kind: "ready"; projection: MyWorkProjection }
  | { kind: "error"; code: string; reloadRequired: boolean };
const urgencyOrder: Record<AttentionUrgency, number> = {
  high: 0,
  medium: 1,
  low: 2,
};

function currentFocus(): string | null {
  return new URLSearchParams(window.location.search).get("focus");
}
function showingScenarios(): boolean {
  return new URLSearchParams(window.location.search).get("mode") === "scenario";
}
function pushWorkspaceHref(href: string): void {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}
function governedContextHref(item: AttentionItem): string | null {
  return item.evidence_mode === "live" &&
    item.kind === "waiting-input" &&
    item.technical_evidence_available
    ? "/governed"
    : null;
}

export function MyWork({ embedded = false }: { embedded?: boolean }) {
  const { language, text } = useWorkspaceLanguage();
  const groupLabels: Record<AttentionGroup, string> = {
    "decision-required": text(
      "Требуется решение / ввод",
      "Decision / input required",
    ),
    "blocked-failed": text("Заблокировано / ошибка", "Blocked / failed"),
    "reconciliation-required": text(
      "Требуется сверка",
      "Awaiting reconciliation",
    ),
    "recent-outcome": text(
      "Недавний важный результат",
      "Recent important outcome",
    ),
    informational: text("Информация", "Informational"),
  };
  const kindLabels: Record<AttentionItem["kind"], string> = {
    "waiting-approval": text("Ожидает согласования", "Waiting approval"),
    "waiting-input": text("Ожидает ввода", "Waiting input"),
    "reconciliation-required": text(
      "Требуется сверка",
      "Reconciliation required",
    ),
    "guarded-action-failed": text(
      "Управляемое действие завершилось ошибкой",
      "Guarded action failed",
    ),
    "recoverable-system-condition": text(
      "Системное состояние",
      "System condition",
    ),
    "recent-outcome": text("Недавний результат", "Recent outcome"),
    informational: text("Информация", "Informational"),
  };
  const urgencyLabels: Record<AttentionUrgency, string> = {
    high: text("Высокая", "High"),
    medium: text("Средняя", "Medium"),
    low: text("Низкая", "Low"),
  };
  const displayTime = (value: string | null): string => {
    if (!value)
      return text(
        "Время наблюдения недоступно",
        "Observation time unavailable",
      );
    const parsed = new Date(value);
    return Number.isNaN(parsed.getTime())
      ? value
      : parsed.toLocaleString(language === "ru" ? "ru-RU" : "en-US");
  };
  const [state, setState] = useState<LoadState>({ kind: "loading" });
  const [group, setGroup] = useState<AttentionGroup | "all">("all");
  const [urgency, setUrgency] = useState<AttentionUrgency | "all">("all");
  const [sort, setSort] = useState<"urgency" | "newest">("urgency");
  const refresh = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      setState({ kind: "ready", projection: await loadMyWork() });
    } catch (error) {
      setState(
        error instanceof WorkspaceApiError
          ? {
              kind: "error",
              code: error.code,
              reloadRequired: error.reloadRequired,
            }
          : {
              kind: "error",
              code: "MY_WORK_UNAVAILABLE",
              reloadRequired: false,
            },
      );
    }
  }, []);
  useEffect(() => {
    void refresh();
  }, [refresh]);
  const focusId = embedded ? null : currentFocus();
  const scenarioView = !embedded && showingScenarios();
  const titleId = embedded ? "home-my-work-title" : "my-work-title";
  const Heading = embedded ? "h2" : "h1";
  if (state.kind === "loading")
    return (
      <section
        className={`my-work${embedded ? " my-work-embedded" : ""}`}
        aria-live="polite"
      >
        <p>
          {text(
            "Загружаем задачи, требующие внимания…",
            "Loading current attention sources…",
          )}
        </p>
      </section>
    );
  if (state.kind === "error")
    return (
      <section
        className={`my-work my-work-error${embedded ? " my-work-embedded" : ""}`}
        role="alert"
      >
        <p className="eyebrow">{text("Задачи", "Tasks")}</p>
        <Heading>
          {text("Список задач недоступен.", "Tasks are unavailable.")}
        </Heading>
        <p>
          {state.reloadRequired
            ? text(
                "Версия приложения изменилась. Перезагрузите страницу.",
                "The application release changed. Reload before relying on this projection.",
              )
            : text(
                "Не удалось безопасно определить текущую область источников. Детали защищённых задач не показываются.",
                "Current source scope could not be safely resolved. No protected work-item detail is shown.",
              )}
        </p>
        <code>{state.code}</code>
        <button
          type="button"
          onClick={() =>
            state.reloadRequired ? window.location.reload() : void refresh()
          }
        >
          {state.reloadRequired
            ? text("Перезагрузить", "Reload application")
            : text("Повторить", "Try again")}
        </button>
      </section>
    );
  const projection = state.projection;
  const scoped = projection.items.filter((item) =>
    scenarioView
      ? item.evidence_mode === "scenario"
      : item.evidence_mode === "live",
  );
  const filtered = scoped
    .filter((item) => group === "all" || item.group === group)
    .filter((item) => urgency === "all" || item.urgency === urgency)
    .sort((left, right) => {
      if (sort === "urgency") {
        const delta = urgencyOrder[left.urgency] - urgencyOrder[right.urgency];
        if (delta !== 0) return delta;
      }
      return (
        (Date.parse(right.observed_at ?? "") || 0) -
        (Date.parse(left.observed_at ?? "") || 0)
      );
    });
  const visible = embedded ? filtered.slice(0, 3) : filtered;
  const focused = focusId
    ? scoped.find((item) => item.id === focusId)
    : undefined;
  const detailHref = (item: AttentionItem) =>
    item.evidence_mode === "scenario"
      ? `${item.open_href}&mode=scenario`
      : item.open_href;
  const navigateTo =
    (item: AttentionItem) => (event: React.MouseEvent<HTMLAnchorElement>) => {
      event.preventDefault();
      if (item.open_href.startsWith("/my-work?focus="))
        pushWorkspaceHref(detailHref(item));
    };
  const navigateContext =
    (href: string) => (event: React.MouseEvent<HTMLAnchorElement>) => {
      event.preventDefault();
      pushWorkspaceHref(href);
    };
  const homeCopy = (item: AttentionItem) =>
    item.kind === "waiting-approval" || item.kind === "waiting-input"
      ? {
          title: text("Требуется решение", "Decision needed"),
          reason: text(
            "Ожидается ваше подтверждение.",
            "Your confirmation is needed.",
          ),
        }
      : item.kind === "reconciliation-required"
        ? {
            title: text("Нужно проверить результат", "Check the result"),
            reason: text(
              "Перед продолжением нужно уточнить текущее состояние.",
              "Confirm the current state before continuing.",
            ),
          }
        : item.kind === "guarded-action-failed" ||
            item.kind === "recoverable-system-condition"
          ? {
              title: text("Процесс требует проверки", "Process needs review"),
              reason: text(
                "Нужно проверить причину и текущий статус.",
                "Check the cause and current status.",
              ),
            }
          : {
              title: text("Важный результат", "Important outcome"),
              reason: text(
                "Откройте контекст, если нужна дополнительная информация.",
                "Open the context if more information is needed.",
              ),
            };
  return (
    <section
      className={`my-work${embedded ? " my-work-embedded" : ""}`}
      aria-labelledby={titleId}
    >
      <div className="my-work-heading">
        <div>
          <p className="eyebrow">
            {scenarioView
              ? text(
                  "Настройки · тестовые сценарии",
                  "Settings · test scenarios",
                )
              : text("Текущие задачи", "Current tasks")}
          </p>
          <Heading id={titleId}>
            {scenarioView
              ? text("Тестовые сценарии", "Test scenarios")
              : text("Требует внимания", "Needs attention")}
          </Heading>
          <p>
            {scenarioView
              ? text(
                  "Сценарные данные отделены от обычной работы и не являются живыми событиями.",
                  "Scenario data is separate from ordinary work and is not live activity.",
                )
              : text(
                  "Показываются только текущие задачи из live-источников.",
                  "Only current tasks from live sources are shown.",
                )}
          </p>
        </div>
        {embedded ? (
          <a
            className="quiet-link"
            href="/work"
            onClick={(e) => {
              e.preventDefault();
              pushWorkspaceHref("/work");
            }}
          >
            {text("Открыть задачи", "Open tasks")}
          </a>
        ) : (
          <button
            type="button"
            className="quiet-button"
            onClick={() => void refresh()}
          >
            {text("Обновить", "Refresh")}
          </button>
        )}
      </div>
      <div
        className={`projection-health projection-health-${projection.health.state}`}
        role="status"
      >
        <strong>
          {projection.health.state === "fresh"
            ? text("Актуально", "Current")
            : projection.health.state === "stale"
              ? text("Устарело", "Stale")
              : text("Ограничено", "Degraded")}
        </strong>
        <span>{projection.health.message}</span>
        <small>
          {text("Проверено", "Checked")}{" "}
          {displayTime(projection.health.observed_at)}
        </small>
      </div>
      <p className="boundary-note">
        {embedded
          ? text(
              "Просмотр задач не даёт разрешений или полномочий.",
              "Viewing tasks does not grant permission or authority.",
            )
          : text(
              "Эта очередь не является источником полномочий. Видимость задачи не выдаёт разрешение и не заменяет согласование.",
              "This queue is non-authoritative. Visibility does not grant permission or replace approval.",
            )}
      </p>
      {!embedded && focused ? (
        <article className="attention-detail">
          <p className="eyebrow">
            {text("Выбранная задача", "Focused work item")} ·{" "}
            {kindLabels[focused.kind]}
          </p>
          <h2>{focused.title}</h2>
          <p>{focused.reason}</p>
          <dl>
            <div>
              <dt>{text("Почему сейчас", "Why now")}</dt>
              <dd>{groupLabels[focused.group]}</dd>
            </div>
            <div>
              <dt>
                {text("Следующий допустимый шаг", "Legitimate next step")}
              </dt>
              <dd>{focused.next_step}</dd>
            </div>
          </dl>
          <section className="technical-details">
            <h3>{text("Исходные данные", "Source data")}</h3>
            <dl>
              <div>
                <dt>{text("Источник", "Source")}</dt>
                <dd>{focused.source}</dd>
              </div>
              <div>
                <dt>{text("Режим данных", "Evidence mode")}</dt>
                <dd>
                  {focused.evidence_mode === "scenario"
                    ? text("Тестовый сценарий", "Test scenario")
                    : text("Текущий источник", "Live source")}
                </dd>
              </div>
            </dl>
          </section>
          {focused.evidence_mode === "scenario" ? (
            <p className="scenario-note">
              {text(
                "Контролируемый сценарий — не живое событие.",
                "Controlled scenario evidence — not a live occurrence.",
              )}
            </p>
          ) : null}
          {governedContextHref(focused) ? (
            <a
              className="context-action-link"
              href="/governed"
              onClick={navigateContext("/governed")}
            >
              {text("Открыть контекст выполнения", "Open execution context")}
            </a>
          ) : null}
          <a
            href={scenarioView ? "/my-work?mode=scenario" : "/my-work"}
            onClick={(e) => {
              e.preventDefault();
              pushWorkspaceHref(
                scenarioView ? "/my-work?mode=scenario" : "/my-work",
              );
            }}
          >
            {text("Назад к списку", "Back to queue")}
          </a>
        </article>
      ) : !embedded && focusId ? (
        <div className="attention-unavailable" role="status">
          <strong>
            {text(
              "Задача недоступна в текущем представлении.",
              "Work item is unavailable in this view.",
            )}
          </strong>
          <p>
            {text(
              "Она могла стать неактуальной или недоступной. Защищённые сведения о существовании не раскрываются.",
              "It may no longer be current or authorized. No protected existence detail is disclosed.",
            )}
          </p>
        </div>
      ) : null}
      {!embedded ? (
        <div className="queue-toolbar">
          <label>
            {text("Состояние работы", "Work state")}
            <select
              value={group}
              onChange={(e) =>
                setGroup(e.target.value as AttentionGroup | "all")
              }
            >
              <option value="all">
                {text("Все видимые задачи", "All visible tasks")}
              </option>
              {Object.entries(groupLabels).map(([v, l]) => (
                <option key={v} value={v}>
                  {l}
                </option>
              ))}
            </select>
          </label>
          <label>
            {text("Срочность", "Urgency")}
            <select
              value={urgency}
              onChange={(e) =>
                setUrgency(e.target.value as AttentionUrgency | "all")
              }
            >
              <option value="all">{text("Любая", "All urgency")}</option>
              <option value="high">{text("Высокая", "High")}</option>
              <option value="medium">{text("Средняя", "Medium")}</option>
              <option value="low">{text("Низкая", "Low")}</option>
            </select>
          </label>
          <label>
            {text("Сортировка", "Sort")}
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value as "urgency" | "newest")}
            >
              <option value="urgency">
                {text("Сначала срочные", "Urgency first")}
              </option>
              <option value="newest">
                {text("Сначала новые", "Newest first")}
              </option>
            </select>
          </label>
        </div>
      ) : null}
      <div className="queue-summary">
        {embedded && scoped.length > visible.length
          ? text(
              `Показано ${visible.length} из ${scoped.length}`,
              `Showing ${visible.length} of ${scoped.length} visible items`,
            )
          : text(
              `Видимых задач: ${visible.length}`,
              `${visible.length} visible item${visible.length === 1 ? "" : "s"}`,
            )}
      </div>
      {visible.length === 0 ? (
        <div className="empty-queue">
          <strong>
            {scenarioView
              ? text(
                  "Тестовых сценариев нет.",
                  "No test scenarios are available.",
                )
              : text(
                  "Сейчас нет задач, требующих вашего решения.",
                  "There are no tasks requiring your decision now.",
                )}
          </strong>
          {!scenarioView ? (
            <p>
              {text(
                "Это не означает, что вне текущей авторизованной области нет защищённой работы.",
                "This does not assert that no protected work exists outside the current authorized scope.",
              )}
            </p>
          ) : null}
        </div>
      ) : (
        <div className="attention-list">
          {visible.map((item) =>
            embedded ? (
              <article
                className="attention-card attention-card-home"
                key={item.id}
              >
                <div className="attention-card-topline">
                  <span className={`urgency urgency-${item.urgency}`}>
                    {text(
                      `${urgencyLabels[item.urgency]} срочность`,
                      `${urgencyLabels[item.urgency]} urgency`,
                    )}
                  </span>
                </div>
                <h3>{homeCopy(item).title}</h3>
                <p>{homeCopy(item).reason}</p>
                <div className="attention-card-footer">
                  <a
                    className="home-item-action"
                    href={detailHref(item)}
                    onClick={navigateTo(item)}
                  >
                    {text("Открыть", "Open")}
                  </a>
                </div>
              </article>
            ) : (
              <article className="attention-card" key={item.id}>
                <div className="attention-card-topline">
                  <span className={`urgency urgency-${item.urgency}`}>
                    {text(
                      `${urgencyLabels[item.urgency]} срочность`,
                      `${urgencyLabels[item.urgency]} urgency`,
                    )}
                  </span>
                  <span>{kindLabels[item.kind]}</span>
                  {item.evidence_mode === "scenario" ? (
                    <span>{text("Тестовый сценарий", "Test scenario")}</span>
                  ) : null}
                </div>
                <h2>{item.title}</h2>
                <p>{item.reason}</p>
                <dl>
                  <div>
                    <dt>{text("Источник", "Source")}</dt>
                    <dd>{item.source}</dd>
                  </div>
                  <div>
                    <dt>{text("Следующий шаг", "Next step")}</dt>
                    <dd>{item.next_step}</dd>
                  </div>
                </dl>
                <div className="attention-card-footer">
                  <small>{displayTime(item.observed_at)}</small>
                  <div className="attention-actions">
                    <a href={detailHref(item)} onClick={navigateTo(item)}>
                      {text("Открыть", "Open")}
                    </a>
                    {governedContextHref(item) ? (
                      <a
                        href="/governed"
                        onClick={navigateContext("/governed")}
                      >
                        {text("Открыть выполнение", "Open execution context")}
                      </a>
                    ) : null}
                  </div>
                </div>
              </article>
            ),
          )}
        </div>
      )}
    </section>
  );
}
