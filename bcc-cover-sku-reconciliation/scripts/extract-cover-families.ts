#!/usr/bin/env node
/**
 * Extract clean cover family data from the La-Z-Boy cover workbook.
 *
 * Source sheets:
 * - MASTER FABRICS
 * - MASTER LEATHER
 *
 * Output:
 * - JSON with schemaVersion, generatedAt, and coverFamilies[]
 *
 * Scope intentionally kept narrow:
 * - Keeps only cover information agreed for the clean workbook source.
 * - Does not include generated SKU IDs; seriesNumber + colorCode can derive those later.
 * - Does not infer BCC-only data.
 * - Uses workbook formatting only to determine color-level dropStatus.
 *
 * Run example:
 *   npx tsx scripts/extract-cover-families.ts \
 *     --input "data/April 2026 Cover Information List FINAL (v.5.01.2026).xlsx" \
 *     --output "data/cover-families.json"
 *
 * Dry run:
 *   npx tsx scripts/extract-cover-families.ts --input "data/workbook.xlsx" --dry-run
 */

import ExcelJS from "exceljs";
import { existsSync } from "node:fs";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readdirSync } from "node:fs";

type CoverType = "fabric" | "leather";
type DropStatus = "active" | "dropped";

type CoverColor = {
  colorCode: string;
  colorName: string;
  dropStatus: DropStatus;
};

type CoverFamily = {
  seriesNumber: string;
  patternName: string;
  coverType: CoverType;
  introDate?: string;
  dot?: string;
  specialty: string[];
  cleaningCode?: string;
  capCode?: string;
  faceContents?: string;
  description?: string;
  colors: CoverColor[];
};

type CoverFamilyDocument = {
  schemaVersion: "1.0.0";
  generatedAt: string;
  coverFamilies: CoverFamily[];
};

type CliOptions = {
  input?: string;
  output: string;
  dryRun: boolean;
};

type HeaderMap = Record<string, number>;

type ColorLine = {
  lineIndex: number;
  colorCode: string;
  colorName: string;
  dropStatus: DropStatus;
};

type RichChar = {
  ch: string;
  dropped: boolean;
};

class ExtractionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ExtractionError";
  }
}

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_OUTPUT = path.resolve(process.cwd(), "data", "cover-families.json");

// Dot / classification mappings. These become a single decoded business value in output.
const FABRIC_DOT: Record<string, string> = {
  N: "Normal Fabric",
  M: "Medium Fabric",
  P: "Performance Fabric",
};

const LEATHER_DOT: Record<string, string> = {
  A: "Authentic Leather",
  P: "Performance Leather",
  N: "Nubuck Leather",
};

// Specialty mappings. These align conceptually with BCC addedMaterialTypes.
const SPECIALTY_FABRIC: Record<string, string> = {
  I: "iClean",
  C: "Conserve",
  A: "Antimicrobial",
  PF: "Pet Friendly",
  N: "Nanobionic",
  "W*B": "Bleach Cleanable",
};

const SPECIALTY_LEATHER: Record<string, string> = {
  A: "Antimicrobial",
  C: "Crypton",
  I: "iClean",
};

const COLOR_LINE_RE = /^(\d{2})\s*[=\-]\s*(.+?)\s*$/;
const SERIES_RE = /^[A-Z]+\d+$/;

const FABRIC_REQUIRED_HEADERS = [
  "seriesNumber",
  "patternName",
  "colors",
  "introDate",
  "wearability",
  "cleaningCode",
  "description",
];

const LEATHER_REQUIRED_HEADERS = [
  "seriesNumber",
  "patternName",
  "colors",
  "introDate",
  "leatherDot",
  "cleaningCode",
  "description",
];

function parseArgs(argv: string[]): CliOptions {
  const opts: CliOptions = {
    output: DEFAULT_OUTPUT,
    dryRun: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--input" || arg === "-i") {
      opts.input = argv[++i];
    } else if (arg === "--output" || arg === "-o") {
      opts.output = argv[++i];
    } else if (arg === "--dry-run") {
      opts.dryRun = true;
    } else if (arg === "--help" || arg === "-h") {
      printHelpAndExit();
    } else {
      throw new ExtractionError(`Unknown argument: ${arg}`);
    }
  }

  if (!opts.input) {
    opts.input = findDefaultWorkbook();
  }

  opts.input = path.resolve(process.cwd(), opts.input);
  opts.output = path.resolve(process.cwd(), opts.output);

  return opts;
}

function printHelpAndExit(): never {
  console.log(`Usage:
  npx tsx scripts/extract-cover-families.ts --input <workbook.xlsx> [--output <cover-families.json>] [--dry-run]

Options:
  --input, -i    Path to cover workbook. If omitted, searches ./data for one matching *Cover Information List*.xlsx.
  --output, -o   Output JSON path. Default: data/cover-families.json
  --dry-run      Parse and validate without writing output.
  --help, -h     Show this help.
`);
  process.exit(0);
}

function findDefaultWorkbook(): string {
  const candidates = [
    path.resolve(process.cwd(), "data"),
    path.resolve(SCRIPT_DIR, "..", "data"),
  ];

  const matches: string[] = [];
  for (const dir of candidates) {
    if (!existsSync(dir)) continue;
    const names = readdirSync(dir);
    for (const name of names) {
      if (/Cover Information List/i.test(name) && /\.xlsx$/i.test(name) && !name.startsWith("~$")) {
        matches.push(path.join(dir, name));
      }
    }
  }

  const unique = [...new Set(matches.map((p) => path.resolve(p)))];
  if (unique.length === 1) return unique[0];

  if (unique.length > 1) {
    throw new ExtractionError(
      `Multiple matching workbooks found. Pass --input explicitly:\n${unique.map((p) => `  - ${p}`).join("\n")}`
    );
  }

  throw new ExtractionError(
    `No input workbook provided and no matching workbook found in data/. Pass --input "path/to/workbook.xlsx".`
  );
}

function normalizeText(value: unknown): string {
  if (value === null || value === undefined) return "";
  if (value instanceof Date) return formatDate(value);
  if (typeof value === "object") {
    const maybe = value as { text?: unknown; richText?: Array<{ text?: unknown }> };
    if (typeof maybe.text === "string") return normalizeWhitespace(maybe.text);
    if (Array.isArray(maybe.richText)) return normalizeWhitespace(maybe.richText.map((r) => String(r.text ?? "")).join(""));
  }
  return normalizeWhitespace(String(value));
}

function normalizeWhitespace(s: string): string {
  return s.replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/[ \t]+/g, " ").trim();
}

function compactMultilineText(value: unknown): string {
  return normalizeText(value)
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .join("\n");
}

function formatDate(d: Date): string {
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function excelSerialDateToIso(serial: number): string {
  // Excel serial date system: day 1 = 1900-01-01, with Excel's historical leap-year bug.
  const utcDays = Math.floor(serial - 25569);
  const utcValue = utcDays * 86400;
  const dateInfo = new Date(utcValue * 1000);
  return dateInfo.toISOString().slice(0, 10);
}

function normalizeDateCell(value: unknown, context: string): string | undefined {
  if (value === null || value === undefined || value === "") return undefined;
  if (value instanceof Date) return formatDate(value);
  if (typeof value === "number") return excelSerialDateToIso(value);

  const s = normalizeText(value);
  if (!s) return undefined;

  const parsed = new Date(s);
  if (!Number.isNaN(parsed.getTime())) return formatDate(parsed);

  throw new ExtractionError(`${context}: cannot parse introDate value "${s}"`);
}

function headerKey(raw: string): string | undefined {
  const s = raw.toLowerCase().replace(/[’']/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  if (!s) return undefined;

  if (/^series( number)?$/.test(s) || s === "series") return "seriesNumber";
  if (s.includes("pattern") && s.includes("name")) return "patternName";
  if (s === "colors" || s.includes("color")) return "colors";
  if (s.includes("sku")) return "skuCount";
  if (s.includes("product line")) return "productLine";
  if (s.includes("intro")) return "introDate";
  if (s.includes("horiz")) return "horizontalRepeat";
  if (s.includes("vertical") || s.includes("vert")) return "verticalRepeat";
  if (s.includes("cap")) return "capCode";
  if (s.includes("face") && s.includes("content")) return "faceContents";
  if (s.includes("back") && s.includes("content")) return "backContents";
  if (s.includes("wearability")) return "wearability";
  if (s.includes("specialty fabric")) return "specialtyFabric";
  if (s.includes("welt")) return "weltPattern";
  if (s.includes("slip")) return "slipCoverProgram";
  if (s.includes("cleaning")) return "cleaningCode";
  if (s.includes("description")) return "description";
  if (s.includes("leather") && s.includes("dot")) return "leatherDot";
  if (s.includes("leather description")) return "leatherDot";
  if (s.includes("specialty leather")) return "specialtyLeather";
  return undefined;
}

function findHeaderRow(ws: ExcelJS.Worksheet, requiredKeys: string[], sheetName: string): { rowNumber: number; headers: HeaderMap } {
  for (let rowNumber = 1; rowNumber <= Math.min(ws.rowCount, 60); rowNumber++) {
    const row = ws.getRow(rowNumber);
    const headers: HeaderMap = {};
    row.eachCell({ includeEmpty: false }, (cell, colNumber) => {
      const key = headerKey(normalizeText(cell.value));
      if (key && headers[key] === undefined) headers[key] = colNumber;
    });

    const hasAll = requiredKeys.every((key) => headers[key] !== undefined);
    if (hasAll) return { rowNumber, headers };
  }

  throw new ExtractionError(`${sheetName}: could not find header row with required headers: ${requiredKeys.join(", ")}`);
}

function cellValue(ws: ExcelJS.Worksheet, rowNumber: number, headers: HeaderMap, key: string): unknown {
  const col = headers[key];
  if (col === undefined) return undefined;
  return ws.getRow(rowNumber).getCell(col).value;
}

function cellText(ws: ExcelJS.Worksheet, rowNumber: number, headers: HeaderMap, key: string): string {
  return normalizeText(cellValue(ws, rowNumber, headers, key));
}

function multilineCellText(ws: ExcelJS.Worksheet, rowNumber: number, headers: HeaderMap, key: string): string {
  return compactMultilineText(cellValue(ws, rowNumber, headers, key));
}

function decodeRequiredCode(map: Record<string, string>, raw: string, context: string): string | undefined {
  const code = raw.trim();
  if (!code) return undefined;
  const decoded = map[code];
  if (!decoded) throw new ExtractionError(`${context}: unknown code "${code}"`);
  return decoded;
}

function splitCodes(raw: string): string[] {
  if (!raw.trim()) return [];
  return raw
    .split(/[;,/\n]+/)
    .map((x) => x.trim())
    .filter(Boolean);
}

function decodeSpecialty(map: Record<string, string>, raw: string, context: string): string[] {
  const out: string[] = [];
  for (const code of splitCodes(raw)) {
    const decoded = map[code];
    if (!decoded) throw new ExtractionError(`${context}: unknown specialty code "${code}"`);
    if (!out.includes(decoded)) out.push(decoded);
  }
  return out;
}

function getRichLines(cell: ExcelJS.Cell): RichChar[][] {
  const value = cell.value as unknown;
  const chars: RichChar[] = [];

  if (
    value &&
    typeof value === "object" &&
    "richText" in value &&
    Array.isArray((value as { richText?: unknown }).richText)
  ) {
    const richText = (value as { richText: Array<{ text?: unknown; font?: { strike?: boolean; color?: { argb?: string } } }> }).richText;
    for (const run of richText) {
      const text = String(run.text ?? "");
      const argb = run.font?.color?.argb?.toUpperCase();
      const dropped = run.font?.strike === true || argb === "FFFF0000" || Boolean(argb?.endsWith("FF0000"));
      for (const ch of text) chars.push({ ch, dropped });
    }
  }

  if (chars.length === 0) return [];

  const lines: RichChar[][] = [];
  let current: RichChar[] = [];
  for (const item of chars) {
    if (item.ch === "\n") {
      lines.push(current);
      current = [];
    } else {
      current.push(item);
    }
  }
  lines.push(current);
  return lines;
}

function dropStatusForLine(richLine: RichChar[] | undefined, context: string): DropStatus {
  if (!richLine) return "active";

  const nonWhitespace = richLine.filter((x) => !/\s/.test(x.ch));
  if (nonWhitespace.length === 0) return "active";

  const droppedCount = nonWhitespace.filter((x) => x.dropped).length;
  if (droppedCount === 0) return "active";
  if (droppedCount === nonWhitespace.length) return "dropped";

  throw new ExtractionError(`${context}: mixed active/dropped formatting in one color line`);
}

function parseColorLines(cell: ExcelJS.Cell, context: string): ColorLine[] {
  const text = normalizeText(cell.value);
  const richLines = getRichLines(cell);
  const out: ColorLine[] = [];

  if (!text) return out;

  const lines = text.split("\n");
  for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
    const rawLine = lines[lineIndex].trim();
    if (!rawLine) continue;

    const match = COLOR_LINE_RE.exec(rawLine);
    if (!match) throw new ExtractionError(`${context}: cannot parse color line "${rawLine}"`);

    out.push({
      lineIndex,
      colorCode: match[1],
      colorName: normalizeWhitespace(match[2]),
      dropStatus: dropStatusForLine(richLines[lineIndex], `${context}, color line "${rawLine}"`),
    });
  }

  return out;
}

function expectedSkuCount(ws: ExcelJS.Worksheet, rowNumber: number, headers: HeaderMap): number | undefined {
  const raw = cellText(ws, rowNumber, headers, "skuCount");
  if (!raw) return undefined;
  const n = Number(raw.replace(/[^0-9.-]/g, ""));
  if (!Number.isFinite(n)) return undefined;
  return Math.trunc(n);
}

function addIfPresent<T extends Record<string, unknown>>(obj: T, key: string, value: string | undefined): void {
  const v = value?.trim();
  if (v) obj[key] = v;
}

function validateFamily(family: CoverFamily, context: string): void {
  if (!family.seriesNumber) throw new ExtractionError(`${context}: missing seriesNumber`);
  if (!family.patternName) throw new ExtractionError(`${context}: missing patternName`);
  if (!family.coverType) throw new ExtractionError(`${context}: missing coverType`);
  if (!family.colors.length) throw new ExtractionError(`${context}: no colors parsed`);

  for (const color of family.colors) {
    if (!color.colorCode) throw new ExtractionError(`${context}: color missing colorCode`);
    if (!color.colorName) throw new ExtractionError(`${context}: color ${color.colorCode} missing colorName`);
    if (color.dropStatus !== "active" && color.dropStatus !== "dropped") {
      throw new ExtractionError(`${context}: invalid dropStatus ${color.dropStatus}`);
    }
  }
}

function isLikelyDataRow(seriesNumber: string): boolean {
  return SERIES_RE.test(seriesNumber);
}

function extractFabricFamilies(ws: ExcelJS.Worksheet): CoverFamily[] {
  const { rowNumber: headerRow, headers } = findHeaderRow(ws, FABRIC_REQUIRED_HEADERS, ws.name);
  const families: CoverFamily[] = [];

  for (let rowNumber = headerRow + 1; rowNumber <= ws.rowCount; rowNumber++) {
    const seriesNumber = cellText(ws, rowNumber, headers, "seriesNumber");
    if (!seriesNumber) continue;
    if (!isLikelyDataRow(seriesNumber)) continue;

    const context = `${ws.name} row ${rowNumber} (${seriesNumber})`;
    const colorsCell = ws.getRow(rowNumber).getCell(headers.colors);
    const colors = parseColorLines(colorsCell, context).map((c) => ({
      colorCode: c.colorCode,
      colorName: c.colorName,
      dropStatus: c.dropStatus,
    }));

    const expected = expectedSkuCount(ws, rowNumber, headers);
    if (expected !== undefined && expected !== colors.length) {
      throw new ExtractionError(`${context}: expected ${expected} colors from # of SKU's but parsed ${colors.length}`);
    }

    const dot = decodeRequiredCode(FABRIC_DOT, cellText(ws, rowNumber, headers, "wearability"), context);
    const specialty = decodeSpecialty(SPECIALTY_FABRIC, cellText(ws, rowNumber, headers, "specialtyFabric"), context);

    const family: CoverFamily = {
      seriesNumber,
      patternName: cellText(ws, rowNumber, headers, "patternName"),
      coverType: "fabric",
      specialty,
      colors,
    };

    addIfPresent(family, "introDate", normalizeDateCell(cellValue(ws, rowNumber, headers, "introDate"), context));
    addIfPresent(family, "dot", dot);
    addIfPresent(family, "cleaningCode", cellText(ws, rowNumber, headers, "cleaningCode"));
    addIfPresent(family, "capCode", cellText(ws, rowNumber, headers, "capCode"));
    addIfPresent(family, "faceContents", cellText(ws, rowNumber, headers, "faceContents"));
    addIfPresent(family, "description", multilineCellText(ws, rowNumber, headers, "description"));

    validateFamily(family, context);
    families.push(family);
  }

  return families;
}

function extractLeatherFamilies(ws: ExcelJS.Worksheet): CoverFamily[] {
  const { rowNumber: headerRow, headers } = findHeaderRow(ws, LEATHER_REQUIRED_HEADERS, ws.name);
  const families: CoverFamily[] = [];

  for (let rowNumber = headerRow + 1; rowNumber <= ws.rowCount; rowNumber++) {
    const seriesNumber = cellText(ws, rowNumber, headers, "seriesNumber");
    if (!seriesNumber) continue;
    if (!isLikelyDataRow(seriesNumber)) continue;

    const context = `${ws.name} row ${rowNumber} (${seriesNumber})`;
    const colorsCell = ws.getRow(rowNumber).getCell(headers.colors);
    const colors = parseColorLines(colorsCell, context).map((c) => ({
      colorCode: c.colorCode,
      colorName: c.colorName,
      dropStatus: c.dropStatus,
    }));

    const expected = expectedSkuCount(ws, rowNumber, headers);
    if (expected !== undefined && expected !== colors.length) {
      throw new ExtractionError(`${context}: expected ${expected} colors from # of SKU's but parsed ${colors.length}`);
    }

    const dot = decodeRequiredCode(LEATHER_DOT, cellText(ws, rowNumber, headers, "leatherDot"), context);
    const specialty = decodeSpecialty(SPECIALTY_LEATHER, cellText(ws, rowNumber, headers, "specialtyLeather"), context);

    const family: CoverFamily = {
      seriesNumber,
      patternName: cellText(ws, rowNumber, headers, "patternName"),
      coverType: "leather",
      specialty,
      colors,
    };

    addIfPresent(family, "introDate", normalizeDateCell(cellValue(ws, rowNumber, headers, "introDate"), context));
    addIfPresent(family, "dot", dot);
    addIfPresent(family, "cleaningCode", cellText(ws, rowNumber, headers, "cleaningCode"));
    // No P/S extraction by design. No capCode for leather unless the workbook unexpectedly has a matching column.
    addIfPresent(family, "capCode", cellText(ws, rowNumber, headers, "capCode"));
    addIfPresent(family, "faceContents", cellText(ws, rowNumber, headers, "faceContents"));
    addIfPresent(family, "description", multilineCellText(ws, rowNumber, headers, "description"));

    validateFamily(family, context);
    families.push(family);
  }

  return families;
}

function validateNoDuplicateDerivedIds(families: CoverFamily[]): void {
  const seen = new Map<string, string>();
  for (const family of families) {
    for (const color of family.colors) {
      const derivedId = `${family.seriesNumber}${color.colorCode}`;
      const context = `${family.coverType} ${family.seriesNumber} ${family.patternName} color ${color.colorCode}`;
      const previous = seen.get(derivedId);
      if (previous) {
        throw new ExtractionError(`Duplicate derived cover id ${derivedId}: ${previous}; ${context}`);
      }
      seen.set(derivedId, context);
    }
  }
}

function summarize(families: CoverFamily[]): string {
  const fabricFamilies = families.filter((f) => f.coverType === "fabric").length;
  const leatherFamilies = families.filter((f) => f.coverType === "leather").length;
  const colorCount = families.reduce((sum, f) => sum + f.colors.length, 0);
  const droppedCount = families.reduce(
    (sum, f) => sum + f.colors.filter((c) => c.dropStatus === "dropped").length,
    0
  );

  return [
    `Cover families: ${families.length}`,
    `Fabric families: ${fabricFamilies}`,
    `Leather families: ${leatherFamilies}`,
    `Colors: ${colorCount}`,
    `Dropped colors: ${droppedCount}`,
  ].join("\n");
}

async function main(): Promise<void> {
  const opts = parseArgs(process.argv.slice(2));

  if (!existsSync(opts.input!)) {
    throw new ExtractionError(`Input workbook not found: ${opts.input}`);
  }

  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(opts.input!);

  const fabricSheet = workbook.getWorksheet("MASTER FABRICS");
  const leatherSheet = workbook.getWorksheet("MASTER LEATHER");

  if (!fabricSheet) throw new ExtractionError(`Missing required sheet: MASTER FABRICS`);
  if (!leatherSheet) throw new ExtractionError(`Missing required sheet: MASTER LEATHER`);

  const coverFamilies = [
    ...extractFabricFamilies(fabricSheet),
    ...extractLeatherFamilies(leatherSheet),
  ];

  validateNoDuplicateDerivedIds(coverFamilies);

  coverFamilies.sort((a, b) => {
    const type = a.coverType.localeCompare(b.coverType);
    if (type !== 0) return type;
    return a.seriesNumber.localeCompare(b.seriesNumber) || a.patternName.localeCompare(b.patternName);
  });

  const doc: CoverFamilyDocument = {
    schemaVersion: "1.0.0",
    generatedAt: new Date().toISOString(),
    coverFamilies,
  };

  console.log(summarize(coverFamilies));

  if (opts.dryRun) {
    console.log(`Dry run complete. No file written.`);
    return;
  }

  await mkdir(path.dirname(opts.output), { recursive: true });
  await writeFile(opts.output, JSON.stringify(doc, null, 2) + "\n", "utf8");
  console.log(`Output written: ${opts.output}`);
}

main().catch((err: unknown) => {
  if (err instanceof ExtractionError) {
    console.error(`ERROR: ${err.message}`);
  } else if (err instanceof Error) {
    console.error(err.stack || err.message);
  } else {
    console.error(err);
  }
  process.exit(1);
});
