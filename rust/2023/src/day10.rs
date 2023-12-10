use std::collections::{hash_map::RandomState, HashMap, HashSet};

#[derive(Debug)]
enum Directions {
    Vertical,
    Horizontal,
    NorthEast,
    NorthWest,
    SouthWest,
    SouthEast,
    Ground,
    Start,
}

impl From<char> for Directions {
    fn from(value: char) -> Self {
        match value {
            '|' => Directions::Vertical,
            '-' => Directions::Horizontal,
            'L' => Directions::NorthEast,
            'J' => Directions::NorthWest,
            '7' => Directions::SouthWest,
            'F' => Directions::SouthEast,
            '.' => Directions::Ground,
            'S' => Directions::Start,
            _ => panic!("Unexpected char: {value}"),
        }
    }
}

fn make_move(position: (usize, usize), direction: &Directions) -> Vec<(usize, usize)> {
    match direction {
        Directions::Vertical => {
            vec![(position.0 - 1, position.1), (position.0 + 1, position.1)]
        }
        Directions::Horizontal => {
            vec![(position.0, position.1 - 1), (position.0, position.1 + 1)]
        }
        Directions::NorthEast => {
            vec![(position.0 - 1, position.1), (position.0, position.1 + 1)]
        }
        Directions::NorthWest => {
            vec![(position.0 - 1, position.1), (position.0, position.1 - 1)]
        }
        Directions::SouthEast => {
            vec![(position.0 + 1, position.1), (position.0, position.1 + 1)]
        }
        Directions::SouthWest => {
            vec![(position.0 + 1, position.1), (position.0, position.1 - 1)]
        }
        Directions::Ground => {
            vec![]
        }
        Directions::Start => {
            vec![
                (position.0 - 1, position.1),
                (position.0 + 1, position.1),
                (position.0, position.1 - 1),
                (position.0, position.1 + 1),
            ]
        }
    }
}

pub fn part1(input: &str) -> String {
    let mut map: HashMap<usize, HashMap<usize, Directions>> = HashMap::new();
    let mut position_of_s = (0 as usize, 0 as usize);
    for (index, line) in input.lines().enumerate() {
        let row: HashMap<usize, Directions, RandomState> = HashMap::from_iter(
            line.char_indices().map(|e| (e.0, e.1.try_into().unwrap())),
        );
        if let Some(s_index) = line.find('S') {
            position_of_s = (index, s_index);
        }
        map.insert(index, row);
    }

    // Create an initial step from the start point
    let mut pointers: Vec<((usize, usize), (usize, usize))> = Vec::from_iter(
        make_move(position_of_s, &Directions::Start)
            .iter()
            .map(|e| (position_of_s, e.to_owned())),
    );

    let mut steps = 0;
    loop {
        let mut new_pointers: Vec<_> = Vec::new();

        pointers.dedup_by(|a, b| a.1 == b.1);

        if pointers.len() == 1 {
            break;
        }

        for (old_position, current_position) in pointers {
            let direction = map
                .get(&current_position.0)
                .unwrap()
                .get(&current_position.1)
                .unwrap();

            let mut valid = false;
            let mut potential_new_pointers: Vec<_> = Vec::new();
            for potential_move in make_move(current_position, direction) {
                if potential_move == old_position {
                    valid = true;
                } else {
                    potential_new_pointers.push((current_position, potential_move))
                }
            }
            if valid {
                new_pointers.extend(potential_new_pointers);
            }
        }
        pointers = new_pointers;
        steps += 1;
    }

    // Should be 6716
    steps.to_string()
}

pub fn part2(input: &str) -> String {
    let mut map: HashMap<usize, HashMap<usize, Directions>> = HashMap::new();
    let mut position_of_s = (0 as usize, 0 as usize);
    for (index, line) in input.lines().enumerate() {
        let row: HashMap<usize, Directions, RandomState> = HashMap::from_iter(
            line.char_indices().map(|e| (e.0, e.1.try_into().unwrap())),
        );
        if let Some(s_index) = line.find('S') {
            position_of_s = (index, s_index);
        }
        map.insert(index, row);
    }

    // Create an initial step from the start point
    let mut pointers: Vec<((usize, usize), (usize, usize))> = Vec::from_iter(
        make_move(position_of_s, &Directions::Start)
            .iter()
            .map(|e| (position_of_s, e.to_owned())),
    );

    let mut total = 0;
    let mut new_map: HashMap<usize, HashSet<usize>> = HashMap::new();
    loop {
        let mut new_pointers: Vec<_> = Vec::new();

        pointers.dedup_by(|a, b| a.1 == b.1);

        if pointers.len() == 1 {
            new_map
                .entry(pointers[0].1 .0)
                .or_default()
                .insert(pointers[0].1 .1);
            break;
        }

        for (old_position, current_position) in pointers {
            let direction = map
                .get(&current_position.0)
                .unwrap()
                .get(&current_position.1)
                .unwrap();

            let mut valid = false;
            let mut potential_new_pointers: Vec<_> = Vec::new();
            for potential_move in make_move(current_position, direction) {
                if potential_move == old_position {
                    valid = true;
                } else {
                    potential_new_pointers.push((current_position, potential_move))
                }
            }
            if valid {
                new_map
                    .entry(current_position.0)
                    .or_insert(HashSet::new())
                    .insert(current_position.1);
                new_map
                    .entry(old_position.0)
                    .or_insert(HashSet::new())
                    .insert(old_position.1);
                new_pointers.extend(potential_new_pointers);
            }
        }
        pointers = new_pointers;
    }

    // 1359 too high
    // 394 is too high
    total.to_string()
}
