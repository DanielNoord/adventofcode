use regex::Regex;

struct GameSet {
    green: u32,
    red: u32,
    blue: u32,
}

fn is_valid(set: GameSet) -> bool {
    if set.red > 12 {
        return false;
    } else if set.green > 13 {
        return false;
    } else if set.blue > 14 {
        return false;
    }
    true
}

pub fn part1(input: &String) -> String {
    let mut total: u32 = 0;
    let green_pat = Regex::new(r"(\d+) green").unwrap();
    let red_pat = Regex::new(r"(\d+) red").unwrap();
    let blue_pat = Regex::new(r"(\d+) blue").unwrap();

    for line in input.lines() {
        let mut is_valid_game: bool = true;

        let mut split = line.split(": ");
        let (_, game_id_as_str) = split.next().unwrap().split_at(5);

        for set_line in split.next().unwrap().split("; ") {
            match green_pat.captures(set_line) {
                Some(caps) => {
                    let value: u32 = caps[1].parse().unwrap();
                    if value > 13 {
                        is_valid_game = false;
                        break;
                    }
                }
                _ => (),
            };
            match red_pat.captures(set_line) {
                Some(caps) => {
                    let value: u32 = caps[1].parse().unwrap();
                    if value > 12 {
                        is_valid_game = false;
                        break;
                    }
                }
                _ => (),
            };
            match blue_pat.captures(set_line) {
                Some(caps) => {
                    let value: u32 = caps[1].parse().unwrap();
                    if value > 14 {
                        is_valid_game = false;
                        break;
                    }
                }
                _ => (),
            };
        }
        if is_valid_game {
            total += game_id_as_str.parse::<u32>().unwrap();
        }
    }
    assert!(total == 2101, "Should be 2101");
    total.to_string()
}

pub fn part2(input: &String) -> String {
    let mut total: u32 = 0;
    let green_pat = Regex::new(r"(\d+) green").unwrap();
    let red_pat = Regex::new(r"(\d+) red").unwrap();
    let blue_pat = Regex::new(r"(\d+) blue").unwrap();

    for line in input.lines() {
        let mut max_red = 0;
        let mut max_green = 0;
        let mut max_blue = 0;

        for set_line in line.split(": ").nth(1).unwrap().split("; ") {
            match green_pat.captures(set_line) {
                Some(caps) => {
                    let value = caps[1].parse().unwrap();
                    if value > max_green {
                        max_green = value;
                    }
                }
                _ => (),
            };
            match red_pat.captures(set_line) {
                Some(caps) => {
                    let value = caps[1].parse().unwrap();
                    if value > max_red {
                        max_red = value;
                    }
                }
                _ => (),
            };
            match blue_pat.captures(set_line) {
                Some(caps) => {
                    let value = caps[1].parse().unwrap();
                    if value > max_blue {
                        max_blue = value;
                    }
                }
                _ => (),
            };
        }
        total += max_green * max_blue * max_red;
    }
    assert!(total == 58269, "Should be 58269");
    total.to_string()
}
