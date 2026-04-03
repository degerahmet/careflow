# Markdown Message Component

Create `src/components/MarkdownMessage.vue` to render AI assistant replies as formatted markdown.

## Props

```js
props: {
  content: String  // raw markdown string from the assistant
}
```

## Behavior

- Parse and render `content` as HTML using a lightweight markdown library
- Support: **bold**, _italic_, bullet lists, numbered lists, inline `code`
- Do not support: images, tables, raw HTML blocks (strip or escape them)

## Recommended Library

Use `marked` (already a small, zero-dependency parser):
```js
import { marked } from 'marked'
const html = marked.parse(props.content)
```

Render with `v-html` — since content comes from our own Claude API response (not user input), XSS risk is low, but strip any `<script>` tags as a precaution.

## Styling

Wrap rendered HTML in a `<div class="prose">` — apply minimal prose styles:
- Paragraph spacing
- Bold/italic rendered correctly
- Bullet and numbered lists with left padding and list-style
- Inline code with monospace font and light background

Avoid importing a full typography plugin — write the styles as scoped CSS in the component.

## Notes
- This component is used only in `MemberChatView` for assistant bubbles
- User messages are plain text and should NOT use this component
- The component should be stateless — just a renderer, no reactive state
