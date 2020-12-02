use std::io::{self, Read};

#[derive(serde::Serialize)]
pub struct Order<'b> {
    pub command: &'b str,
    pub args: Vec<&'b str>
}

pub struct TerminalShell<'a> {
    client: reqwest::blocking::Client,
    server_addr: &'a str,
    header: &'a str,
    footer: &'a str,
}
impl<'a> TerminalShell<'a> {
    pub fn new(server_addr: &'a str, header: &'a str, footer: &'a str) -> Self {
        Self {
            client: reqwest::blocking::Client::new(),
            server_addr,
            header,
            footer,
        }
    }

    pub fn parse_input(input: &'a str) -> Order<'a> {
        let mut data = input.trim().splitn(2, " ");

        let command: &str = data.nth(0).expect("Error");
        let args: Vec<&str> = {
            if let Some(args_str) = data.nth(0) {
                args_str.split(" ").collect()
            } else {
                Vec::new()
            }
        };
        Order {
            command,
            args
        }
    }

    pub fn send_to_server(&self, order: &Order) -> Result<reqwest::blocking::Response, reqwest::Error> {
        self.client.post(self.server_addr).json(order).send()
    }

    pub fn start(&mut self) {
        println!("{}", self.header);

        let mut direction_input = String::new();
        while let Ok(size) = io::stdin().read_line(&mut direction_input) {
            if size != 0 {
                let order = TerminalShell::parse_input(&direction_input);
                if let Err(e) = self.send_to_server(&order) {
                    println!("Error occured while sending order to server")
                }
                direction_input.clear();
            }
        }
        println!("{}", self.footer)
    }
}