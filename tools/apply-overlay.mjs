#!/usr/bin/env node
// Applies an OpenAPI Overlay 1.0 document to an OpenAPI description.
//
//   node tools/apply-overlay.mjs openapi/openapi.json openapi/overlay.yaml > openapi-presented.json
//
// Supports the target forms the Agilis overlay uses: "$", "$.info" and "$.paths['<path>'].<method>".
// Each action's `update` is merged into its target (objects merged key by key, everything else
// replaced). A target that matches nothing fails: an overlay must never silently drift from the
// contract. No dependencies apart from the `yaml` package, installed by the workflow.

import { readFileSync } from 'node:fs';
import { parse } from 'yaml';

const [specFile, overlayFile] = process.argv.slice(2);
if (!specFile || !overlayFile) {
  console.error('Usage: apply-overlay.mjs <openapi.json> <overlay.yaml>');
  process.exit(2);
}

const spec = JSON.parse(readFileSync(specFile, 'utf8'));
const overlay = parse(readFileSync(overlayFile, 'utf8'));

if (overlay.overlay !== '1.0.0') {
  console.error(`Unsupported overlay version: ${overlay.overlay}`);
  process.exit(1);
}

const isObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const merge = (target, update) => {
  for (const [key, value] of Object.entries(update)) {
    target[key] = isObject(value) && isObject(target[key]) ? merge(target[key], value) : value;
  }
  return target;
};

const resolve = (target) => {
  if (target === '$') return spec;
  if (target === '$.info') return spec.info;
  const m = /^\$\.paths\['([^']+)'\]\.(get|put|post|patch|delete)$/.exec(target);
  return m ? spec.paths?.[m[1]]?.[m[2]] : undefined;
};

let failed = 0;
for (const action of overlay.actions ?? []) {
  if (action.remove) {
    console.error(`Remove actions are not used by this overlay: ${action.target}`);
    failed++;
    continue;
  }
  const node = resolve(action.target);
  if (!isObject(node)) {
    console.error(`Overlay target not found in the contract: ${action.target}`);
    failed++;
    continue;
  }
  merge(node, action.update ?? {});
}

if (failed) process.exit(1);
process.stdout.write(JSON.stringify(spec, null, 2) + '\n');
