#!/bin/bash
OUTPUT="k8s/configmap.yaml"
echo "apiVersion: v1
kind: ConfigMap
metadata:
  name: domain-lists
data:" > $OUTPUT

find domains -type f -name "*.txt" | while read file; do
  key=$(echo "${file#domains/}" | tr '/' '_' | sed 's/.txt//')
  echo "  ${key}.txt: |" >> $OUTPUT
  sed 's/^/    /' "$file" >> $OUTPUT
done

echo "✅ Generated $OUTPUT"
