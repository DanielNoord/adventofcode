use std::collections::{hash_map::Entry, HashMap};

#[derive(Debug)]
enum Space {
    Empty,
    // This is '/'
    MirrorUp,
    // This is '\'
    MirrorDown,
    VerticalSplitter,
    HorizontalSplitter,
}

impl From<char> for Space {
    fn from(value: char) -> Self {
        match value {
            '.' => Space::Empty,
            '/' => Space::MirrorUp,
            '\\' => Space::MirrorDown,
            '|' => Space::VerticalSplitter,
            '-' => Space::HorizontalSplitter,
            _ => panic!("Unexpected space value {}", value),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

fn get_map(input: &str) -> HashMap<usize, Vec<Space>> {
    let mut map = HashMap::new();
    for (index, line) in input.lines().enumerate() {
        let spaces: Vec<Space> = line.chars().map(|e| e.try_into().unwrap()).collect();
        map.insert(index, spaces);
    }
    map
}

fn do_loop(
    mut position: ((usize, usize), Direction),
    map_of_cave: &HashMap<usize, Vec<Space>>,
    mut visited: HashMap<usize, HashMap<usize, Vec<Direction>>>,
) -> HashMap<usize, HashMap<usize, Vec<Direction>>> {
    let max_y = map_of_cave.len();
    let max_x = map_of_cave.get(&0).unwrap().len();

    loop {
        // Prevent index errors
        if position.0 .0 == max_y || position.0 .1 == max_x {
            return visited;
        }

        if let Entry::Occupied(mut rows) = visited.entry(position.0 .0) {
            {
                if let Entry::Occupied(directions) = rows.get_mut().entry(position.0 .1)
                {
                    if directions.get().contains(&position.1) {
                        break;
                    }
                }
            }
        }

        visited
            .entry(position.0 .0)
            .or_default()
            .entry(position.0 .1)
            .or_default()
            .push(position.1);

        match &map_of_cave.get(&position.0 .0).unwrap()[position.0 .1] {
            Space::Empty => (),
            Space::VerticalSplitter => match position.1 {
                Direction::Right | Direction::Left => {
                    if position.0 .0 != usize::MIN {
                        let upward_position =
                            ((position.0 .0 - 1, position.0 .1), Direction::Up);
                        visited = do_loop(upward_position, map_of_cave, visited);
                    }

                    let downward_position =
                        ((position.0 .0 + 1, position.0 .1), Direction::Down);
                    visited = do_loop(downward_position, map_of_cave, visited);
                    break;
                }
                Direction::Up | Direction::Down => (),
            },
            Space::HorizontalSplitter => match position.1 {
                Direction::Up | Direction::Down => {
                    let rightward_position =
                        ((position.0 .0, position.0 .1 + 1), Direction::Right);
                    visited = do_loop(rightward_position, map_of_cave, visited);

                    if position.0 .1 != usize::MIN {
                        let leftward =
                            ((position.0 .0, position.0 .1 - 1), Direction::Left);
                        visited = do_loop(leftward, map_of_cave, visited);
                    }
                    break;
                }
                Direction::Right | Direction::Left => (),
            },
            Space::MirrorUp => match position.1 {
                Direction::Up => position = (position.0, Direction::Right),
                Direction::Right => position = (position.0, Direction::Up),
                Direction::Down => position = (position.0, Direction::Left),
                Direction::Left => position = (position.0, Direction::Down),
            },
            Space::MirrorDown => match position.1 {
                Direction::Up => position = (position.0, Direction::Left),
                Direction::Right => position = (position.0, Direction::Down),
                Direction::Down => position = (position.0, Direction::Right),
                Direction::Left => position = (position.0, Direction::Up),
            },
        }

        match position.1 {
            Direction::Up => {
                if position.0 .0 == usize::MIN {
                    return visited;
                }
                position = ((position.0 .0 - 1, position.0 .1), position.1)
            }
            Direction::Right => {
                position = ((position.0 .0, position.0 .1 + 1), position.1)
            }
            Direction::Down => {
                position = ((position.0 .0 + 1, position.0 .1), position.1)
            }
            Direction::Left => {
                if position.0 .1 == usize::MIN {
                    break;
                }
                position = ((position.0 .0, position.0 .1 - 1), position.1)
            }
        }
    }

    visited
}

pub fn part1(input: &str) -> String {
    let map_of_cave = get_map(input);
    let initial_position: ((usize, usize), Direction) = ((0, 0), Direction::Right);
    let mut visited: HashMap<usize, HashMap<usize, Vec<Direction>>> = HashMap::new();

    visited = do_loop(initial_position, &map_of_cave, visited);

    let total: usize = visited.values().map(|e| e.keys().len()).sum();

    assert!(total == 8112, "Should be 8112");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let map_of_cave = get_map(input);
    let max_y = map_of_cave.len();
    let max_x = map_of_cave.get(&0).unwrap().len();

    let mut highest_total = 0;
    for y_index in 0..max_y {
        let mut visited: HashMap<usize, HashMap<usize, Vec<Direction>>> =
            HashMap::new();
        visited = do_loop(((y_index, 0), Direction::Right), &map_of_cave, visited);
        let total: usize = visited.values().map(|e| e.keys().len()).sum();
        highest_total = highest_total.max(total);

        let mut visited: HashMap<usize, HashMap<usize, Vec<Direction>>> =
            HashMap::new();
        visited = do_loop(
            ((y_index, max_x - 1), Direction::Left),
            &map_of_cave,
            visited,
        );
        let total: usize = visited.values().map(|e| e.keys().len()).sum();
        highest_total = highest_total.max(total);
    }
    for x_index in 0..max_x {
        let mut visited: HashMap<usize, HashMap<usize, Vec<Direction>>> =
            HashMap::new();
        visited = do_loop(((0, x_index), Direction::Down), &map_of_cave, visited);
        let total: usize = visited.values().map(|e| e.keys().len()).sum();
        highest_total = highest_total.max(total);

        let mut visited: HashMap<usize, HashMap<usize, Vec<Direction>>> =
            HashMap::new();
        visited = do_loop(((max_y - 1, x_index), Direction::Up), &map_of_cave, visited);
        let total: usize = visited.values().map(|e| e.keys().len()).sum();
        highest_total = highest_total.max(total);
    }

    assert!(highest_total == 8314, "Should be 8314");
    highest_total.to_string()
}
