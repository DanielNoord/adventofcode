use std::collections::{HashMap, HashSet};

#[derive(Debug, PartialEq)]
enum Plot {
    Rock,
    Garden,
    Start,
}

impl From<char> for Plot {
    fn from(value: char) -> Self {
        match value {
            '#' => Plot::Rock,
            '.' => Plot::Garden,
            'S' => Plot::Start,
            _ => panic!("Unsupported plot {}", value),
        }
    }
}

fn get_map(input: &str) -> (HashMap<usize, HashMap<usize, Plot>>, (usize, usize)) {
    let mut plot_map: HashMap<usize, HashMap<usize, Plot>> = HashMap::new();
    let mut position_of_s = (0, 0);

    for (index, line) in input.lines().enumerate() {
        for (x_index, char_value) in line.char_indices() {
            let plot: Plot = char_value.into();

            if plot == Plot::Start {
                position_of_s = (index, x_index);
            }

            plot_map.entry(index).or_default().insert(x_index, plot);
        }
    }
    (plot_map, position_of_s)
}

fn get_neighbours(position: (usize, usize)) -> Vec<(usize, usize)> {
    let mut neighbours: Vec<(usize, usize)> = Vec::new();
    if position.0 != usize::MIN {
        neighbours.push((position.0 - 1, position.1))
    }
    if position.1 != usize::MIN {
        neighbours.push((position.0, position.1 - 1))
    }
    neighbours.push((position.0 + 1, position.1));
    neighbours.push((position.0, position.1 + 1));

    neighbours
}

fn flood_fill(
    map: &HashMap<usize, HashMap<usize, Plot>>,
    current_positions: HashSet<(usize, usize)>,
    seen: &mut HashSet<(usize, usize)>,
) -> HashSet<(usize, usize)> {
    let mut new_positions: HashSet<(usize, usize)> = HashSet::new();
    for position in current_positions {
        seen.insert(position);
        for neighbour in get_neighbours(position) {
            if seen.contains(&neighbour) {
                continue;
            }

            if let Some(row) = map.get(&neighbour.0) {
                if let Some(entry) = row.get(&neighbour.1) {
                    if entry == &Plot::Garden {
                        new_positions.insert(neighbour);
                    }
                }
            }
        }
    }
    new_positions
}

pub fn part1(input: &str) -> String {
    let (map, position_of_s) = get_map(input);

    let mut seen: HashSet<(usize, usize)> = HashSet::new();
    let mut positions: HashSet<(usize, usize)> = HashSet::new();
    positions.insert(position_of_s);

    let mut options = HashSet::new();
    options.insert(position_of_s);

    for index in 1..65 {
        positions = flood_fill(&map, positions, &mut seen);
        if index % 2 == 0 {
            options.extend(positions.clone());
        }
    }

    // Should be 3853
    options.len().to_string()
}

fn flood_fill2(
    map: &HashMap<usize, HashMap<usize, Plot>>,
    current_positions: HashSet<(usize, usize)>,
    seen: &mut HashSet<(usize, usize)>,
    map_len: usize,
) -> HashSet<(usize, usize)> {
    let mut new_positions: HashSet<(usize, usize)> = HashSet::new();
    for position in current_positions {
        seen.insert(position);
        for neighbour in get_neighbours(position) {
            if seen.contains(&neighbour) {
                continue;
            }
            // println!("INITIAL {} {}", neighbour.0, neighbour.1);

            let y_coord = if neighbour.0 >= map_len {
                neighbour.0 % (map_len - 1)
            } else {
                neighbour.0
            };

            let x_coord = if neighbour.1 >= map_len - 1 {
                neighbour.1 % (map_len - 1)
            } else {
                neighbour.1
            };

            // println!("{} {}", y_coord, x_coord);

            if map.get(&y_coord).unwrap().get(&x_coord).unwrap() == &Plot::Garden {
                new_positions.insert(neighbour);
            }
        }
    }
    new_positions
}

pub fn part2(input: &str) -> String {
    let (map, position_of_s) = get_map(input);

    let mut seen: HashSet<(usize, usize)> = HashSet::new();
    let mut positions: HashSet<(usize, usize)> = HashSet::new();
    positions.insert(position_of_s);

    let map_len = map.len();

    let mut options = HashSet::new();
    options.insert(position_of_s);

    for index in 1..200000000 {
        positions = flood_fill2(&map, positions, &mut seen, map_len);
        if positions.contains(&(position_of_s.0 + (1 * map_len), position_of_s.1)) {
            println!("1 {}", index);
            println!("{}", options.len());
            // panic!();
        }
        if positions.contains(&(position_of_s.0 + (2 * map_len), position_of_s.1)) {
            println!("4 {}", index);
            println!("{}", options.len());
            // panic!();
        }
        if positions.contains(&(position_of_s.0 + (3 * map_len), position_of_s.1)) {
            println!("8 {}", index);
            println!("{}", options.len());
            // panic!();
        }

        if index % 2 == 0 {
            options.extend(positions.clone());
        }
    }

    // Should be 639.051.580.070.841
    options.len().to_string()
}
