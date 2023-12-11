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

fn find_loop(
    input: &str,
) -> (
    u32,
    HashMap<usize, HashMap<usize, Directions>>,
    HashMap<usize, HashSet<usize>>,
) {
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
    let mut pipes_in_cycle: HashMap<usize, HashSet<usize>> = HashMap::new();
    pipes_in_cycle
        .entry(position_of_s.0)
        .or_default()
        .insert(position_of_s.1);

    loop {
        let mut new_pointers: Vec<_> = Vec::new();
        let mut found = false;

        for (old_position, current_position) in pointers.clone() {
            let direction = map
                .get(&current_position.0)
                .unwrap()
                .get(&current_position.1)
                .unwrap();
            if current_position == position_of_s {
                found = true;
                break;
            }

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
                pipes_in_cycle
                    .entry(current_position.0)
                    .or_insert(HashSet::new())
                    .insert(current_position.1);
                new_pointers.extend(potential_new_pointers);
            }
        }
        if found {
            break;
        }
        pointers = new_pointers;
        steps += 1;
    }

    (steps, map, pipes_in_cycle)
}

pub fn part1(input: &str) -> String {
    let (steps, _, _) = find_loop(input);
    let final_score = steps.div_ceil(2);

    assert!(final_score == 6717, "Should be 6717");
    final_score.to_string()
}

pub fn part2(input: &str) -> String {
    let (_, map, pipes_in_cycle) = find_loop(input);
    let mut total = 0;

    let max_y = map.len() - 1;
    let max_x = map.get(&(max_y)).unwrap().len() - 1;

    for y_coord in 0..max_y {
        let mut seen_pipes_in_row = 0;
        for x_coord in 0..max_x {
            if let Some(entry) = pipes_in_cycle.get(&y_coord) {
                if entry.contains(&x_coord) {
                    match map.get(&y_coord).unwrap().get(&x_coord).unwrap() {
                        Directions::Vertical
                        | Directions::NorthEast
                        | Directions::NorthWest
                        | Directions::Start => seen_pipes_in_row += 1,
                        _ => (),
                    }
                } else {
                    total += seen_pipes_in_row % 2;
                }
            } else {
                total += seen_pipes_in_row % 2;
            }
        }
    }

    assert!(total == 381, "Should be 381");
    total.to_string()
}
