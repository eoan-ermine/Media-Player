mod terminal_shell;
use terminal_shell::TerminalShell;

fn main() {
    let mut shell: TerminalShell = TerminalShell::new("http://127.0.0.1:8026", "header", "Goodbye");
    shell.start()
}