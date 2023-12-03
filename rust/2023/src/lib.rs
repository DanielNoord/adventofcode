mod day01;
mod day02;
mod day03;

pub fn get_funcs(day: u32, input: &String) -> (String, String) {
    match day {
        1 => return (day01::part1(input), day01::part2(input)),
        2 => return (day02::part1(input), day02::part2(input)),
        3 => return (day03::part1(input), day03::part2(input)),
        _ => panic!("Unsupported day {}", day),
    }
}
