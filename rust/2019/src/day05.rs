use crate::intcode;

pub fn part1(input: &str) -> String {
    let values: Vec<&str> = input.split(",").collect();
    let result = intcode::parse_intcode(values, 1);
    assert!(result == 6731945, "Should be 6731945");
    result.to_string()
}

pub fn part2(input: &str) -> String {
    let values: Vec<&str> = input.split(",").collect();
    let result = intcode::parse_intcode(values, 5);
    assert!(result == 9571668, "Should be 9571668");
    result.to_string()
}
