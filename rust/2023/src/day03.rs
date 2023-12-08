use std::collections::{HashMap, HashSet};

fn get_all_coords(y_coord: usize, x_coord: usize) -> Vec<(usize, usize)> {
    // This assumes that there are no symbols in the outermost rows or columns
    // And that no symbol and digit can be on the same spot at the same time
    let mut coords: Vec<(usize, usize)> = Vec::new();
    coords.push((y_coord - 1, x_coord - 1));
    coords.push((y_coord - 1, x_coord));
    coords.push((y_coord - 1, x_coord + 1));
    coords.push((y_coord, x_coord - 1));
    coords.push((y_coord, x_coord + 1));
    coords.push((y_coord + 1, x_coord - 1));
    coords.push((y_coord + 1, x_coord));
    coords.push((y_coord + 1, x_coord + 1));
    coords
}

pub fn part1(input: &str) -> String {
    let mut valid_positions: HashSet<(usize, usize)> = HashSet::new();

    for (line_index, line) in input.lines().enumerate() {
        for (char_index, char) in line.char_indices() {
            if char != '.' && !char.is_ascii_digit() {
                for valid_pos in get_all_coords(line_index, char_index) {
                    valid_positions.insert(valid_pos);
                }
            }
        }
    }

    let mut total: u32 = 0;
    for (line_index, line) in input.lines().enumerate() {
        let mut current_number: String = String::new();
        let mut is_valid: bool = false;
        for (char_index, char) in line.char_indices() {
            if char.is_ascii_digit() {
                current_number.push(char);
                if !is_valid {
                    is_valid = valid_positions.contains(&(line_index, char_index));
                }
            } else {
                if is_valid && current_number != "" {
                    let value: u32 = current_number.parse().unwrap();
                    total += value;
                }
                current_number = String::new();
                is_valid = false;
            }
        }
        if is_valid && current_number != "" {
            let value: u32 = current_number.parse().unwrap();
            total += value;
        }
    }
    assert!(total == 537832, "Should be 537832");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let mut valid_positions: HashMap<(usize, usize), (usize, usize)> = HashMap::new();

    for (line_index, line) in input.lines().enumerate() {
        for (char_index, char) in line.char_indices() {
            if char == '*' {
                for valid_pos in get_all_coords(line_index, char_index) {
                    valid_positions.insert(valid_pos, (line_index, char_index));
                }
            }
        }
    }

    let mut gears: HashMap<(usize, usize), (u32, u32)> = HashMap::new();
    for (line_index, line) in input.lines().enumerate() {
        let mut current_number: String = String::new();
        let mut is_valid: bool = false;
        let mut gear: (usize, usize) = (usize::MIN, usize::MIN);
        for (char_index, char) in line.char_indices() {
            if char.is_ascii_digit() {
                current_number.push(char);
                if !is_valid {
                    if valid_positions.contains_key(&(line_index, char_index)) {
                        is_valid = true;
                        gear = valid_positions
                            .get(&(line_index, char_index))
                            .unwrap()
                            .to_owned();
                    }
                }
            } else {
                if is_valid && current_number != "" {
                    let value: u32 = current_number.parse().unwrap();
                    gears
                        .entry(gear)
                        .and_modify(|e| {
                            e.0 += 1;
                            e.1 *= value;
                        })
                        .or_insert((1, value));
                }
                current_number = String::new();
                is_valid = false;
            }
        }
        if is_valid && current_number != "" {
            let value: u32 = current_number.parse().unwrap();
            gears
                .entry(gear)
                .and_modify(|e| {
                    e.0 += 1;
                    e.1 *= value;
                })
                .or_insert((1, value));
        }
    }

    let mut total: u32 = 0;
    for (count, entry_value) in gears.values() {
        if count == &2 {
            total += entry_value;
        }
    }
    assert!(total == 81939900, "Should be 81939900");
    total.to_string()
}
