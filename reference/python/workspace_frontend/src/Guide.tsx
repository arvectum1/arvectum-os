import { useWorkspaceLanguage } from "./i18n";

function navigateTo(href: string) {
  window.history.pushState({}, "", href);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function WorkspaceLink({ href, children }: { href: string; children: React.ReactNode }) {
  return <a href={href} onClick={(event) => { event.preventDefault(); navigateTo(href); }}>{children}</a>;
}

export function Guide({ release }: { release: string }) {
  const { text } = useWorkspaceLanguage();

  return <section className="guide-page" aria-labelledby="guide-title">
    <header className="hero">
      <p className="eyebrow">{text("Arvectum OS · Руководство", "Arvectum OS · Guide")}</p>
      <h1 id="guide-title">{text("Что здесь можно делать", "What you can do here")}</h1>
      <p>{text(
        "Это руководство описывает возможности именно той версии Workspace, которая открыта сейчас.",
        "This guide describes the capabilities of the exact Workspace release currently open.",
      )}</p>
      <p><strong>{text("Версия Workspace", "Workspace release")}:</strong> <code>{release}</code></p>
    </header>

    <section aria-labelledby="guide-start-title">
      <h2 id="guide-start-title">{text("С чего начать", "Where to start")}</h2>
      <div className="home-actions" aria-label={text("Переходы из руководства", "Guide shortcuts")}>
        <WorkspaceLink href="/work">{text("Посмотреть задачи", "View tasks")}</WorkspaceLink>
        <WorkspaceLink href="/information">{text("Найти информацию", "Find information")}</WorkspaceLink>
        <WorkspaceLink href="/copilot">{text("Спросить Arvectum AI", "Ask Arvectum AI")}</WorkspaceLink>
      </div>
      <p>{text(
        "Если задач сейчас нет, это нормальное рабочее состояние: используйте поиск по доступному организационному контексту, задайте вопрос Arvectum AI или откройте нужный продуктовый контекст в разделе «Задачи».",
        "If there are no tasks now, that is a normal working state: search the available organizational context, ask Arvectum AI, or open the relevant product context under Tasks.",
      )}</p>
    </section>

    <section aria-labelledby="guide-capabilities-title">
      <h2 id="guide-capabilities-title">{text("Что работает сейчас", "What works now")}</h2>
      <dl>
        <div><dt>{text("Главная", "Home")}</dt><dd>{text("Показывает, что требует вашего внимания сейчас, и даёт короткие переходы к основным действиям.", "Shows what needs your attention now and provides shortcuts to primary actions.")}</dd></div>
        <div><dt>{text("Задачи", "Tasks")}</dt><dd>{text("Показывает только реальные текущие задачи владельца и доступные продуктовые контексты. Тестовые сценарии не выдаются за живую работу.", "Shows only real current owner tasks and available product contexts. Test scenarios are not presented as live work.")}</dd></div>
        <div><dt>{text("Документы", "Documents")}</dt><dd>{text("Ищет и открывает уже доступные Workspace записи, документы и знания с учётом текущих прав и организации.", "Searches and opens records, documents, and knowledge already available to Workspace under current access and organization scope.")}</dd></div>
        <div><dt>Arvectum AI</dt><dd>{text("Отвечает на вопросы по доступному контексту и показывает источники. Ответ — вспомогательный результат: он не является решением, разрешением, организационным полномочием или автоматически подтверждённым знанием.", "Answers questions over available context and shows sources. The answer is assistive output: it is not a decision, permission, organizational authority, or automatically validated knowledge.")}</dd></div>
        <div><dt>{text("Настройки", "Settings")}</dt><dd>{text("Содержат сведения об организации, активность, технические проверки, тестовые сценарии и форму обратной связи для dogfooding.", "Contains organization information, activity, technical checks, test scenarios, and dogfooding feedback.")}</dd></div>
      </dl>
    </section>

    <section aria-labelledby="guide-limits-title">
      <h2 id="guide-limits-title">{text("Чего пока нет", "What is not available yet")}</h2>
      <p>{text(
        "В этой версии ещё нет общего приёма организационных материалов. Через Workspace пока нельзя загрузить логотип или брендбук, шаблон презентации .pptx, шаблон документа .docx, шаблон письма или произвольный файл-источник для последующего использования.",
        "This release does not yet provide general organizational material intake. Workspace cannot yet upload a logo or brandbook, a .pptx presentation template, a .docx document template, an email template, or an arbitrary source file for later use.",
      )}</p>
      <p>{text(
        "Добавление такого механизма проектируется отдельно: сам факт загрузки не должен автоматически делать файл утверждённым знанием, стандартом, решением или источником полномочий.",
        "That mechanism is being designed separately: uploading a file must not automatically make it validated knowledge, a standard, a decision, or a source of authority.",
      )}</p>
    </section>

    <section aria-labelledby="guide-governance-title">
      <h2 id="guide-governance-title">{text("Как Workspace обращается с полномочиями", "How Workspace handles authority")}</h2>
      <p>{text(
        "Поиск, экран, кнопка или ответ ИИ сами по себе ничего не утверждают и не дают новых прав. Существенные изменения канонического состояния выполняются только через предусмотренный управляемый контур с повторной проверкой необходимых условий.",
        "Search results, a screen, a button, or an AI answer do not by themselves approve anything or grant new rights. Consequential canonical changes only occur through the governed path with the required checks revalidated.",
      )}</p>
    </section>
  </section>;
}
