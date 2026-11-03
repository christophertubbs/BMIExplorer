# Infrastructure configuration

The runtime baseline is the installed package resource
`bmi_explorer/config/log_config.json`. It uses logging.config.dictConfig, leaves
existing loggers enabled, and attaches a stderr handler to the bmi_explorer
namespace at WARNING without propagation. Root logging is preserved for hosts.
Library imports do not configure logging; only CLI composition does.

An optional explicit `--log-override PATH` is applied after initialization. Schema:

```json
{"loggers": {"bmi_explorer.console.session": "DEBUG", "urllib3": "ERROR"}}
```

Top-level `loggers` is required; logger names must be nonempty strings other than
__main__; levels are exact registered logging level names such as DEBUG, INFO,
WARNING, ERROR, CRITICAL. No arbitrary handler construction is allowed in an
override. Unknown fields, malformed JSON, invalid levels, and unreadable explicit
paths fail with a diagnostic and exit status 2. With no explicit path, optional
local files are not searched. Relative explicit paths are resolved by the caller's
current directory; the baseline never depends on the checkout or current directory.

Copy log_override.example.json to a deployment-specific file if needed;
log_override.json is ignored by Git. Do not store secrets in logging configuration.
Business scenario choices are documented separately in docs/business-configuration.md.
