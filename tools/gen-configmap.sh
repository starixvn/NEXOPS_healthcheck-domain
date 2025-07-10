#!/bin/bash
OUTPUT="/tmp/gen/k8s/configmap.yaml"
mkdir -p "$(dirname "$OUTPUT")"

echo "apiVersion: v1
kind: ConfigMap
metadata:
  name: domain-lists
data:" > "$OUTPUT"

find domains -type f -name "*.txt" | while read file; do
  key=$(echo "${file#domains/}" | tr '/' '_' | sed 's/.txt//')
  echo "  ${key}.txt: |" >> "$OUTPUT"
  sed 's/^/    /' "$file" >> "$OUTPUT"
done

echo "✅ Generated $OUTPUT"