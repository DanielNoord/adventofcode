use std::str::FromStr;

#[derive(Debug, Clone, Copy)]
enum Direction {
    U,
    R,
    D,
    L,
}

impl FromStr for Direction {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.chars().next().unwrap() {
            'U' => Ok(Direction::U),
            'R' => Ok(Direction::R),
            'D' => Ok(Direction::D),
            'L' => Ok(Direction::L),
            _ => panic!("Unsupported direction!"),
        }
    }
}

fn shoelace(points: Vec<(i64, i64)>) -> i64 {
    points
        .windows(2)
        .map(|w| w[0].0 * w[1].1 - w[0].1 * w[1].0)
        .sum::<i64>()
        .abs()
        / 2
}

pub fn part1(input: &str) -> String {
    let mut position: (i64, i64) = (0, 0);
    let mut coords: Vec<(i64, i64)> = Vec::new();
    let mut perimeter = 0;

    for line in input.lines() {
        let mut split_line = line.split_ascii_whitespace();
        let direction: Direction = split_line.next().unwrap().parse().unwrap();
        let distance: i64 = split_line.next().unwrap().parse().unwrap();

        perimeter += distance;

        match direction {
            Direction::U => position = (position.0 - distance, position.1),
            Direction::R => position = (position.0, position.1 + distance),
            Direction::D => position = (position.0 + distance, position.1),
            Direction::L => position = (position.0, position.1 - distance),
        }
        coords.push((position.0, position.1));
    }

    let result = shoelace(coords.clone()) + perimeter / 2 + 1;

    assert!(result == 46359, "Should be 46359");
    result.to_string()
}

pub fn part2(input: &str) -> String {
    let mut position: (i64, i64) = (0, 0);
    let mut coords: Vec<(i64, i64)> = Vec::new();
    let mut perimeter: i64 = 0;

    for line in input.lines() {
        let mut split_line = line.split_ascii_whitespace();
        let unparsed_instruction =
            split_line.nth(2).unwrap().chars().collect::<Vec<char>>();

        let direction = match u32::from_str_radix(
            &unparsed_instruction[7].to_string(),
            16,
        )
        .unwrap()
        {
            0 => Direction::R,
            1 => Direction::D,
            2 => Direction::L,
            3 => Direction::U,
            _ => panic!(),
        };

        let distance: i64 =
            i64::from_str_radix(&String::from_iter(&unparsed_instruction[2..7]), 16)
                .unwrap();

        perimeter += distance;

        match direction {
            Direction::U => position = (position.0 - distance, position.1),
            Direction::R => position = (position.0, position.1 + distance),
            Direction::D => position = (position.0 + distance, position.1),
            Direction::L => position = (position.0, position.1 - distance),
        }

        coords.push((position.0, position.1));
    }

    let result = shoelace(coords.clone()) + perimeter / 2 + 1;

    assert!(result == 59574883048274, "Should be 59574883048274");
    result.to_string()
}
