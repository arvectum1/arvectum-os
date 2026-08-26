#!/usr/bin/env python3
"""Deterministic Productive Workspace code-health inventory for the R32 gate.

The Engineering Standard treats size/complexity thresholds as review signals rather
than automatic architectural law. This tool therefore reports candidates by default
and only fails on unreviewed high signals when ``--strict`` is requested.

No third-party parser is required: Python complexity is a bounded McCabe-style AST
count; TypeScript/TSX is covered by the existing TypeScript compiler and this tool
only reports module size/test inventory for those sources.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PYTHON_ROOTS = (
    Path("workspace_app"),
    Path("workspace_tests"),
)
PYTHON_SINGLE_FILES = (Path("p9_03_workspace.py"),)
FRONTEND_ROOT = Path("workspace_frontend/src")

PREFERRED_COMPLEXITY = 10
REVIEW_COMPLEXITY = 15
FUNCTION_REVIEW_LINES = 60
MODULE_REVIEW_LINES = 800


@dataclass(frozen=True, slots=True)
class FunctionMetric:
    path: str
    qualified_name: str
    line: int
    lines: int
    complexity: int


@dataclass(frozen=True, slots=True)
class ModuleMetric:
    path: str
    lines: int


class ComplexityVisitor(ast.NodeVisitor):
    """Small deterministic McCabe-style counter for one function body."""

    def __init__(self) -> None:
        self.value = 1
        self._root_seen = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not self._root_seen:
            self._root_seen = True
            for item in node.body:
                self.visit(item)
        # Nested function complexity is measured separately.

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if not self._root_seen:
            self._root_seen = True
            for item in node.body:
                self.visit(item)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        # Treat nested lambdas as separate conceptual units rather than inflating
        # the containing function's branch count.
        return

    def visit_If(self, node: ast.If) -> None:
        self.value += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.value += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.value += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.value += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.value += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        self.value += len(node.handlers)
        if node.orelse:
            self.value += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.value += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.value += max(0, len(node.cases) - 1)
        self.generic_visit(node)

    def _visit_comprehension(self, generators: Iterable[ast.comprehension]) -> None:
        for generator in generators:
            self.value += 1 + len(generator.ifs)
            self.visit(generator.target)
            self.visit(generator.iter)
            for condition in generator.ifs:
                self.visit(condition)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node.generators)
        self.visit(node.elt)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node.generators)
        self.visit(node.elt)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node.generators)
        self.visit(node.elt)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node.generators)
        self.visit(node.key)
        self.visit(node.value)


class FunctionCollector(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.scope: list[str] = []
        self.metrics: list[FunctionMetric] = []

    def _record(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        end = node.end_lineno or node.lineno
        visitor = ComplexityVisitor()
        visitor.visit(node)
        name = ".".join([*self.scope, node.name])
        self.metrics.append(
            FunctionMetric(
                path=self.path.as_posix(),
                qualified_name=name,
                line=node.lineno,
                lines=end - node.lineno + 1,
                complexity=visitor.value,
            )
        )
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record(node)


def _python_files() -> list[Path]:
    files: set[Path] = set()
    for root in PYTHON_ROOTS:
        if root.is_dir():
            files.update(path for path in root.rglob("*.py") if "__pycache__" not in path.parts)
    files.update(path for path in PYTHON_SINGLE_FILES if path.is_file())
    return sorted(files)


def _frontend_files() -> list[Path]:
    if not FRONTEND_ROOT.is_dir():
        return []
    return sorted(
        path
        for path in FRONTEND_ROOT.rglob("*")
        if path.is_file() and path.suffix in {".ts", ".tsx", ".js", ".jsx", ".css"}
    )


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def collect() -> tuple[list[ModuleMetric], list[FunctionMetric], list[ModuleMetric]]:
    python_modules: list[ModuleMetric] = []
    functions: list[FunctionMetric] = []
    for path in _python_files():
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=path.as_posix())
        python_modules.append(ModuleMetric(path.as_posix(), len(source.splitlines())))
        collector = FunctionCollector(path)
        collector.visit(tree)
        functions.extend(collector.metrics)

    frontend_modules = [ModuleMetric(path.as_posix(), _line_count(path)) for path in _frontend_files()]
    return python_modules, functions, frontend_modules


def render_report(
    python_modules: list[ModuleMetric],
    functions: list[FunctionMetric],
    frontend_modules: list[ModuleMetric],
) -> tuple[str, bool]:
    high_complexity = sorted(
        (metric for metric in functions if metric.complexity > REVIEW_COMPLEXITY),
        key=lambda item: (-item.complexity, item.path, item.line),
    )
    review_complexity = sorted(
        (metric for metric in functions if PREFERRED_COMPLEXITY < metric.complexity <= REVIEW_COMPLEXITY),
        key=lambda item: (-item.complexity, item.path, item.line),
    )
    long_functions = sorted(
        (metric for metric in functions if metric.lines > FUNCTION_REVIEW_LINES),
        key=lambda item: (-item.lines, item.path, item.line),
    )
    long_modules = sorted(
        [*python_modules, *frontend_modules], key=lambda item: (-item.lines, item.path)
    )
    long_modules = [metric for metric in long_modules if metric.lines > MODULE_REVIEW_LINES]

    frontend_tests = [metric for metric in frontend_modules if ".test." in metric.path]
    python_tests = [metric for metric in python_modules if Path(metric.path).name.startswith("test_")]

    lines = [
        "R32 Productive Workspace code-health inventory",
        "==============================================",
        f"Python modules scanned: {len(python_modules)}",
        f"Python functions/methods scanned: {len(functions)}",
        f"Python test modules: {len(python_tests)}",
        f"Frontend source/style modules scanned: {len(frontend_modules)}",
        f"Frontend test modules: {len(frontend_tests)}",
        "",
        f"Complexity > {REVIEW_COMPLEXITY} (high review signal): {len(high_complexity)}",
    ]
    for metric in high_complexity:
        lines.append(
            f"  HIGH {metric.path}:{metric.line} {metric.qualified_name} "
            f"complexity={metric.complexity} lines={metric.lines}"
        )
    lines.append(f"Complexity {PREFERRED_COMPLEXITY + 1}-{REVIEW_COMPLEXITY} (review candidate): {len(review_complexity)}")
    for metric in review_complexity:
        lines.append(
            f"  REVIEW {metric.path}:{metric.line} {metric.qualified_name} "
            f"complexity={metric.complexity} lines={metric.lines}"
        )
    lines.append(f"Functions > {FUNCTION_REVIEW_LINES} lines (review signal): {len(long_functions)}")
    for metric in long_functions:
        lines.append(
            f"  LONG {metric.path}:{metric.line} {metric.qualified_name} "
            f"lines={metric.lines} complexity={metric.complexity}"
        )
    lines.append(f"Modules > {MODULE_REVIEW_LINES} lines (review signal): {len(long_modules)}")
    for metric in long_modules:
        lines.append(f"  MODULE {metric.path} lines={metric.lines}")

    high_signal = bool(high_complexity or long_modules)
    lines.extend(
        [
            "",
            "Interpretation:",
            "- thresholds are Engineering Standard review signals, not automatic architecture rules;",
            "- TypeScript semantic/static correctness remains enforced by `tsc --noEmit`;",
            "- this inventory does not substitute for tests, security review, dependency audit, or owner evidence.",
        ]
    )
    return "\n".join(lines), high_signal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail when an unreviewed high signal (>15 complexity or >800-line module) exists",
    )
    args = parser.parse_args()
    python_modules, functions, frontend_modules = collect()
    report, high_signal = render_report(python_modules, functions, frontend_modules)
    print(report)
    if args.strict and high_signal:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
