use std::collections::{HashMap, HashSet};

fn find_all_manhattan_distances(input: &str, expansion_factor: usize) -> usize {
    let mut image: HashMap<usize, HashSet<usize>> = HashMap::new();
    let mut empty_rows: HashSet<usize> = HashSet::new();
    let mut galaxies: Vec<(usize, usize)> = Vec::new();

    for (index, line) in input.lines().enumerate() {
        let entry = image.entry(index).or_default();
        for (x_index, point) in line.char_indices() {
            if point == '#' {
                entry.insert(x_index);
                galaxies.push((index, x_index))
            }
        }
        if entry.is_empty() {
            empty_rows.insert(index);
        }
    }

    let max_y = image.len();
    let max_x = input.lines().next().unwrap().len();
    let mut empty_columns: HashSet<usize> = HashSet::new();

    for x_coord in 0..max_x {
        let mut found_galaxy = false;
        for y_coord in 0..max_y {
            if let Some(entry) = image.get(&y_coord) {
                if entry.contains(&x_coord) {
                    found_galaxy = true;
                    break;
                }
            }
        }
        if !found_galaxy {
            empty_columns.insert(x_coord);
        }
    }

    let mut total = 0;
    while !galaxies.is_empty() {
        let starting_galaxy = galaxies.remove(0);

        for galaxy in &galaxies {
            let mut y_coords = [starting_galaxy.0, galaxy.0];
            y_coords.sort();
            let mut x_coords = [starting_galaxy.1, galaxy.1];
            x_coords.sort();

            let y_range = y_coords[0]..y_coords[1];
            let x_range = x_coords[0]..x_coords[1];

            let mut steps = y_range.clone().count() + x_range.clone().count();
            for empty_row in &empty_rows {
                if y_range.contains(empty_row) {
                    steps += expansion_factor - 1;
                }
            }
            for empty_column in &empty_columns {
                if x_range.contains(empty_column) {
                    steps += expansion_factor - 1;
                }
            }
            total += steps;
        }
    }
    total
}

pub fn part1(input: &str) -> String {
    let result = find_all_manhattan_distances(input, 2);

    assert!(result == 10231178, "Should be 10231178");
    result.to_string()
}

pub fn part2(input: &str) -> String {
    let result = find_all_manhattan_distances(input, 1000000);

    assert!(result == 622120986954, "Should be 622120986954");
    result.to_string()
}
