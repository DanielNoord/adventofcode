use std::env;
use std::fs;

use aoc_2019::get_funcs;

fn do_day(day: u32) {
    let mut input =
        fs::read_to_string(format!("inputs/day{day}.txt")).expect("File should be there");
    input = input.trim_end().to_string();

    let results = get_funcs(day, &input);

    println!("Part 1: {}", results.0);
    println!("Part 2: {}", results.1);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let day_string = &args[1];
    if day_string == "all" {
        for day in 1..25 {
            println!("Running day {}", day);
            do_day(day);
        }
    } else {
        let day: u32 = day_string
            .parse()
            .expect("First argument should be an integer");

        do_day(day)
    }
}
