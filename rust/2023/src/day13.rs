use std::iter::zip;

fn transpose_pattern(pattern: String) -> Vec<String> {
    let max_x = pattern.lines().next().unwrap().len();

    // Get a vector of char vectors so we can index each row easily
    let lines_as_chars: Vec<Vec<char>> =
        pattern.lines().map(|e| e.chars().collect()).collect();

    let mut new_lines: Vec<String> = Vec::new();
    for x_coord in 0..max_x {
        new_lines.push(String::new());
        for line in lines_as_chars.iter() {
            new_lines[x_coord].push(line[x_coord]);
        }
    }

    new_lines
}

fn find_horizontal_mirror(lines: Vec<String>, smudges: usize) -> u32 {
    // Iterate over all indices except the last (as it can't start a mirror)
    for index in 0..lines.len() - 1 {
        let mut non_similar_chars = 0;

        // Iterate over all indices that we need to compare
        for up_index in 0..index + 1 {
            // Prevent an out of bounds index
            if index + up_index + 1 == lines.len() {
                break;
            }

            // Count characters that are not similar so that we can compare them against smudges
            non_similar_chars += zip(
                lines[index + up_index + 1].chars(),
                lines[index - up_index].chars(),
            )
            .filter(|e| e.0 != e.1)
            .count();

            // Exit early if this row already requires more smudges than available
            if non_similar_chars > smudges {
                break;
            }
        }

        // If this index has the correct amount of smudges required we return it + 1
        if non_similar_chars == smudges {
            return index as u32 + 1;
        }
    }
    0
}

pub fn part1(input: &str) -> String {
    let mut total = 0;

    for pattern in input.split("\n\n") {
        let lines: Vec<String> = pattern.lines().map(|e| e.to_string()).collect();
        match find_horizontal_mirror(lines, 0) {
            value if value > 0 => {
                total += value * 100;
                continue;
            }
            _ => (),
        }

        let lines = transpose_pattern(pattern.to_string());
        match find_horizontal_mirror(lines, 0) {
            value if value > 0 => {
                total += value;
                continue;
            }
            _ => panic!("Should have found vertical mirror"),
        }
    }

    assert!(total == 35538, "Should be 35538");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let mut total = 0;

    for pattern in input.split("\n\n") {
        let lines: Vec<String> = pattern.lines().map(|e| e.to_string()).collect();
        match find_horizontal_mirror(lines, 1) {
            value if value > 0 => {
                total += value * 100;
                continue;
            }
            _ => (),
        }

        let lines = transpose_pattern(pattern.to_string());
        match find_horizontal_mirror(lines, 1) {
            value if value > 0 => {
                total += value;
                continue;
            }
            _ => panic!("Should have found vertical mirror"),
        }
    }

    assert!(total == 30442, "Should be 30442");
    total.to_string()
}
