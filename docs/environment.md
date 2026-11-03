# Environment settings

Explorer currently consumes **no application environment variables** and does not
load `.env` files. No exported settings are required. CLI options own fixture
selection and the optional explicit logging override path. There is therefore no
application boolean parsing or environment precedence layer in Phase 1.

Installed packaged logging defaults are loaded first, followed by an explicit
`--log-override PATH`. With no explicit path, no local override is loaded. Conda
and uv invocations use the same CLI policy. If future keys are introduced, a
central typed system_configuration adapter and tests must precede their use;
this document must list every key, type, accepted values, default, precedence,
export/unset examples and security considerations at that time.

Python and package tools retain their own standard environment behavior; Explorer
does not inspect credentials or redefine those tools' settings.
