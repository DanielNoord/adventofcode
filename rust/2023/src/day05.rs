use std::collections::{HashMap, HashSet};

#[derive(Debug)]
enum Desination {
    String(u64),
    None,
}

fn parse_destination_source_map(mapping: &str) -> (Vec<u64>, HashMap<u64, Desination>) {
    let mut mapping_lines = mapping.lines();
    // Skip the first line
    mapping_lines.next();

    let mut indices: HashSet<u64> = HashSet::new();
    let mut values: HashMap<u64, Desination> = HashMap::new();

    for mapped_row in mapping_lines {
        let mut row_numbers = mapped_row.split(" ");
        let destination: u64 = row_numbers.next().unwrap().parse().unwrap();
        let source: u64 = row_numbers.next().unwrap().parse().unwrap();
        let range: u64 = row_numbers.next().unwrap().parse().unwrap();
        indices.insert(source);
        values.insert(source, Desination::String(destination));
        indices.insert(source + range);
        values.entry(source + range).or_insert(Desination::None);
    }
    let mut vec_of_indices = Vec::from_iter(indices);
    vec_of_indices.sort();
    (vec_of_indices, values)
}

fn find_next_destination(sources: Vec<u64>, mapping: &str) -> Vec<u64> {
    let (indices, values) = parse_destination_source_map(mapping);
    let mut desintations: Vec<u64> = Vec::new();

    for source in sources {
        let mut to_do = &Desination::None;
        let mut relevant_index = 0;
        for index in indices.clone() {
            if source >= index {
                to_do = values.get(&index).unwrap();
                relevant_index = index;
            } else {
                break;
            }
        }

        let destination = match to_do {
            Desination::None => source,
            Desination::String(start) => source - relevant_index + start,
        };
        desintations.push(destination);
    }
    desintations
}

fn find_next_ranges(ranges: Vec<(u64, u64)>, mapping: &str) -> Vec<(u64, u64)> {
    let (indices, values) = parse_destination_source_map(mapping);
    let mut new_ranges: Vec<(u64, u64)> = Vec::new();
    for range in ranges {
        let mut current_pointer = range.0;
        let mut last_to_do = &Desination::None;
        let mut last_index: u64 = 0;
        let end = range.1;

        for index in indices.clone() {
            if index >= end {
                match last_to_do {
                    Desination::None => {
                        new_ranges.push((current_pointer, end - 1));
                        current_pointer = end;
                    }
                    Desination::String(start) => {
                        new_ranges.push((
                            current_pointer - last_index + start,
                            end - last_index + start,
                        ));
                        current_pointer = end;
                    }
                }
                break;
            }
            if index >= current_pointer {
                match last_to_do {
                    Desination::None => {
                        new_ranges.push((current_pointer, index - 1));
                        current_pointer = index;
                    }
                    Desination::String(start) => {
                        new_ranges.push((
                            current_pointer - last_index + start,
                            index - last_index + start,
                        ));
                        current_pointer = index;
                    }
                }
            }

            last_to_do = values.get(&index).unwrap();
            last_index = index;
        }
        if current_pointer == range.0 {
            new_ranges.push(range);
        }
    }
    new_ranges
}

pub fn part1(input: &String) -> String {
    let mut split_input = input.split("\n\n");
    let seeds = split_input.next().unwrap();

    let seed_numbers: Vec<u64> = seeds
        .split_at(6)
        .1
        .split_ascii_whitespace()
        .map(|e| e.parse::<u64>().unwrap())
        .collect();

    let soils = find_next_destination(seed_numbers, split_input.next().unwrap());
    let fertilizers = find_next_destination(soils, split_input.next().unwrap());
    let waters = find_next_destination(fertilizers, split_input.next().unwrap());
    let lights = find_next_destination(waters, split_input.next().unwrap());
    let temps = find_next_destination(lights, split_input.next().unwrap());
    let humidities = find_next_destination(temps, split_input.next().unwrap());
    let locations = find_next_destination(humidities, split_input.next().unwrap());

    let result = locations.iter().min().unwrap();
    assert!(result == &322500873, "Should be 322500873");
    result.to_string()
}

pub fn part2(input: &String) -> String {
    let mut split_input = input.split("\n\n");
    let seeds = split_input.next().unwrap();
    let seed_ranges = seeds
        .split_at(6)
        .1
        .split_ascii_whitespace()
        .map(|e| e.parse::<u64>().unwrap())
        .collect::<Vec<u64>>()
        .chunks(2)
        .map(|c| (c[0], c[0] + c[1] - 1))
        .collect();

    let soils: Vec<(u64, u64)> =
        find_next_ranges(seed_ranges, split_input.next().unwrap());
    let fertilizers = find_next_ranges(soils, split_input.next().unwrap());
    let waters = find_next_ranges(fertilizers, split_input.next().unwrap());
    let lights = find_next_ranges(waters, split_input.next().unwrap());
    let temps: Vec<(u64, u64)> = find_next_ranges(lights, split_input.next().unwrap());
    let humidities = find_next_ranges(temps, split_input.next().unwrap());
    let locations = find_next_ranges(humidities, split_input.next().unwrap());

    let result = locations.iter().map(|x| x.0).min().unwrap();
    assert!(result == 108956227, "Should be 108956227");
    result.to_string()
}
