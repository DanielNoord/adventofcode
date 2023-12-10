pub fn part1(input: &str) -> String {
    let mut total = 0;
    for line in input.lines() {
        let mut numbers: Vec<i32> =
            Vec::from_iter(line.split(" ").map(|x| x.parse().unwrap()));
        let mut last_numbers: Vec<i32> = Vec::new();

        while !numbers.iter().all(|x| x == &0) {
            last_numbers.push(*numbers.last().unwrap());
            let mut new_numbers: Vec<i32> = vec![numbers[0]];
            for number in &numbers[1..] {
                *new_numbers.last_mut().unwrap() = number - new_numbers.last().unwrap();
                new_numbers.push(*number);
            }
            new_numbers.pop().unwrap();
            numbers = new_numbers.clone();
        }

        total += last_numbers.iter().sum::<i32>();
    }

    assert!(total == 1884768153, "Should be 1884768153");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let mut total = 0;

    for line in input.lines() {
        let mut numbers: Vec<i32> =
            Vec::from_iter(line.split(" ").map(|x| x.parse().unwrap()));
        let mut first_numbers: Vec<i32> = vec![numbers[0]];

        while !numbers.iter().all(|x| x == &0) {
            let mut new_numbers: Vec<i32> = vec![numbers[0]];
            for number in &numbers[1..] {
                *new_numbers.last_mut().unwrap() = number - new_numbers.last().unwrap();
                new_numbers.push(*number);
            }
            first_numbers.push(*new_numbers.first().unwrap());
            new_numbers.pop().unwrap();
            numbers = new_numbers.clone();
        }

        let final_score: i32 = first_numbers.iter().rev().fold(0, |acc, &e| e - acc);
        total += final_score;
    }

    assert!(total == 1031, "Should be 1031");
    total.to_string()
}
