use std::{collections::HashMap, str::FromStr};

use num::Integer;

#[derive(Debug)]
struct Node {
    name: String,
    left: String,
    right: String,
}

impl FromStr for Node {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Node {
            name: s[..3].to_string(),
            left: s[7..10].to_string(),
            right: s[12..15].to_string(),
        })
    }
}

pub fn part1(input: &str) -> String {
    let mut split_input = input.split("\n\n");
    let mut instructions = split_input.next().unwrap().chars().cycle();

    let nodes = split_input.next().unwrap().lines().map(|x| {
        let node = x.parse::<Node>().unwrap();
        (node.name.clone(), node)
    });
    let nodes_map: HashMap<String, Node> = HashMap::from_iter(nodes);

    let mut steps = 0;
    let mut pointer = String::from("AAA");
    while pointer != "ZZZ" {
        steps += 1;
        let instruct = instructions.next().unwrap();
        if instruct == 'L' {
            pointer = nodes_map.get(&pointer).unwrap().left.to_owned();
        } else {
            pointer = nodes_map.get(&pointer).unwrap().right.to_owned();
        }
    }

    assert!(steps == 16531, "Should be 16531");
    steps.to_string()
}

pub fn part2(input: &str) -> String {
    let mut split_input = input.split("\n\n");
    let instructions_str = split_input.next().unwrap();

    let nodes = split_input.next().unwrap().lines().map(|x| {
        let node = x.parse::<Node>().unwrap();
        (node.name.clone(), node)
    });
    let nodes_map: HashMap<String, Node> = HashMap::from_iter(nodes);

    let mut starts: Vec<&String> = nodes_map
        .iter()
        .filter(|x| x.0.ends_with('A'))
        .map(|x| x.0)
        .collect();

    let mut cycles: Vec<u128> = Vec::new();
    for value in &mut starts {
        let mut steps = 0;
        let mut previous_z_step = 0;
        let mut cycle_steps = 0;
        let mut instructions = instructions_str.chars().cycle();
        loop {
            steps += 1;
            let instruct = instructions.next().unwrap();

            if instruct == 'L' {
                *value = &nodes_map.get(&value.to_owned()).unwrap().left;
            } else {
                *value = &nodes_map.get(&value.to_owned()).unwrap().right;
            }
            if value.ends_with('Z') {
                if steps - previous_z_step == cycle_steps {
                    cycles.push(cycle_steps);
                    break;
                }
                cycle_steps = steps - previous_z_step;
                previous_z_step = steps;
            }
        }
    }

    let score = cycles.iter().copied().reduce(|acc, e| acc.lcm(&e)).unwrap();
    assert!(score == 24035773251517, "Should be 24035773251517");
    score.to_string()
}
