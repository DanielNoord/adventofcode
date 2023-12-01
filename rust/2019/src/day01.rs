pub fn part1(input: &String) -> String {
    let mut total: u32 = 0;
    for line in input.lines() {
        total += line.parse::<u32>().unwrap() / 3 - 2;
    }
    assert!(total == 3335787, "Should be 3335787");
    total.to_string()
}

pub fn part2(input: &String) -> String {
    let mut total: u64 = 0;
    for line in input.lines() {
        let mut value: u64 = line.parse().expect("Should be a positive integer");
        while value > 5 {
            value = value / 3 - 2;
            total += value;
        }
    }
    assert!(total == 5000812, "Should be 5000812");
    total.to_string()
}
