import { useCallback, useEffect, useState } from "react";
import { loadWorkspaceContext, logoutWorkspace, WorkspaceApiError } from "./api";
import { useWorkspaceLanguage } from "./i18n";
import { Shell } from "./Shell";
import type { WorkspaceContext } from "./types";

type State =
  | { kind: "loading" }
  | { kind: "ready"; context: WorkspaceContext }
  | { kind: "signedOut" }
  | { kind: "error"; code: string; reloadRequired: boolean };

export function App() {
  const [state, setState] = useState<State>({ kind: "loading" });
  const [, rerenderForRoute] = useState(0);
  const { text } = useWorkspaceLanguage();

  const refresh = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      const context = await loadWorkspaceContext();
      setState({ kind: "ready", context });
    } catch (error) {
      if (error instanceof WorkspaceApiError) {
        setState({ kind: "error", code: error.code, reloadRequired: error.reloadRequired });
      } else {
        setState({ kind: "error", code: "WORKSPACE_UNAVAILABLE", reloadRequired: false });
      }
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);
  useEffect(() => {
    const listener = () => {
      rerenderForRoute((value) => value + 1);
      document.getElementById("workspace-main")?.focus();
    };
    window.addEventListener("popstate", listener);
    return () => window.removeEventListener("popstate", listener);
  }, []);

  if (state.kind === "loading") return <main className="center-state" aria-live="polite">{text("Открываем защищённое рабочее пространство…", "Opening secure workspace…")}</main>;
  if (state.kind === "signedOut") {
    return (
      <main className="center-state">
        <h1>{text("Сеанс завершён", "Signed out")}</h1>
        <p>{text("Серверный сеанс Arvectum OS отозван.", "The server-side Workspace session has been revoked.")}</p>
        <button type="button" onClick={() => void refresh()}>{text("Открыть локальное пространство снова", "Re-open local workspace")}</button>
      </main>
    );
  }
  if (state.kind === "error") {
    return (
      <main className="center-state error-state" role="alert">
        <h1>{text("Рабочее пространство недоступно", "Workspace unavailable")}</h1>
        <p>{state.reloadRequired
          ? text("Версия приложения изменилась. Перезагрузите страницу перед продолжением.", "The application release changed. Reload before continuing.")
          : text("Не удалось безопасно установить контекст доступа.", "Access or security context could not be established.")}</p>
        <code>{state.code}</code>
        <button type="button" onClick={() => state.reloadRequired ? window.location.reload() : void refresh()}>
          {state.reloadRequired ? text("Перезагрузить приложение", "Reload application") : text("Повторить", "Try again")}
        </button>
      </main>
    );
  }

  const logout = async () => {
    try {
      await logoutWorkspace(state.context.session.csrf_token);
      setState({ kind: "signedOut" });
    } catch (error) {
      if (error instanceof WorkspaceApiError) setState({ kind: "error", code: error.code, reloadRequired: error.reloadRequired });
      else setState({ kind: "error", code: "LOGOUT_FAILED", reloadRequired: false });
    }
  };

  return <Shell context={state.context} onLogout={() => void logout()} />;
}
