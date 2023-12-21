use std::collections::{hash_map::Entry, HashMap};

#[derive(Debug, Clone, PartialEq, Hash, Eq)]
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
    mut seen_arrangements: HashMap<(Sign, Vec<Sign>, Vec<u32>), u32>,
) -> (u32, HashMap<(Sign, Vec<Sign>, Vec<u32>), u32>) {
    if let Entry::Occupied(entry) = seen_arrangements.entry((
        previous_sign.to_owned(),
        diagram.clone(),
        spacing.clone(),
    )) {
        return (entry.get().to_owned(), seen_arrangements);
    }

    if diagram.is_empty() {
        if spacing.is_empty() {
            seen_arrangements.insert((previous_sign.to_owned(), diagram, spacing), 1);
            return (1, seen_arrangements);
        } else {
            seen_arrangements.insert((previous_sign.to_owned(), diagram, spacing), 0);
            return (0, seen_arrangements);
        }
    }

    match diagram[0] {
        Sign::Question => {
            let mut result = 0;

            let mut new_diagram = diagram.clone();
            new_diagram[0] = Sign::Broken;
            let (intermediate_total, seen_arrangements) = find_matching_arrangement(
                previous_sign,
                new_diagram,
                spacing.clone(),
                seen_arrangements,
            );
            result += intermediate_total;

            let mut new_diagram = diagram.clone();
            new_diagram[0] = Sign::Fixed;
            let (intermediate_total, seen_arrangements) = find_matching_arrangement(
                previous_sign,
                new_diagram,
                spacing.clone(),
                seen_arrangements,
            );
            result += intermediate_total;

            (result, seen_arrangements)
        }
        Sign::Broken => {
            if spacing.is_empty() {
                seen_arrangements
                    .insert((previous_sign.to_owned(), diagram, spacing), 0);
                return (0, seen_arrangements);
            }

            match previous_sign {
                Sign::Broken => (0, seen_arrangements),
                Sign::Fixed => {
                    let broken_length: usize = spacing[0] as usize;
                    if diagram.len() < broken_length {
                        seen_arrangements
                            .insert((previous_sign.to_owned(), diagram, spacing), 0);
                        return (0, seen_arrangements);
                    }
                    if diagram[0..broken_length].iter().any(|e| e == &Sign::Fixed) {
                        seen_arrangements
                            .insert((previous_sign.to_owned(), diagram, spacing), 0);
                        return (0, seen_arrangements);
                    }

                    let spacing = spacing[1..].to_vec();
                    let diagram = diagram[broken_length..].to_vec();
                    find_matching_arrangement(
                        &Sign::Broken,
                        diagram,
                        spacing,
                        seen_arrangements,
                    )
                }
                _ => panic!(),
            }
        }
        Sign::Fixed => {
            let diagram = diagram[1..].to_vec();

            match previous_sign {
                Sign::Broken => find_matching_arrangement(
                    &Sign::Fixed,
                    diagram,
                    spacing,
                    seen_arrangements,
                ),
                Sign::Fixed => find_matching_arrangement(
                    &Sign::Fixed,
                    diagram,
                    spacing,
                    seen_arrangements,
                ),
                _ => panic!(),
            }
        }
    }
}

pub fn part1(input: &str) -> String {
    let mut total = 0;

    for line in input.lines() {
        let (diagram, spacing) = line.split_once(' ').unwrap();
        let seen_arrangements = HashMap::new();

        total += find_matching_arrangement(
            &Sign::Fixed,
            Vec::from_iter(diagram.chars().map(|e| e.try_into().unwrap())),
            Vec::from_iter(spacing.split(',').map(|e| e.parse().unwrap())),
            seen_arrangements,
        )
        .0;
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
        let seen_arrangements = HashMap::new();
        total += find_matching_arrangement(
            &Sign::Fixed,
            Vec::from_iter(diagram.chars().map(|e| e.try_into().unwrap())),
            Vec::from_iter(spacing.split(',').map(|e| e.parse().unwrap())),
            seen_arrangements,
        )
        .0;
    }

    // Should be 45322533163795
    total.to_string()
}
