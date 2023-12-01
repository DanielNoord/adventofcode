use std::collections::HashMap;

fn get_all_positions(line: &str) -> HashMap<(i32, i32), u32> {
    let mut result: HashMap<(i32, i32), u32> = HashMap::new();
    let mut pointer = (0, 0);
    let mut counter: u32 = 0;

    for instruction in line.split(",") {
        let (direction, string_value) = instruction.split_at(1);
        let value: i32 = string_value.parse().expect("Expected a value");
        for _ in 0..value {
            counter += 1;
            pointer = match direction {
                "R" => (pointer.0, pointer.1 + 1),
                "D" => (pointer.0 - 1, pointer.1),
                "L" => (pointer.0, pointer.1 - 1),
                "U" => (pointer.0 + 1, pointer.1),
                _ => panic!("Unexpected instruction"),
            };
            result.entry(pointer).or_insert_with(|| counter);
        }
    }
    result
}

pub fn part1(input: &String) -> String {
    let mut lines: std::str::Lines<'_> = input.lines();
    let line1 = get_all_positions(lines.next().expect("Expected a first line"));
    let mut line2 = get_all_positions(lines.next().expect("Expected a second line"));

    line2.retain(|k, _v| line1.contains_key(k));

    let mut distances: Vec<i32> = Vec::new();
    for val in line2 {
        distances.push(val.0 .0.abs() + val.0 .1.abs());
    }

    let result = distances.iter().min().expect("");
    assert!(result == &855, "Should be 855");
    return result.to_string();
}

pub fn part2(input: &String) -> String {
    let mut lines: std::str::Lines<'_> = input.lines();
    let line1 = get_all_positions(lines.next().expect("Expected a first line"));
    let mut line2 = get_all_positions(lines.next().expect("Expected a second line"));

    line2.retain(|k, _v| line1.contains_key(k));

    let mut distances: Vec<u32> = Vec::new();
    for val in line2 {
        distances.push(val.1 + line1.get(&val.0).expect(""));
    }

    let result = distances.iter().min().expect("");
    assert!(result == &11238, "Should be 11238");
    return result.to_string();
}
