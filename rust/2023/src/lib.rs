mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;

pub fn get_funcs(day: u32, input: &String) -> (String, String) {
    match day {
        1 => return (day01::part1(input), day01::part2(input)),
        2 => return (day02::part1(input), day02::part2(input)),
        3 => return (day03::part1(input), day03::part2(input)),
        4 => return (day04::part1(input), day04::part2(input)),
        5 => return (day05::part1(input), day05::part2(input)),
        6 => return (day06::part1(input), day06::part2(input)),
        7 => return (day07::part1(input), day07::part2(input)),
        _ => panic!("Unsupported day {}", day),
    }
}
