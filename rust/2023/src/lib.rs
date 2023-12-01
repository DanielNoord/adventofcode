mod day01;

pub fn get_funcs(day: u32, input: &String) -> (String, String) {
    match day {
        1 => return (day01::part1(input), day01::part2(input)),
        _ => panic!("Unsupported day {}", day),
    }
}
