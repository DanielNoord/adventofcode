use std::{collections::HashSet, iter::zip};

use itertools::Itertools;

fn partition_numbers(numbers: u32, bins: u32, lowest: u32) -> HashSet<Vec<u32>> {
    let mut final_bins: HashSet<Vec<u32>> = HashSet::new();

    match bins {
        1 => {
            final_bins.insert(vec![numbers]);
        }
        _ if bins > 1 => {
            for i in lowest..(numbers / 2 + 1) {
                for p in partition_numbers(numbers - i, bins - 1, i) {
                    let mut bin = p;
                    bin.push(i);
                    final_bins.insert(bin);
                }
            }
        }
        _ => (),
    }

    final_bins
}

pub fn part1(input: &str) -> String {
    let mut total = 0;
    for line in input.lines() {
        let mut split_line = line.split(' ');
        let current_diagram = split_line.next().unwrap();
        let spacing = split_line.next().unwrap();

        let diagram_length = current_diagram.len();
        let mut dividers: u32 = 2;
        let mut space_for_dividers: u32 = diagram_length as u32;
        let mut space_indicators: Vec<u32> = Vec::new();

        for instruction in spacing.replace(',', " , ").split(' ') {
            if instruction == "," {
                dividers += 1;
                space_for_dividers -= 1;
            } else {
                let value: u32 = instruction.parse().unwrap();
                space_for_dividers -= value;
                space_indicators.push(value);
            }
        }

        let partitions: HashSet<Vec<u32>> = HashSet::from_iter(
            partition_numbers(space_for_dividers, dividers, 0)
                .into_iter()
                .flat_map(|e| e.clone().into_iter().permutations(e.len())),
        );

        for mut final_partition in partitions {
            let len = &final_partition.len();
            for (index, value) in final_partition.iter_mut().enumerate() {
                if index != 0 && &index != len {
                    *value += 1;
                }
            }
            let mut damaged_indicators = space_indicators.clone();
            damaged_indicators.push(0);
            let mut indicator_iter = damaged_indicators.iter();
            let mut diagram = String::new();
            for divider_count in final_partition {
                diagram += &".".repeat(divider_count as usize);
                diagram += &"#".repeat(*indicator_iter.next().unwrap() as usize);
            }

            if space_indicators.len()
                != diagram.replace('.', " ").split_ascii_whitespace().count()
            {
                continue;
            }

            let mut good = true;
            for (c, d) in zip(current_diagram.chars(), diagram.chars()) {
                match c {
                    '?' => (),
                    _ => {
                        if c != d {
                            good = false;
                            break;
                        }
                    }
                }
            }
            if good {
                total += 1;
            }
        }
    }

    assert!(total == 8193, "Should be 8193");
    total.to_string()
}

pub fn part2(_input: &str) -> String {
    let total = 0;

    // Should be 45322533163795
    total.to_string()
}
