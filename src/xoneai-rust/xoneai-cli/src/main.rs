//! XoneAI CLI - Command-line interface for XoneAI
//!
//! # Commands
//!
//! - `xoneai chat` - Interactive chat session
//! - `xoneai run <file>` - Run a workflow from YAML file
//! - `xoneai "prompt"` - Single-shot prompt execution
//! - `xoneai --version` - Show version

mod commands;

use anyhow::Result;
use clap::{Parser, Subcommand};

/// XoneAI - High-performance agentic AI framework
#[derive(Parser)]
#[command(name = "xoneai-rust")]
#[command(author = "XoneAI <hello@ai.xone.vn>")]
#[command(version = env!("CARGO_PKG_VERSION"))]
#[command(about = "High-performance, agentic AI framework for Rust")]
#[command(long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,

    /// Single-shot prompt (when no subcommand is given)
    #[arg(trailing_var_arg = true)]
    prompt: Vec<String>,

    /// Model to use (e.g., gpt-4o-mini, claude-3-sonnet)
    #[arg(short, long, default_value = "gpt-4o-mini")]
    model: String,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Subcommand)]
enum Commands {
    /// Start an interactive chat session
    Chat {
        /// Model to use
        #[arg(short, long, default_value = "gpt-4o-mini")]
        model: String,

        /// System instructions
        #[arg(short, long)]
        instructions: Option<String>,
    },

    /// Run a workflow from YAML file
    Run {
        /// Path to the YAML workflow file
        file: String,

        /// Enable verbose output
        #[arg(short, long)]
        verbose: bool,
    },

    /// Execute a single prompt
    Prompt {
        /// The prompt to execute
        text: String,

        /// Model to use
        #[arg(short, long, default_value = "gpt-4o-mini")]
        model: String,
    },
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::from_default_env()
                .add_directive(tracing::Level::INFO.into()),
        )
        .init();

    let cli = Cli::parse();

    match cli.command {
        Some(Commands::Chat {
            model,
            instructions,
        }) => commands::chat::run(model, instructions).await,
        Some(Commands::Run { file, verbose }) => commands::run::run(file, verbose).await,
        Some(Commands::Prompt { text, model }) => commands::prompt::run(text, model).await,
        None => {
            // If no subcommand but prompt provided, run single-shot
            if !cli.prompt.is_empty() {
                let text = cli.prompt.join(" ");
                commands::prompt::run(text, cli.model).await
            } else {
                // No command and no prompt - show help
                println!("XoneAI - High-performance agentic AI framework\n");
                println!("Usage:");
                println!("  xoneai chat              Start interactive chat");
                println!("  xoneai run <file>        Run workflow from YAML");
                println!("  xoneai \"<prompt>\"        Single-shot prompt");
                println!("\nOptions:");
                println!("  -m, --model <MODEL>         Model to use [default: gpt-4o-mini]");
                println!("  -v, --verbose               Enable verbose output");
                println!("  -h, --help                  Show help");
                println!("  -V, --version               Show version");
                Ok(())
            }
        }
    }
}
