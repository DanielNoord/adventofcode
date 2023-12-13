fn transpose_pattern(pattern: String) -> Vec<String> {
    let lines_as_chars: Vec<Vec<char>> =
        pattern.lines().map(|e| e.chars().collect()).collect();

    let mut string_lines: Vec<String> = Vec::new();
    for x_coord in 0..pattern.lines().next().unwrap().len() {
        string_lines.push(String::new());
        for y_coord in 0..pattern.lines().count() {
            string_lines[x_coord].push(lines_as_chars[y_coord][x_coord]);
        }
    }

    string_lines
}

fn find_horizontal_mirror(lines: Vec<String>) -> u32 {
    // Iterate over all indices except the last (as it can't start a mirror)
    for index in 0..lines.len() - 1 {
        let mut no_mirror_found: bool = false;

        for up_index in 0..index + 1 {
            if index + up_index + 1 == lines.len() {
                break;
            }
            if lines[index + up_index + 1] != lines[index - up_index] {
                no_mirror_found = true;
                break;
            }
        }
        if !no_mirror_found {
            return index as u32 + 1;
        }
    }
    0
}

pub fn part1(input: &str) -> String {
    let mut total = 0;

    for pattern in input.split("\n\n") {
        let lines: Vec<String> = pattern.lines().map(|e| e.to_string()).collect();
        match find_horizontal_mirror(lines) {
            value if value > 0 => {
                total += value * 100;
                continue;
            }
            _ => (),
        }

        let lines = transpose_pattern(pattern.to_string());
        match find_horizontal_mirror(lines) {
            value if value > 0 => {
                total += value;
                continue;
            }
            _ => panic!("Should have found vertical mirror"),
        }
    }

    // Should be 35538
    // assert!(total == 35538, "Should be 35538");
    total.to_string()
}

pub fn part2(_input: &str) -> String {
    "".to_string()
}
