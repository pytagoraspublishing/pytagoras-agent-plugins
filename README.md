# agent-plugins

AI agent plugins and tools for Claude Code.

## Adding This Marketplace

Add this marketplace to Claude Code using one of these methods:

**From GitHub:**

```bash
/plugin marketplace add pytagoras/agent-plugins
```

**From a local clone:**

```bash
/plugin marketplace add /path/to/agent-plugins
```

## Installing Plugins

Once the marketplace is added, install plugins using:

```bash
/plugin install <plugin-name>@pytagoras-plugins
```

For example:

```bash
/plugin install book-latex@pytagoras-plugins
```

## Available Plugins

| Plugin         | Description                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------- |
| `book-latex`   | Manage book projects with LaTeX support - create/edit parts, chapters, sections, and appendices |
| `statusline`   | Custom statusline for Claude Code - displays context usage, session time, git branch, and more  |

## Plugin Commands

After installing a plugin, use `/help` to see available commands, or check the plugin's documentation.

## Uninstalling

To remove a plugin:

```bash
/plugin uninstall <plugin-name>
```

To remove the marketplace:

```bash
/plugin marketplace remove pytagoras-plugins
```


## Testing

1. Run /plugin validate . from repo root to validate marketplace
2. Test with /plugin marketplace add ./ locally                                                              │
3. Test plugin install with /plugin install book-latex@pytagoras-plugins
