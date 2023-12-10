pub fn part1(input: &str) -> String {
    let mut lines = input.lines();
    let times = lines.next().unwrap().split_ascii_whitespace();
    let mut time_destination_pairs =
        lines.next().unwrap().split_ascii_whitespace().zip(times);

    // Skip the introduction text
    time_destination_pairs.next();

    let mut total_options = 1;
    for (winning_distance, time) in time_destination_pairs
        .map(|x| (x.0.parse::<u32>().unwrap(), x.1.parse::<u32>().unwrap()))
    {
        let mut options_for_time = 0;
        for press_time in 1..time {
            let distance = press_time * (time - press_time);
            if distance > winning_distance {
                options_for_time += 1;
            }
        }
        total_options *= options_for_time;
    }

    assert!(total_options == 1083852, "Should be 1083852");
    total_options.to_string()
}

pub fn part2(input: &str) -> String {
    let mut lines = input.lines();
    let time: u64 = lines
        .next()
        .unwrap()
        .split(": ")
        .nth(1)
        .unwrap()
        .split_ascii_whitespace()
        .collect::<Vec<&str>>()
        .join("")
        .parse()
        .unwrap();
    let max_distance: u64 = lines
        .next()
        .unwrap()
        .split(": ")
        .nth(1)
        .unwrap()
        .split_ascii_whitespace()
        .collect::<Vec<&str>>()
        .join("")
        .parse()
        .unwrap();

    let mut total_options = 0;
    for press_time in 1..time {
        let distance = press_time * (time - press_time);
        if distance > max_distance {
            total_options += 1;
        }
    }

    assert!(total_options == 23501589, "Should be 23501589");
    total_options.to_string()
}
