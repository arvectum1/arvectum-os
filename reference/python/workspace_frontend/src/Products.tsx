import { useEffect, useState } from "react";
import { loadProductComposition, WorkspaceApiError } from "./api";
import { useWorkspaceLanguage } from "./i18n";
import { productSurfaceRegistry } from "./product_surfaces/registry";
import type { ProductCompositionProjection } from "./types";

type State = { kind: "loading" } | { kind: "ready"; data: ProductCompositionProjection } | { kind: "error"; code: string };
function navigateTo(href: string) { window.history.pushState({}, "", href); window.dispatchEvent(new PopStateEvent("popstate")); }

export function Products({ productId }: { productId?: string | null }) {
  const { text } = useWorkspaceLanguage();
  const [state, setState] = useState<State>({ kind: "loading" });
  useEffect(() => { let live = true; loadProductComposition().then((data) => { if (live) setState({ kind: "ready", data }); }, (error) => { if (live) setState({ kind: "error", code: error instanceof WorkspaceApiError ? error.code : "PRODUCT_COMPOSITION_UNAVAILABLE" }); }); return () => { live = false; }; }, []);
  if (state.kind === "loading") return <section className="placeholder" aria-live="polite">{text("Загружаем продуктовые контексты…", "Loading product contexts…")}</section>;
  if (state.kind === "error") return <section className="placeholder" role="alert"><h1>{text("Продуктовые контексты недоступны", "Product contexts unavailable")}</h1><p>{text("Текущие продуктовые свидетельства не удалось перепроверить. Ничего не выводится из устаревшего или отсутствующего состояния.", "Current product evidence could not be revalidated. Nothing is inferred from stale or missing product state.")}</p><code>{state.code}</code></section>;
  if (productId) {
    const surface = state.data.products.find((item) => item.id === productId);
    const contribution = productSurfaceRegistry[productId];
    if (!surface || !contribution || contribution.id !== surface.id) return <section className="placeholder" role="alert"><h1>{text("Продуктовый раздел недоступен", "Product surface unavailable")}</h1><p>{text("Запрошенный продуктовый модуль не зарегистрирован в этой точной версии Workspace.", "The requested product contribution is not registered in this exact Workspace release.")}</p></section>;
    return <>{contribution.render(surface)}</>;
  }
  return <section className="products-section" aria-labelledby="products-title">
    <div className="my-work-heading"><div><p className="eyebrow">{text("Продукты", "Products")}</p><h2 id="products-title">{text("Продуктовые контексты", "Product contexts")}</h2><p>{text("Откройте доступный контекст продукта. Подробные операции — в самом продукте.", "Open an available product context. Detailed work remains in the product.")}</p></div></div>
    <div className="status-grid">{state.data.products.map((surface) => <article key={surface.id}><strong>{surface.label}</strong><p>{surface.contour.summary}</p><dl><div><dt>{text("Сейчас доступно", "Available now")}</dt><dd>{text("Проверенный контекст для просмотра", "Verified context for inspection")}</dd></div></dl><a href={`/products/${surface.id}`} onClick={(event) => { event.preventDefault(); navigateTo(`/products/${surface.id}`); }}>{text(`Открыть ${surface.label}`, `Open ${surface.label}`)}</a></article>)}</div>
    <p className="boundary-note">{text("Контексты компонуются, а не сливаются: Workspace не создаёт бизнес-связь между продуктами и не расширяет доступ или полномочия.", "Contexts are composed, not merged: Workspace creates no business relationship between products and does not broaden access or authority.")}</p>
  </section>;
}
