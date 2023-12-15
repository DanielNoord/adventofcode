use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
enum Sign {
    Broken,
    Fixed,
    Question,
}

impl From<char> for Sign {
    fn from(value: char) -> Self {
        match value {
            '?' => Sign::Question,
            '#' => Sign::Broken,
            '.' => Sign::Fixed,
            _ => panic!(),
        }
    }
}

fn find_matching_arrangement(
    previous_sign: &Sign,
    diagram: Vec<Sign>,
    spacing: Vec<u32>,
) -> u32 {
    if diagram.is_empty() {
        if spacing.is_empty() {
            return 1;
        } else {
            return 0;
        }
    }

    match diagram[0] {
        Sign::Question => {
            let mut intermediate_total = 0;

            let mut new_diagram = diagram.clone();
            new_diagram[0] = Sign::Broken;
            println!("{:?}", diagram);
            println!("{:?}", new_diagram);
            intermediate_total +=
                find_matching_arrangement(previous_sign, new_diagram, spacing.clone());

            let mut new_diagram = diagram.clone();
            new_diagram[0] = Sign::Fixed;
            intermediate_total +=
                find_matching_arrangement(previous_sign, new_diagram, spacing.clone());
            intermediate_total
        }
        Sign::Broken => {
            if spacing.is_empty() {
                return 0;
            }

            match previous_sign {
                Sign::Broken => 0,
                Sign::Fixed => {
                    let broken_length: usize = spacing[0] as usize;
                    if diagram.len() < broken_length {
                        return 0;
                    }
                    if diagram[0..broken_length].iter().any(|e| e == &Sign::Fixed) {
                        return 0;
                    }

                    let spacing = spacing[1..].to_vec();
                    let diagram = diagram[broken_length..].to_vec();
                    find_matching_arrangement(&Sign::Broken, diagram, spacing)
                }
                _ => panic!(),
            }
        }
        Sign::Fixed => {
            let diagram = diagram[1..].to_vec();

            match previous_sign {
                Sign::Broken => {
                    find_matching_arrangement(&Sign::Fixed, diagram, spacing)
                }
                Sign::Fixed => {
                    find_matching_arrangement(&Sign::Fixed, diagram, spacing)
                }
                _ => panic!(),
            }
        }
    }
}

pub fn part1(input: &str) -> String {
    let mut total = 0;

    for line in input.lines() {
        let (diagram, spacing) = line.split_once(' ').unwrap();
        total += find_matching_arrangement(
            &Sign::Fixed,
            Vec::from_iter(diagram.chars().map(|e| e.try_into().unwrap())),
            Vec::from_iter(spacing.split(',').map(|e| e.parse().unwrap())),
        );
    }

    assert!(total == 8193, "Should be 8193 {total}");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let mut total = 0;

    for (index, line) in input.lines().enumerate() {
        println!("{}", index);
        let (diagram, spacing) = line.split_once(' ').unwrap();
        let diagram = [diagram; 5].join("?");
        let spacing = [spacing; 5].join(",");
        total += find_matching_arrangement(
            &Sign::Fixed,
            Vec::from_iter(diagram.chars().map(|e| e.try_into().unwrap())),
            Vec::from_iter(spacing.split(',').map(|e| e.parse().unwrap())),
        );
    }

    // Should be 45322533163795
    total.to_string()
}
