import { useState } from "react";
import { useWorkspaceLanguage } from "../i18n";
import type { ProductSurfaceContext } from "../types";

export function TenderOperatorSurface({ surface }: { surface: ProductSurfaceContext }) {
  const { text } = useWorkspaceLanguage();
  const [technicalOpen, setTechnicalOpen] = useState(false);
  return <section className="hero" aria-labelledby="tender-surface-title">
    <p className="eyebrow">{text("Продуктовый контекст", "Product context")}</p>
    <h1 id="tender-surface-title">Tender Operator</h1>
    <p>{surface.contour.summary}</p>
    <div className="status-grid"><article><span>{text("Сейчас доступно", "Available now")}</span><strong>{text("Проверенный контекст Tender Operator", "Verified Tender Operator context")}</strong><p>{text("Рабочие product-specific операции остаются в продукте до появления соответствующей управляемой точки входа.", "Product-specific work remains in the product until an applicable governed entry point exists.")}</p></article><article><span>{text("Следующий шаг", "Next step")}</span><strong>{text("Открыть и проверить контекст", "Open and inspect context")}</strong><p>{text("Эта композиция доступна только для чтения.", "This composed surface is read-only.")}</p></article></div>
    <details><summary onClick={() => setTechnicalOpen((open) => !open)}>{text("Технические сведения", "Technical details")}</summary>{technicalOpen ? <dl><div><dt>Product Contract</dt><dd>{surface.product_contract.id} · {surface.product_contract.lifecycle} {surface.product_contract.version}</dd></div><div><dt>{text("Общие зависимости", "Shared dependencies")}</dt><dd>{surface.contour.shared_dependencies.join(", ")}</dd></div><div><dt>{text("Источник и авторитет", "Source and authority")}</dt><dd>{surface.contour.source_authority}</dd></div><div><dt>{text("Репозиторий", "Repository")}</dt><dd>{surface.repository}</dd></div><div><dt>{text("Версия продукта", "Product release")}</dt><dd>{surface.technical.product_release_sha ?? text("Не раскрыта сохранёнными свидетельствами", "Not disclosed by retained evidence")}</dd></div><div><dt>{text("Свидетельства", "Evidence")}</dt><dd>{surface.technical.evidence_refs.join(", ")}</dd></div></dl> : null}</details>
  </section>;
}
