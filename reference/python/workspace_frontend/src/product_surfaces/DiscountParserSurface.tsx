import { useState } from "react";
import { useWorkspaceLanguage } from "../i18n";
import type { ProductSurfaceContext } from "../types";

export function DiscountParserSurface({ surface }: { surface: ProductSurfaceContext }) {
  const { text } = useWorkspaceLanguage();
  const [technicalOpen, setTechnicalOpen] = useState(false);
  return <section className="hero" aria-labelledby="discount-surface-title">
    <p className="eyebrow">{text("Продуктовый контекст", "Product context")}</p>
    <h1 id="discount-surface-title">Discount Parser</h1>
    <p>{surface.contour.summary}</p>
    <div className="status-grid"><article><span>{text("Сейчас доступно", "Available now")}</span><strong>{text("Проверенный контекст Discount Parser", "Verified Discount Parser context")}</strong><p>{text("Сейчас доступна только проверка сохранённого контекста; публикация и другие операции остаются в продукте.", "Only retained-context inspection is available; publication and other work remain in the product.")}</p></article><article><span>{text("Следующий шаг", "Next step")}</span><strong>{text("Открыть и проверить контекст", "Open and inspect context")}</strong><p>{text("Реконструкция доступна только для чтения и не повторяет внешний эффект.", "Reconstruction is read-only and never replays an external effect.")}</p></article></div>
    <details><summary onClick={() => setTechnicalOpen((open) => !open)}>{text("Технические сведения", "Technical details")}</summary>{technicalOpen ? <dl><div><dt>Product Contract</dt><dd>{surface.product_contract.id} · {surface.product_contract.lifecycle} {surface.product_contract.version}</dd></div><div><dt>{text("Общие зависимости", "Shared dependencies")}</dt><dd>{surface.contour.shared_dependencies.join(", ")}</dd></div><div><dt>{text("Источник и авторитет", "Source and authority")}</dt><dd>{surface.contour.source_authority}</dd></div><div><dt>{text("Репозиторий", "Repository")}</dt><dd>{surface.repository}</dd></div><div><dt>{text("Версия продукта", "Product release")}</dt><dd>{surface.technical.product_release_sha ?? text("Не раскрыта сохранёнными свидетельствами", "Not disclosed by retained evidence")}</dd></div><div><dt>{text("Свидетельства", "Evidence")}</dt><dd>{surface.technical.evidence_refs.join(", ")}</dd></div></dl> : null}</details>
  </section>;
}
