<template>
  <div class="markdown-body text-sm leading-relaxed" v-html="rendered" />
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

const props = defineProps({
  text: { type: String, required: true },
});

marked.use({ breaks: true });

const rendered = computed(() =>
  DOMPurify.sanitize(marked.parse(props.text))
);
</script>

<style scoped>
.markdown-body :deep(p)      { margin-bottom: 0.5rem; }
.markdown-body :deep(ul)     { list-style: disc; padding-left: 1.25rem; margin-bottom: 0.5rem; }
.markdown-body :deep(ol)     { list-style: decimal; padding-left: 1.25rem; margin-bottom: 0.5rem; }
.markdown-body :deep(li)     { margin-bottom: 0.25rem; }
.markdown-body :deep(strong) { font-weight: 600; }
.markdown-body :deep(em)     { font-style: italic; }
.markdown-body :deep(code)   { background: #f3f4f6; border-radius: 3px; padding: 0.1rem 0.3rem; font-size: 0.85em; }
.markdown-body :deep(pre)    { background: #f3f4f6; border-radius: 6px; padding: 0.75rem; overflow-x: auto; margin-bottom: 0.5rem; }
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3)     { font-weight: 600; margin-bottom: 0.25rem; }
</style>
