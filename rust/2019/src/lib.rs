mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod intcode;

pub fn get_funcs(day: u32, input: &str) -> (String, String) {
    match day {
        1 => (day01::part1(input), day01::part2(input)),
        2 => (day02::part1(input), day02::part2(input)),
        3 => (day03::part1(input), day03::part2(input)),
        4 => (day04::part1(input), day04::part2(input)),
        5 => (day05::part1(input), day05::part2(input)),
        6 => (day06::part1(input), day06::part2(input)),
        _ => panic!("Unsupported day {}", day),
    }
}
