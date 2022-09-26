# Install Rust on Windows 10

# ---- Set install directories ----
# Right-click Windows button, select 'Windows PowerShell (Admin)'
[Environment]::SetEnvironmentVariable('CARGO_HOME', "c:\rust\.cargo", "Machine")
[Environment]::SetEnvironmentVariable('RUSTUP_HOME', "c:\rust\.rustup", "Machine")
# Close window

# ---- Install rust ----
# Download rustup-init.exe
# https://forge.rust-lang.org/infra/other-installation-methods.html
# Open the download folder
# Hold shift & right-click inside of the folder, select 'Open PowerShell window here'
.\rustup-init.exe
# Close window
# Open the $CARGO_HOME\bin folder
# Hold shift & right-click inside of the folder, select 'Open PowerShell window here'
.\rustup.exe component add rust-analyzer
# But that doesn't currently provide the binary, so you have to go download it at:
# https://github.com/rust-lang/rust-analyzer/releases
# Find the right platform, download, unzip to $CARGO_HOME\bin
# Rename the extracted file to 'rust-analyzer.exe'

# ---- Sublime ----
# ctrl + shift + P
# Type 'Install Package Control', press Enter
# ctrl + shift + P
# Type 'Package Control: Install Package', press Enter
# Install 'Rust Enhanced'
# Install 'TOML'
# Install 'RustFmt'
# Install 'LSP'
# Install 'LSP-rust-analyzer'
# Install 'LSP-file-watcher-chokidar'

# ---- Project build & run in Sublime ----
# Open your workspace folder or wherever you're going to create your project.
# Hold shift & right-click inside of the folder, select 'Open PowerShell window here'
cargo new PROJECT_NAME --bin
# Write code in src/main.rs
# ctrl + shift + B once and select 'Cargo - Run'
# You can build (and run) with this from now on with only Ctrl + B.
